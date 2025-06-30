from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import sys
import yaml
import uuid
import re # Import re directly
import markdown # For view_file, ensure it's imported where needed

# Add the parent directory to the sys.path to allow relative imports
# Assuming web_app.py is in knowledge_reinforcer/
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR) # This should be template-rules-1/
STAGING_DIR = os.path.join(CURRENT_SCRIPT_DIR, 'staging_area') # staging_area inside knowledge_reinforcer

# Ensure STAGING_DIR exists
os.makedirs(STAGING_DIR, exist_ok=True)

# Adjust sys.path to correctly find sibling modules like fetcher, processor, storage
# if they are in the same directory as web_app.py or if knowledge_reinforcer is a package
# If knowledge_reinforcer is treated as a package, imports should be relative like from .fetcher import ...
# For now, assuming direct imports work if PROJECT_ROOT is in sys.path or structure is flat.
# The original code had `sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))`
# which added the parent of knowledge_reinforcer (i.e., PROJECT_ROOT) to the path.
# Let's ensure that's robust or use relative imports if knowledge_reinforcer is a proper package.
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from knowledge_reinforcer.fetcher import fetch_content
from knowledge_reinforcer.processor import process_content_to_markdown
from knowledge_reinforcer.storage import save_to_knowledge_base, BASE_KNOWLEDGE_DIR
# kb_utils will be imported by routes that need it, once created and used.

app = Flask(__name__, template_folder='templates')
# IMPORTANT: Set a secret key for Flask sessions to work!
# Replace 'dev_default_secret_key_please_change_me' with a real secret key,
# preferably from an environment variable in production.
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_default_secret_key_please_change_me')

@app.route('/')
def index():
    message = request.args.get('message')
    # Clear any stale staged item from session when returning to index
    if 'staged_item_details' in session:
        # Potentially add logic here to clean up the actual temp file 
        # if session['staged_item_details'].get('temp_id') else just pop
        session.pop('staged_item_details', None)
    return render_template('index.html', message=message)

@app.route('/process_input', methods=['POST'])
def process_input():
    url = request.form.get('url')
    text = request.form.get('text')
    # Get title from form, default to empty string if not provided
    title_from_form = request.form.get('title', '').strip()
    tags_str = request.form.get('tags', '')
    purpose = request.form.get('purpose', '')

    tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

    content_type = None
    raw_content = None
    source_url = None
    title = title_from_form # Start with user-provided title

    if url:
        source_url = url
        content_type = "youtube-video" if "youtube.com/watch" in url or "youtu.be/" in url else "web-article"
        
        print(f"Fetching content from: {url}")
        raw_content, fetched_title = fetch_content(url, content_type)

        if not title and fetched_title: # If user didn't provide a title, use the fetched one
            title = fetched_title
        elif not title and not fetched_title: # Default if no title from user or fetch for URL
            title = "Untitled Web Content"

        if not raw_content:
            return redirect(url_for('index', message=f"Error: Could not fetch content from {url}."))

    elif text:
        content_type = "direct-text"
        raw_content = text
        if not title: # If user didn't provide a title for direct text
            title = f"Direct Text {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print("Processing direct text content.")
    
    else:
        return redirect(url_for('index', message="Error: No URL or text content provided."))

    if not title: # Final fallback for title if somehow still empty
        title = "Untitled"

    if raw_content:
        markdown_content_with_frontmatter = process_content_to_markdown(
            raw_content,
            content_type,
            source_url,
            title, # This is the initial title for frontmatter
            tags_list,
            purpose
        )

        if markdown_content_with_frontmatter:
            temp_id = uuid.uuid4().hex
            staging_filepath = os.path.join(STAGING_DIR, f"{temp_id}.md")

            try:
                with open(staging_filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown_content_with_frontmatter)
                
                # Store details needed for the review and final save process
                session['staged_item_details'] = {
                    'temp_id': temp_id,
                    'content_type': content_type,
                    'source_url': source_url,
                    # The initial title, tags, purpose are now in the staging file's frontmatter.
                    # The review step will read them from there.
                }
                print(f"Content staged to: {staging_filepath} with temp_id: {temp_id}")
                return redirect(url_for('review_item', temp_id=temp_id))
            except IOError as e:
                print(f"Error saving staging file {staging_filepath}: {e}")
                return redirect(url_for('index', message=f"Error: Could not save staged content. {e}"))
        else:
            return redirect(url_for('index', message="Error: Could not process content to markdown."))
    
    return redirect(url_for('index', message="Error: No content provided or processed."))


@app.route('/browse')
def browse():
    # This will be updated later in Phase 3 to read from kb_index.json
    knowledge_files = []
    # Corrected BASE_KNOWLEDGE_DIR reference for browsing
    # It should be the one defined in storage.py or a consistent one.
    # For now, this is a placeholder until kb_utils and index are used.
    actual_kb_dir = os.path.join(PROJECT_ROOT, 'knowledge_base')

    if os.path.exists(actual_kb_dir):
        for root_dir_name in ['articles', 'videos', 'direct_text']:
            current_dir_path = os.path.join(actual_kb_dir, root_dir_name)
            if os.path.exists(current_dir_path):
                for file_name in os.listdir(current_dir_path):
                    if file_name.endswith('.md'):
                        relative_path = os.path.join(root_dir_name, file_name)
                        knowledge_files.append(relative_path)
    else:
        print(f"Knowledge base directory not found: {actual_kb_dir}")
        
    return render_template('browse.html', files=knowledge_files)


@app.route('/view/<path:filename>')
def view_file(filename):
    # Construct full path carefully, assuming filename might be "category/actualfile.md"
    actual_kb_dir = os.path.join(PROJECT_ROOT, 'knowledge_base')
    file_path = os.path.join(actual_kb_dir, filename)
    
    if not os.path.abspath(file_path).startswith(os.path.abspath(actual_kb_dir)):
        return "Error: Access denied.", 403

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return "File not found", 404

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            front_matter_str = parts[1]
            markdown_body = parts[2]
            metadata = yaml.safe_load(front_matter_str)
        else:
            markdown_body = content
            metadata = {}
    except Exception as e:
        print(f"Error parsing frontmatter for {filename}: {e}")
        markdown_body = content
        metadata = {}
        
    html_content = markdown.markdown(markdown_body, extensions=['fenced_code', 'tables'])

    return render_template('view.html', content=html_content, metadata=metadata, filename=filename)

# --- Placeholder routes for Phase 2 --- 
@app.route('/review_item/<temp_id>', methods=['GET'])
def review_item(temp_id):
    # TODO: Implement in Phase 2
    # - Construct staging_filepath from STAGING_DIR and temp_id
    # - Check if file exists
    # - Read content, parse frontmatter (title, tags, purpose)
    # - Pass to review_item.html template
    staged_item_info = session.get('staged_item_details', {})
    if not staged_item_info or staged_item_info.get('temp_id') != temp_id:
        return redirect(url_for('index', message='Error: Staged item not found or session expired.'))

    staging_filepath = os.path.join(STAGING_DIR, f"{temp_id}.md")
    if not os.path.exists(staging_filepath):
        return redirect(url_for('index', message=f'Error: Staged file {temp_id}.md not found.'))

    with open(staging_filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            front_matter_str = parts[1]
            markdown_body = parts[2]
            metadata = yaml.safe_load(front_matter_str)
        else:
            # Should not happen if processor.py always adds frontmatter
            markdown_body = content 
            metadata = {}
    except Exception as e:
        return redirect(url_for('index', message=f'Error: Could not parse staged file {temp_id}.md. {e}'))

    # Pass necessary data to the template
    return render_template('review_item.html', 
                           temp_id=temp_id, 
                           title=metadata.get('title', 'Untitled'), 
                           tags=', '.join(metadata.get('user_tags', [])), 
                           purpose=metadata.get('user_purpose', ''), 
                           markdown_content=markdown_body, # Pass the body for display
                           full_markdown_for_editing=content # Or pass full content if textarea edits full doc
                           )

@app.route('/save_item/<temp_id>', methods=['POST'])
def save_item(temp_id):
    # TODO: Implement in Phase 2
    # - Get temp_id from URL, edited title, tags, purpose from form
    # - Validate session and temp_id match
    # - Read original staging_filepath
    # - Update frontmatter in the content string with new values
    # - Call kb_utils.get_next_sequence_number()
    # - Generate final filename (seq_no + slug from new_title)
    # - Call storage.save_to_knowledge_base() with new filename and updated content
    # - Call kb_utils.add_to_index() with all metadata
    # - Delete staging file
    # - Clear session['staged_item_details']
    # - Redirect to browse with success message
    return f"Placeholder: Save item {temp_id} - To be implemented in Phase 2"

@app.route('/discard_item/<temp_id>', methods=['POST'])
def discard_item(temp_id):
    # TODO: Implement in Phase 2
    # - Validate session and temp_id match
    # - Delete staging_filepath
    # - Clear session['staged_item_details']
    # - Redirect to index with a message
    return f"Placeholder: Discard item {temp_id} - To be implemented in Phase 2"

if __name__ == '__main__':
    app.run(debug=True, port=3000)
