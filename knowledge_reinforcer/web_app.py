from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import sys
import yaml

# Add the parent directory to the sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knowledge_reinforcer.fetcher import fetch_content
from knowledge_reinforcer.processor import process_content_to_markdown
from knowledge_reinforcer.storage import save_to_knowledge_base, BASE_KNOWLEDGE_DIR

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    url = request.form.get('url')
    text = request.form.get('text')
    tags = request.form.get('tags', '')
    purpose = request.form.get('purpose', '')

    content_type = None
    raw_content = None
    source_url = None
    title = "Untitled"

    if url:
        source_url = url
        if "youtube.com/watch" in url or "youtu.be/" in url:
            content_type = "youtube-video"
        else:
            content_type = "web-article"
        
        raw_content, fetched_title = fetch_content(url, content_type)
        if fetched_title:
            title = fetched_title
        
        if not raw_content:
            return f"Error: Could not fetch content from {url}.", 400

    elif text:
        content_type = "direct-text"
        raw_content = text
        title = f"Direct Text - {datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if raw_content:
        markdown_content = process_content_to_markdown(
            raw_content,
            content_type,
            source_url,
            title,
            tags.split(',') if tags else [],
            purpose
        )
        if markdown_content:
            from knowledge_reinforcer.main import re # Import re here to avoid circular dependency
            filename_base = re.sub(r'[^a-zA-Z0-9_]', '', title.replace(' ', '_'))[:50] or "untitled"
            filename = f"{filename_base}_{datetime.now().strftime('%Y%m%2d_%H%M%S')}.md"
            save_to_knowledge_base(filename, markdown_content, content_type)
            return redirect(url_for('index', message="Content saved successfully!"))
        else:
            return "Error: Could not process content to markdown.", 400
    return "Error: No content provided.", 400

@app.route('/browse')
def browse():
    knowledge_files = []
    for root, _, files in os.walk(BASE_KNOWLEDGE_DIR):
        for file in files:
            if file.endswith('.md'):
                relative_path = os.path.relpath(os.path.join(root, file), BASE_KNOWLEDGE_DIR)
                knowledge_files.append(relative_path)
    return render_template('browse.html', files=knowledge_files)

@app.route('/view/<path:filename>')
def view_file(filename):
    file_path = os.path.join(BASE_KNOWLEDGE_DIR, filename)
    if not os.path.exists(file_path):
        return "File not found", 404
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Separate YAML front matter from content
    parts = content.split('---\n', 2)
    if len(parts) > 2:
        front_matter_str = parts[1]
        markdown_body = parts[2]
        metadata = yaml.safe_load(front_matter_str)
    else:
        markdown_body = content
        metadata = {}

    # Convert markdown body to HTML for display
    import markdown # This will need to be installed
    html_content = markdown.markdown(markdown_body)

    return render_template('view.html', content=html_content, metadata=metadata, filename=filename)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
