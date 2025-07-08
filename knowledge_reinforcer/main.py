import argparse
import os
from datetime import datetime
from urllib.parse import urlparse
import re

from .fetcher import fetch_content
from .processor import process_content_to_markdown
from .storage import save_to_knowledge_base, BASE_KNOWLEDGE_DIR # Import BASE_KNOWLEDGE_DIR
from .nltk_setup import ensure_nltk_resources
from .kb_utils import add_to_index, get_next_sequence_number # Import kb_utils functions

def main():
    # Ensure NLTK resources are available
    """
    Runs the command-line interface for extracting, processing, and storing content from a URL or direct text into a structured markdown knowledge base with metadata indexing.
    
    This function parses CLI arguments, fetches content from a web page, YouTube video, or direct text input, processes it into markdown, saves it in an organized directory structure, and updates the knowledge base index with relevant metadata. Supports both CLI and optional web interface modes. Provides user feedback and handles errors gracefully.
    """
    ensure_nltk_resources()

    parser = argparse.ArgumentParser(description="Knowledge Reinforcer: Extracts content from various sources and stores it as structured markdown.")
    parser.add_argument("--url", type=str, help="The URL (web page or YouTube video) to extract content from.")
    parser.add_argument("--text", type=str, help="Direct text content to store (optional).")
    parser.add_argument("--tags", type=str, default="", help="Comma-separated tags for the content (e.g., 'AI,NLP,Design Patterns').")
    parser.add_argument("--purpose", type=str, default="", help="A brief statement on why this information is relevant for AI coding (e.g., 'New design pattern', 'Best practice for secure APIs').")
    parser.add_argument("--web", action="store_true", help="Run the web interface.")

    args = parser.parse_args()

    if args.web:
        from . import web_app
        web_app.app.run(debug=True, port=3005)
        return

    if not args.url and not args.text:
        parser.error("Either --url or --text must be provided.")

    content_type = None
    raw_content = None
    source_url = None
    title = "Untitled"

    if args.url:
        source_url = args.url
        if "youtube.com/watch" in args.url or "youtu.be/" in args.url:
            content_type = "youtube-video"
        else:
            content_type = "web-article"
        
        print(f"Fetching content from: {args.url}")
        raw_content, fetched_title = fetch_content(args.url, content_type)
        if fetched_title: # Use fetched title if available
            title = fetched_title
        
        if not raw_content:
            print(f"Could not fetch content from {args.url}.")
            return

    elif args.text:
        content_type = "direct-text"
        raw_content = args.text
        title = f"Direct Text - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print("Storing direct text content.")

    if raw_content:
        markdown_content, extracted_metadata = process_content_to_markdown(
            raw_content,
            content_type,
            source_url,
            title,
            args.tags.split(',') if args.tags else [],
            args.purpose
        )
        if markdown_content:
            seq_no = get_next_sequence_number()

            # Sanitize filename: replace non-alphanumeric with underscores, limit length
            # Prepend sequence number for uniqueness and order
            filename_base = re.sub(r'[^a-zA-Z0-9_]', '', title.replace(' ', '_'))[:50] or "untitled"
            base_filename_with_seq = f"{seq_no:04d}_{filename_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

            # Determine the relative path for storage and for the index
            # storage.py saves it into subdirectories like 'articles/', 'videos/'
            # The filename in the index should reflect this relative path from BASE_KNOWLEDGE_DIR
            relative_subdir = ""
            if content_type == "web-article":
                relative_subdir = 'articles'
            elif content_type == "youtube-video":
                relative_subdir = 'videos'
            elif content_type == "direct-text":
                relative_subdir = 'direct_text'
            else:
                relative_subdir = 'misc' # Fallback, though storage.py uses BASE_KNOWLEDGE_DIR directly

            # Filename for storage (just the basename)
            storage_filename = base_filename_with_seq
            # Filename for index (relative path from knowledge_base root)
            index_filename = os.path.join(relative_subdir, base_filename_with_seq) if relative_subdir else base_filename_with_seq

            # Save the file
            saved_filepath = save_to_knowledge_base(storage_filename, markdown_content, content_type)

            if saved_filepath: # save_to_knowledge_base should return the full path or None
                print(f"Content saved to: {saved_filepath}")

                # Prepare metadata for the index
                index_item_metadata = {
                    "seq_no": seq_no,
                    "filename": index_filename, # Store relative path
                    "title": extracted_metadata.get("title"),
                    "source_url": extracted_metadata.get("source_url"),
                    "source_type": extracted_metadata.get("source_type"),
                    "date_extracted": extracted_metadata.get("date_extracted"),
                    "user_tags": extracted_metadata.get("user_tags"),
                    "user_purpose": extracted_metadata.get("user_purpose"),
                    "summary": extracted_metadata.get("summary"),
                    "extracted_keywords": extracted_metadata.get("extracted_keywords")
                    # kb_utils.add_to_index will add 'date_saved'
                }
                try:
                    add_to_index(index_item_metadata)
                    print(f"Successfully added '{title}' to knowledge base index.")
                except Exception as e:
                    print(f"Error adding to index: {e}")
            else:
                print(f"Failed to save content for '{title}'.")
        else:
            print(f"Could not process content to markdown.")

if __name__ == "__main__":
    main()
