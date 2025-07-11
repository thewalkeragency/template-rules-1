from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
import yaml
import re

# Add the parent directory to the sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knowledge_reinforcer.fetcher import fetch_content
from knowledge_reinforcer.processor import process_content_to_markdown
from knowledge_reinforcer.storage import save_to_knowledge_base, BASE_KNOWLEDGE_DIR

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_very_dev_default_secret_key_for_flask_app_kb_project_v2') # Unique default key

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
            filename_base = re.sub(r'[^a-zA-Z0-9_]', '', title.replace(' ', '_'))[:50] or "untitled"
            filename = f"{filename_base}_{datetime.now().strftime('%Y%m%2d_%H%M%S')}.md"
            save_to_knowledge_base(filename, markdown_content, content_type)
            flash("Content saved successfully!", 'success')
            return redirect(url_for('index'))
        else:
            return "Error: Could not process content to markdown.", 400
    return "Error: No content provided.", 400

@app.route('/browse')
def browse():
    knowledge_items = []
    for root, _, files in os.walk(BASE_KNOWLEDGE_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata = {}
                parts = content.split('---\n', 2)
                if len(parts) > 1:
                    try:
                        metadata = yaml.safe_load(parts[1])
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML in {file}: {e}")

                title = metadata.get('title', file.replace('.md', ''))
                date_extracted_str = metadata.get('date_extracted')
                date_extracted = datetime.fromisoformat(date_extracted_str) if date_extracted_str else datetime.min

                relative_path = os.path.relpath(file_path, BASE_KNOWLEDGE_DIR)
                knowledge_items.append({
                    'filename': relative_path,
                    'title': title,
                    'date': date_extracted
                })
    
    # Sort by date, newest first
    knowledge_items.sort(key=lambda x: x['date'], reverse=True)

    return render_template('browse.html', items=knowledge_items)

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

@app.route('/analyze_content', methods=['POST'])
def analyze_content():
    url = request.json.get('url')
    text = request.json.get('text')

    raw_content = None
    plain_text_content = ""

    if url:
        content_type = None
        if "youtube.com/watch" in url or "youtu.be/" in url:
            content_type = "youtube-video"
        else:
            content_type = "web-article"
        
        raw_content, _ = fetch_content(url, content_type)
        if raw_content:
            if content_type == "web-article":
                soup = BeautifulSoup(raw_content, 'html.parser')
                # Extract text from common content tags
                content_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']
                extracted_texts = []
                for tag in content_tags:
                    for element in soup.find_all(tag):
                        extracted_texts.append(element.get_text())
                plain_text_content = " ".join(extracted_texts)
            elif content_type == "youtube-video":
                plain_text_content = raw_content # Transcript is already plain text
    elif text:
        plain_text_content = text

    if plain_text_content:
        from .processor import _clean_text
        plain_text_content = _clean_text(plain_text_content)
        # Generate summary (purpose) and keywords (tags)
        from .processor import _generate_summary, _extract_keywords
        auto_purpose = _generate_summary(plain_text_content)
        if auto_purpose:
            auto_purpose = "Relevant for AI coding: " + auto_purpose
        auto_tags = ', '.join(_extract_keywords(plain_text_content))
        print(f"Generated Purpose: {auto_purpose}")
        print(f"Generated Tags: {auto_tags}")
        return jsonify({'purpose': auto_purpose, 'tags': auto_tags})
    
    return jsonify({'purpose': '', 'tags': ''})

if __name__ == '__main__':
    app.run(debug=True, port=3000)