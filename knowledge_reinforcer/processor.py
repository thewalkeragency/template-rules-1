import markdownify
import yaml
from datetime import datetime

def process_content_to_markdown(raw_content, content_type, source_url, title, tags, purpose):
    markdown_body = ""
    if content_type == "web-article":
        markdown_body = markdownify.markdownify(raw_content, heading_style="ATX")
    elif content_type == "youtube-video":
        markdown_body = raw_content # Transcript is already text
    elif content_type == "direct-text":
        markdown_body = raw_content

    # Create YAML front matter
    metadata = {
        "title": title,
        "source_url": source_url if source_url else "N/A",
        "source_type": content_type,
        "date_extracted": datetime.now().isoformat(),
        "user_tags": tags,
        "user_purpose": purpose
    }

    front_matter = f"---\n{yaml.dump(metadata, sort_keys=False)}---\n\n"

    return front_matter + markdown_body
