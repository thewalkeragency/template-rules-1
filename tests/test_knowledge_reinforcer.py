import pytest
import sys
import os
from unittest.mock import Mock
import requests # Added import
import tempfile
import shutil

# Add the parent directory to the sys.path to allow imports from knowledge_reinforcer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from knowledge_reinforcer.processor import _generate_summary, _extract_keywords
from knowledge_reinforcer.fetcher import fetch_content
from knowledge_reinforcer.web_app import app # Import the Flask app
from knowledge_reinforcer.storage import BASE_KNOWLEDGE_DIR, save_to_knowledge_base

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_knowledge_base(mocker):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # Patch BASE_KNOWLEDGE_DIR to point to the temporary directory
    mocker.patch('knowledge_reinforcer.storage.BASE_KNOWLEDGE_DIR', temp_dir)
    mocker.patch('knowledge_reinforcer.web_app.BASE_KNOWLEDGE_DIR', temp_dir)

    # Create subdirectories for testing
    os.makedirs(os.path.join(temp_dir, 'articles'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, 'direct_text'), exist_ok=True)

    # Create some dummy files
    with open(os.path.join(temp_dir, 'articles', 'test_article.md'), 'w') as f:
        f.write("---\ntitle: Test Article\n---\n\nContent of test article.")
    with open(os.path.join(temp_dir, 'direct_text', 'test_text.md'), 'w') as f:
        f.write("---\ntitle: Test Text\n---\n\nContent of test text.")

    yield temp_dir

    # Clean up the temporary directory after the test
    shutil.rmtree(temp_dir)

# Tests for _generate_summary
def test_generate_summary_basic():
    text = "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence."
    summary = _generate_summary(text, num_sentences=2)
    assert len(summary.split('.')) >= 2 # Check if at least two sentences are returned
    assert "first sentence" in summary or "second sentence" in summary or "third sentence" in summary or "fourth sentence" in summary

def test_generate_summary_empty_text():
    text = ""
    summary = _generate_summary(text)
    assert summary == ""

def test_generate_summary_fewer_sentences_than_requested():
    text = "Only one sentence."
    summary = _generate_summary(text, num_sentences=3)
    assert summary == "Only one sentence."

# Tests for _extract_keywords
def test_extract_keywords_basic():
    text = "Python is a high-level, interpreted programming language. It is widely used for web development and data analysis."
    keywords = _extract_keywords(text, num_keywords=3)
    assert len(keywords) <= 3
    assert "web development" in keywords or "data analysis" in keywords or "programming language" in keywords

def test_extract_keywords_empty_text():
    text = ""
    keywords = _extract_keywords(text)
    assert keywords == []

def test_extract_keywords_fewer_than_requested():
    text = "Simple text."
    keywords = _extract_keywords(text, num_keywords=5)
    assert len(keywords) <= 5
    assert "simple text" in keywords

# Tests for fetch_content
def test_fetch_content_web_article_success(mocker):
    mock_response = Mock()
    mock_response.text = "<html><body><h1>Test Title</h1><p>Test content.</p></body></html>"
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)
    
    # Mock the Document and its title method
    mock_document = Mock()
    mock_document.content.return_value = "Test content."
    mock_document.title.return_value = "Test Title"
    mocker.patch('knowledge_reinforcer.fetcher.Document', return_value=mock_document)

    content, title = fetch_content("http://example.com", "web-article")
    assert "Test content" in content
    assert title == "Test Title"

def test_fetch_content_web_article_failure(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException)

    content, title = fetch_content("http://example.com", "web-article")
    assert content is None
    assert title is None

def test_fetch_content_youtube_success(mocker):
    mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript', return_value=[{'text': 'video transcript'}])
    mock_response = Mock()
    mock_response.text = "<html><body><title>YouTube Video Title</title></body></html>"
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    content, title = fetch_content("https://www.youtube.com/watch?v=test_id", "youtube-video")
    assert "video transcript" in content
    assert title == "YouTube Video Title"

def test_fetch_content_youtube_invalid_url(mocker):
    content, title = fetch_content("https://www.youtube.com/invalid_url", "youtube-video")
    assert content is None
    assert title is None

def test_fetch_content_youtube_transcript_failure(mocker):
    mocker.patch('youtube_transcript_api.YouTubeTranscriptApi.get_transcript', side_effect=Exception)

    content, title = fetch_content("https://www.youtube.com/watch?v=test_id", "youtube-video")
    assert content is None
    assert title is None

# Tests for Flask web_app routes
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Knowledge Reinforcer" in response.data

def test_process_input_direct_text_success(client, mocker):
    mocker.patch('knowledge_reinforcer.web_app.save_to_knowledge_base')
    mocker.patch('knowledge_reinforcer.web_app.process_content_to_markdown', return_value="# Test Markdown")
    mocker.patch('knowledge_reinforcer.web_app.fetch_content', return_value=("raw content", "Test Title"))

    response = client.post('/process_input', data={
        'text': 'This is a test text.',
        'tags': 'test, example',
        'purpose': 'To test direct text input.'
    })
    assert response.status_code == 302 # Redirect
    with client.session_transaction() as session:
        assert '_flashes' in session
        assert session['_flashes'][0][1] == "Content saved successfully!"

def test_process_input_url_success(client, mocker):
    mocker.patch('knowledge_reinforcer.web_app.save_to_knowledge_base')
    mocker.patch('knowledge_reinforcer.web_app.process_content_to_markdown', return_value="# Test Markdown")
    mocker.patch('knowledge_reinforcer.web_app.fetch_content', return_value=("raw content", "Test Title"))

    response = client.post('/process_input', data={
        'url': 'http://example.com/article',
        'tags': 'web, article',
        'purpose': 'To test URL input.'
    })
    assert response.status_code == 302 # Redirect
    with client.session_transaction() as session:
        assert '_flashes' in session
        assert session['_flashes'][0][1] == "Content saved successfully!"

def test_process_input_no_content(client):
    response = client.post('/process_input', data={})
    assert response.status_code == 400
    assert b"Error: No content provided." in response.data

def test_process_input_fetch_failure(client, mocker):
    mocker.patch('knowledge_reinforcer.web_app.fetch_content', return_value=(None, None))

    response = client.post('/process_input', data={
        'url': 'http://example.com/nonexistent',
        'tags': 'fail',
        'purpose': 'Test fetch failure.'
    })
    assert response.status_code == 400
    assert b"Error: Could not fetch content from http://example.com/nonexistent." in response.data

def test_browse_route(client, temp_knowledge_base):
    response = client.get('/browse')
    assert response.status_code == 200
    assert b"Browse Knowledge Base" in response.data
    assert b"articles/test_article.md" in response.data
    assert b"direct_text/test_text.md" in response.data

def test_view_file_route_success(client, temp_knowledge_base):
    response = client.get('/view/articles/test_article.md')
    assert response.status_code == 200
    assert b"Content of test article." in response.data
    assert b"Test Article" in response.data # From YAML front matter

def test_view_file_route_not_found(client, temp_knowledge_base):
    response = client.get('/view/nonexistent_file.md')
    assert response.status_code == 404
    assert b"File not found" in response.data