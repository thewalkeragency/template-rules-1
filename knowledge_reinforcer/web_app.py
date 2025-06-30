from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os
import sys
import yaml
import uuid
import re # Import re directly
import markdown # For view_file, ensure it's imported where needed

# Path setup
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR) 
STAGING_DIR = os.path.join(CURRENT_SCRIPT_DIR, 'staging_area')

os.makedirs(STAGING_DIR, exist_ok=True)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from knowledge_reinforcer.fetcher import fetch_content
from knowledge_reinforcer.processor import process_content_to_markdown
from knowledge_reinforcer.storage import save_to_knowledge_base 
from knowledge_reinforcer import kb_utils # Import kb_utils

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_very_dev_default_secret_key_for_flask_app_kb_project_v2') # Unique default key

@app.route('/')
def index():
    message = request.args.get('message')
    # Clear any stale staged item from session when returning to index
    # This is a simple cleanup; a more robust system might track staging file timestamps
    if 'staged_item_details' in session:
        staged_item_id_to_clear = session['staged_item_details'].get('temp_id')
        if staged_item_id_to_clear:
            try:
                # Best effort to remove the physical file if session is cleared here
                # This path should only be hit if user navigates away from review without saving/discarding
                staging_filepath = os.path.join(STAGING_DIR, f"{staged_item_id_to_clear}.md")
                if os.path.exists(staging_filepath):
                     # print(f"Note: Stale session for {staged_item_id_to_clear} found on index load. File not deleted here.")
                     pass # Avoid deleting if user might have review page open in another tab.
                     # Deletion should be explicit via discard or implicit after save.
            except Exception as e:
                print(f"Error during stale session check for {staged_item_id_to_clear}: {e}")
        session.pop('staged_item_details', None)
    return render_template('index.html', message=message)

@app.route('/process_input', methods=['POST'])
def process_input():
    url = request.form.get('url')
    text = request.form.get('text')
    title_from_form = request.form.get('title', '').strip()
    tags_str = request.form.get('tags', '')
    purpose = request.form.get('purpose', '')

    tags_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

    content_type = None
    raw_content = None
    source_url = None
    title = title_from_form

    if url:
        source_url = url
        content_type = "youtube-video" if "youtube.com/watch" in url or "youtu.be/" in url else "web-article"
        raw_content, fetched_title = fetch_content(url, content_type)
        if not title and fetched_title: title = fetched_title
        elif not title and not fetched_title: title = "Untitled Web Content"
        if not raw_content: return redirect(url_for('index', message=f"Error: Could not fetch content from {url}."))
    elif text:
        content_type = "direct-text"
        raw_content = text
        if not title: title = f"Direct Text {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    else:
        return redirect(url_for('index', message="Error: No URL or text content provided."))

    if not title: title = "Untitled" # Final fallback

    if raw_content:
        markdown_content_with_frontmatter = process_content_to_markdown(
            raw_content, content_type, source_url, title, tags_list, purpose
        )
        if markdown_content_with_frontmatter:
            temp_id = uuid.uuid4().hex
            staging_filepath = os.path.join(STAGING_DIR, f"{temp_id}.md")
            try:
                with open(staging_filepath, 'w', encoding='utf-8') as f: f.write(markdown_content_with_frontmatter)
                session['staged_item_details'] = {
                    'temp_id': temp_id, 
                    'content_type': content_type, 
                    'source_url': source_url,
                    # date_extracted is now part of the frontmatter in the staging file.
                }
                return redirect(url_for('review_item', temp_id=temp_id))
            except IOError as e:
                return redirect(url_for('index', message=f"Error: Could not save staged content. {e}"))
        else:
            return redirect(url_for('index', message="Error: Could not process content to markdown."))
    return redirect(url_for('index', message="Error: No content processed."))

@app.route('/review_item/<temp_id>', methods=['GET'])
def review_item(temp_id):
    staged_item_info_session = session.get('staged_item_details', {})
    if not staged_item_info_session or staged_item_info_session.get('temp_id') != temp_id:
        return redirect(url_for('index', message='Error: Staged item not found or session expired.'))

    staging_filepath = os.path.join(STAGING_DIR, f"{temp_id}.md")
    if not os.path.exists(staging_filepath):
        session.pop('staged_item_details', None) 
        return redirect(url_for('index', message=f'Error: Staged file {temp_id}.md not found.'))

    with open(staging_filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    try:
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            front_matter_str = parts[1]; markdown_body = parts[2]
            metadata = yaml.safe_load(front_matter_str)
        else: 
            session.pop('staged_item_details', None)
            os.remove(staging_filepath) # Clean up invalid file
            return redirect(url_for('index', message=f'Error: Invalid content in staged file {temp_id}.md (missing frontmatter).'))
    except Exception as e:
        session.pop('staged_item_details', None)
        try: os.remove(staging_filepath) # Clean up problematic file
        except: pass
        return redirect(url_for('index', message=f'Error: Could not parse staged file {temp_id}.md. {e}'))

    return render_template('review_item.html',
                           temp_id=temp_id, title=metadata.get('title', 'Untitled'),
                           tags=', '.join(metadata.get('user_tags', [])),
                           purpose=metadata.get('user_purpose', ''),
                           markdown_content=markdown_body,
                           full_markdown_for_editing=content 
                           )

@app.route('/save_item/<temp_id>', methods=['POST'])
def save_item(temp_id):
    staged_item_info_session = session.get('staged_item_details', {})
    if not staged_item_info_session or staged_item_info_session.get('temp_id') != temp_id:
        return redirect(url_for('index', message='Error: Staged item not found or session expired for saving.'))

    staging_filepath = os.path.join(STAGING_DIR, f"{temp_id}.md")
    if not os.path.exists(staging_filepath):
        session.pop('staged_item_details', None) 
        return redirect(url_for('index', message=f'Error: Staged file {temp_id}.md not found for saving.'))

    edited_title = request.form.get('title', 'Untitled').strip()
    edited_tags_str = request.form.get('tags', '')
    edited_purpose = request.form.get('purpose', '').strip()
    
    edited_tags_list = [tag.strip() for tag in edited_tags_str.split(',') if tag.strip()] if edited_tags_str else []

    if not edited_title: edited_title = "Untitled KB Item"

    with open(staging_filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            front_matter_str = parts[1]
            markdown_body = parts[2] 
            metadata_from_file = yaml.safe_load(front_matter_str)
        else:
            return redirect(url_for('index', message=f'Error: Invalid content in staged file {temp_id}.md (missing frontmatter).'))

        metadata_to_save = metadata_from_file.copy()
        metadata_to_save['title'] = edited_title
        metadata_to_save['user_tags'] = edited_tags_list
        metadata_to_save['user_purpose'] = edited_purpose
        if 'date_extracted' not in metadata_to_save or not metadata_to_save['date_extracted']:
             metadata_to_save['date_extracted'] = datetime.now().isoformat() 

        updated_front_matter_str = yaml.dump(metadata_to_save, sort_keys=False, allow_unicode=True)
        updated_markdown_content = f"---\n{updated_front_matter_str}---\n\n{markdown_body}"

        seq_no = kb_utils.get_next_sequence_number()
        
        slug = re.sub(r'[^a-z0-9_]+', '-', edited_title.lower()).strip('-')
        slug = re.sub(r'--+', '-', slug) 
        slug = (slug[:50] or "untitled").strip('-') # Ensure not empty and strip again
        if not slug: slug = "untitled" 
        final_filename = f"{seq_no:04d}-{slug}.md"

        content_type = staged_item_info_session.get('content_type')
        save_to_knowledge_base(final_filename, updated_markdown_content, content_type)

        index_metadata_for_json = {
            "seq_no": seq_no,
            "filename": final_filename,
            "title": edited_title,
            "date_extracted": metadata_to_save.get('date_extracted'),
            "tags": edited_tags_list,
            "purpose": edited_purpose,
            "source_type": content_type,
            "source_url": metadata_to_save.get('source_url', 'N/A')
        }
        kb_utils.add_to_index(index_metadata_for_json)

        os.remove(staging_filepath)
        session.pop('staged_item_details', None)
        
        return redirect(url_for('browse', message=f"Item '{edited_title}' saved successfully as {final_filename}!"))

    except Exception as e:
        print(f"CRITICAL Error during save_item for {temp_id}: {e}")
        try:
            if os.path.exists(staging_filepath):
                os.remove(staging_filepath)
        except Exception as cleanup_e:
            print(f"Error cleaning up staging file {staging_filepath} after save_item error: {cleanup_e}")
        if 'staged_item_details' in session: session.pop('staged_item_details', None)
        return redirect(url_for('index', message=f"Error saving item: {e}. Please check logs."))

@app.route('/discard_item/<temp_id>', methods=['POST'])
def discard_item(temp_id):
    staged_item_info_session = session.get('staged_item_details', {})
    if not staged_item_info_session or staged_item_info_session.get('temp_id') != temp_id:
        return redirect(url_for('index', message='Error: Staged item not found or session expired for discarding.'))

    staging_filepath = os.path.join(STAGING_DIR, f"{temp_id}.md")
    message_to_user = f"Item {temp_id} discarded."
    if os.path.exists(staging_filepath):
        try:
            os.remove(staging_filepath)
            print(f"Discarded staging file: {staging_filepath}")
        except OSError as e:
            print(f"Error deleting staging file {staging_filepath}: {e}")
            message_to_user = f"Error discarding item {temp_id}: {e}. File may still exist."
    else:
        print(f"Staging file {staging_filepath} not found for discard, perhaps already processed or removed.")
        message_to_user = f"Staged file {temp_id}.md already removed or not found."
    
    session.pop('staged_item_details', None)
    return redirect(url_for('index', message=message_to_user))

@app.route('/browse')
def browse():
    # This will be updated in Phase 3 to use kb_utils.read_index()
    actual_kb_dir = os.path.join(PROJECT_ROOT, 'knowledge_base')
    knowledge_items_for_template = [] 
    message = request.args.get('message')

    # Placeholder: Read actual files for now until index is used for browsing
    if os.path.exists(actual_kb_dir):
        for root_dir_name in ['articles', 'videos', 'direct_text']:
            current_dir_path = os.path.join(actual_kb_dir, root_dir_name)
            if os.path.exists(current_dir_path):
                for file_name in os.listdir(current_dir_path):
                    if file_name.endswith('.md'):
                        # For this placeholder, we don't have easy access to title without parsing each file
                        # So we'll just pass filename and a constructed path for linking
                        display_name = f"{root_dir_name}/{file_name}"
                        # Path for url_for('view_file', filename=path_for_view)
                        path_for_view = os.path.join(root_dir_name, file_name).replace(os.sep, '/')
                        knowledge_items_for_template.append({'filename_for_view': path_for_view, 'display_title': display_name})
    else:
        print(f"Knowledge base directory not found: {actual_kb_dir}")
        
    return render_template('browse.html', items=knowledge_items_for_template, message=message)

@app.route('/view/<path:filename>')
def view_file(filename):
    actual_kb_dir = os.path.join(PROJECT_ROOT, 'knowledge_base')
    file_path = os.path.join(actual_kb_dir, filename) 
    
    if not os.path.abspath(file_path).startswith(os.path.abspath(actual_kb_dir)):
        return "Error: Access denied to this path.", 403
        
    if not os.path.exists(file__path) or not os.path.isfile(file_path):
        return f"File not found: {file_path}", 404
        
    with open(file_path, 'r', encoding='utf-8') as f: content = f.read()
    try:
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            front_matter_str = parts[1]; markdown_body = parts[2]
            metadata = yaml.safe_load(front_matter_str)
        else:
            markdown_body = content; metadata = {}
    except Exception as e:
        markdown_body = content; metadata = {}; print(f"Error parsing frontmatter for {filename}: {e}")
        
    html_content = markdown.markdown(markdown_body, extensions=['fenced_code', 'tables'])
    return render_template('view.html', content=html_content, metadata=metadata, filename=filename)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
