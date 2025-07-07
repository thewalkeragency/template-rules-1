import requests
from readability import Document
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def _get_youtube_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        video_id = parse_qs(parsed_url.query).get('v')
        if video_id:
            return video_id[0]
    elif parsed_url.hostname in ('youtu.be',):
        return parsed_url.path[1:]
    return None

def fetch_content(url, content_type):
    if content_type == "web-article":
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            doc = Document(response.text)
            return doc.content(), doc.title()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching web article from {url}: {e}")
            return None, None
    elif content_type == "youtube-video":
        video_id = _get_youtube_video_id(url)
        if not video_id:
            print(f"Invalid YouTube URL: {url}")
            return None, None
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript_list])
            # YouTubeTranscriptApi doesn't directly provide video title, so we'll try to fetch it
            # This is a best-effort attempt and might not always work reliably without YouTube Data API
            try:
                video_response = requests.get(f"https://www.youtube.com/watch?v={video_id}", timeout=5)
                video_response.raise_for_status()
                doc = Document(video_response.text)
                return transcript_text, doc.title()
            except requests.exceptions.RequestException:
                return transcript_text, f"YouTube Video Transcript ({video_id})"
        except Exception as e:
            print(f"Error fetching YouTube transcript for {url}: {e}")
            return None, None
    return None, None
