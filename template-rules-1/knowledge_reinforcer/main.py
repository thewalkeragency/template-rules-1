import argparse
import os
from datetime import datetime
from urllib.parse import urlparse
import re

from .fetcher import fetch_content
from .processor import process_content_to_markdown
from .storage import save_to_knowledge_base
from .nltk_setup import ensure_nltk_resources

def main():
    # Ensure NLTK resources are available
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
        markdown_content = process_content_to_markdown(
            raw_content,
            content_type,
            source_url,
            title,
            args.tags.split(',') if args.tags else [],
            args.purpose
        )
        if markdown_content:
            # Sanitize filename: replace non-alphanumeric with underscores, limit length
            filename_base = re.sub(r'[^a-zA-Z0-9_]', '', title.replace(' ', '_'))[:50] or "untitled"
            filename = f"{filename_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            save_to_knowledge_base(filename, markdown_content, content_type)
            print(f"Content saved to knowledge base as {filename}.")
        else:
            print(f"Could not process content to markdown.")

if __name__ == "__main__":
    main()
