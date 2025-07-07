import nltk
import os
import ssl

def ensure_nltk_resources():
    """
    Ensures that the required NLTK data packages are downloaded and accessible.
    This version specifically targets 'punkt_tab' as requested by the application's traceback.
    """
    # Define a consistent download directory within the project
    download_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Add the custom download directory to NLTK's data path
    if download_dir not in nltk.data.path:
        nltk.data.path.insert(0, download_dir)

    # --- SSL Certificate Workaround (for macOS and other systems) ---
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # --- Resource Verification and Download ---
    resources = {
        "punkt_tab": "tokenizers/punkt_tab",
        "stopwords": "corpora/stopwords"
    }

    for resource_id, resource_path in resources.items():
        try:
            nltk.data.find(resource_path)
            print(f"NLTK '{resource_id}' resource found at {nltk.data.find(resource_path)}.")
        except LookupError:
            print(f"NLTK '{resource_id}' resource not found. Downloading to {download_dir}...")
            nltk.download(resource_id, download_dir=download_dir)
            print(f"NLTK '{resource_id}' downloaded successfully.")
