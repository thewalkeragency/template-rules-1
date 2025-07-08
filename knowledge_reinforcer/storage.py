import os

BASE_KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')

def save_to_knowledge_base(filename, content, content_type):
    """
    Saves content to a file within a categorized subdirectory of the knowledge base.
    
    The target subdirectory is determined by the content type: "web-article" (articles), "youtube-video" (videos), "direct-text" (direct_text), or defaults to the base knowledge directory for other types. Creates the directory if it does not exist.
    
    Parameters:
        filename (str): Name of the file to save.
        content (str): Content to be written to the file.
        content_type (str): Type of content, used to determine the storage subdirectory.
    
    Returns:
        str or None: The full file path if the content was saved successfully, or None if an error occurred.
    """
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
        return file_path
    except IOError as e:
        print(f"Error saving file {file_path}: {e}")
        return None

