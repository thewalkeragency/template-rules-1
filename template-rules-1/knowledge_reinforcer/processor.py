import markdownify
import yaml
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
from bs4 import BeautifulSoup
from rake_nltk import Rake
import re
from .nltk_setup import ensure_nltk_resources

ensure_nltk_resources()

def _clean_text(text):
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove emails
    text = re.sub(r'\S*@\S*\s?', '', text)
    # Remove special characters and numbers, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def _generate_summary(text, num_sentences=1):
    if not text:
        return ""

    # Tokenize sentences
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return " ".join(sentences) # Return all sentences if fewer than num_sentences

    # Tokenize words and remove stopwords
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Calculate word frequencies
    word_freq = defaultdict(int)
    for word in filtered_words:
        word_freq[word] += 1

    # Score sentences based on word frequencies
    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_scores[i] += word_freq[word]

    # Get top sentences
    ranked_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary_sentences_indices = sorted([idx for idx, _ in ranked_sentences[:num_sentences]])

    summary = " ".join([sentences[idx] for idx in summary_sentences_indices])
    return summary

def _extract_keywords(text, num_keywords=3):
    if not text:
        return []
    r = Rake(stopwords=nltk.corpus.stopwords.words('english'))
    r.extract_keywords_from_text(text)
    ranked_phrases = r.get_ranked_phrases()
    return ranked_phrases[:num_keywords]

def process_content_to_markdown(raw_content, content_type, source_url, title, tags, purpose):
    markdown_body = ""
    text_for_processing = "" # Use a consistent variable name for text used in summarization/keyword extraction

    if content_type == "web-article":
        markdown_body = markdownify.markdownify(raw_content, heading_style="ATX")
        text_for_processing = raw_content
    elif content_type == "youtube-video":
        markdown_body = raw_content # Transcript is already text
        text_for_processing = raw_content
    elif content_type == "direct-text":
        markdown_body = raw_content
        text_for_processing = _clean_text(raw_content)

    # Generate summary
    summary = _generate_summary(text_for_processing)

    # Extract keywords
    extracted_keywords = _extract_keywords(text_for_processing)

    # Create YAML front matter
    metadata = {
        "title": title,
        "source_url": source_url if source_url else "N/A",
        "source_type": content_type,
        "date_extracted": datetime.now().isoformat(),
        "user_tags": tags,
        "user_purpose": purpose,
        "summary": summary, # Add the generated summary
        "extracted_keywords": extracted_keywords # Add the extracted keywords
    }

    front_matter = f"---\n{yaml.dump(metadata, sort_keys=False)}---\n\n"

    return front_matter + markdown_body
