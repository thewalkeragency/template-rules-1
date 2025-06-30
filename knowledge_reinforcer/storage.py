import os

BASE_KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')

def save_to_knowledge_base(filename, content, content_type):
    target_dir = ""
    if content_type == "web-article":
        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, 'articles')
    elif content_type == "youtube-video":
        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, 'videos')
    elif content_type == "direct-text":
        target_dir = os.path.join(BASE_KNOWLEDGE_DIR, 'direct_text')
    else:
        target_dir = BASE_KNOWLEDGE_DIR # Fallback

    os.makedirs(target_dir, exist_ok=True)
    file_path = os.path.join(target_dir, filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved: {file_path}")
    except IOError as e:
        print(f"Error saving file {file_path}: {e}")

