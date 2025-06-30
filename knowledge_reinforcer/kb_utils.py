import os
import json
from datetime import datetime

# Determine paths relative to this file's location
# Assumes kb_utils.py is in knowledge_reinforcer/
# and knowledge_base/ is a sibling to knowledge_reinforcer/
# This was the structure indicated by BASE_KNOWLEDGE_DIR in storage.py
# BASE_KNOWLEDGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')

# Let's adjust paths to be relative to the project root if this script is called from web_app.py
# or make them absolute based on a known structure.
# For simplicity and consistency with storage.py, let's assume utils are called from within knowledge_reinforcer module context
# and knowledge_base is one level up from the module directory.

# Path to the directory containing the current script (kb_utils.py)
# Expected to be .../template-rules-1/knowledge_reinforcer/
CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the project root (template-rules-1/)
PROJECT_ROOT = os.path.dirname(CURRENT_SCRIPT_DIR)

# Paths to knowledge_base files
KB_BASE_DIR = os.path.join(PROJECT_ROOT, 'knowledge_base')
COUNTER_FILE = os.path.join(KB_BASE_DIR, 'kb_counter.txt')
INDEX_FILE = os.path.join(KB_BASE_DIR, 'kb_index.json')


def get_next_sequence_number():
    """
    Reads the counter file, increments the number, saves it back, and returns the new number.
    Simple file-based counter, not designed for high concurrency.
    """
    try:
        if not os.path.exists(KB_BASE_DIR):
            os.makedirs(KB_BASE_DIR)
            print(f"Warning: Knowledge base directory created at {KB_BASE_DIR}")

        if not os.path.exists(COUNTER_FILE):
            # Initialize counter file if it doesn't exist
            with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
                f.write('0')
            current_number = 0
        else:
            with open(COUNTER_FILE, 'r+', encoding='utf-8') as f:
                content = f.read().strip()
                current_number = int(content) if content else 0

        next_number = current_number + 1

        # Re-open in write mode to overwrite, or seek and truncate
        with open(COUNTER_FILE, 'w', encoding='utf-8') as f:
            f.write(str(next_number))

        return next_number
    except Exception as e:
        print(f"Error managing sequence counter: {e}")
        # Fallback or re-raise, for now, let's return a timestamp-based fallback for uniqueness if critical
        # Or simply re-raise after logging. For this app, erroring out might be better.
        raise Exception(f"Critical error in get_next_sequence_number: {e}")


def read_index():
    """
    Reads and returns the list of metadata from kb_index.json.
    Returns an empty list if the file doesn't exist or is empty/invalid.
    """
    try:
        if not os.path.exists(INDEX_FILE):
            # Initialize index file if it doesn't exist
            with open(INDEX_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []

        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content: # File is empty
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"Warning: {INDEX_FILE} contains invalid JSON. Returning empty list.")
        return [] # Or handle error more gracefully, maybe backup old file
    except Exception as e:
        print(f"Error reading index file: {e}")
        raise Exception(f"Critical error in read_index: {e}")

def add_to_index(item_metadata):
    """
    Appends new item metadata to kb_index.json.
    item_metadata should be a dictionary.
    """
    if not isinstance(item_metadata, dict):
        raise ValueError("item_metadata must be a dictionary.")

    all_items = read_index() # Handles file creation and empty cases

    # Add a 'date_saved' timestamp if not already present
    if 'date_saved' not in item_metadata:
        item_metadata['date_saved'] = datetime.now().isoformat()

    all_items.append(item_metadata)

    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_items, f, indent=2) # indent for human readability
    except Exception as e:
        print(f"Error writing to index file: {e}")
        # Consider how to handle this - rollback?
        raise Exception(f"Critical error in add_to_index: {e}")

if __name__ == '__main__':
    # Simple test cases (run this file directly to test)
    print(f"Counter file: {COUNTER_FILE}")
    print(f"Index file: {INDEX_FILE}")

    # Ensure knowledge_base directory exists for testing
    if not os.path.exists(KB_BASE_DIR):
        os.makedirs(KB_BASE_DIR)
        print(f"Created directory: {KB_BASE_DIR}")

    # Test counter
    print("Testing sequence counter...")
    initial_seq = get_next_sequence_number() -1 # to get current value from file
    print(f"Initial number (from file or 0 if new): {initial_seq}")
    num1 = get_next_sequence_number()
    print(f"Next sequence number: {num1}")
    num2 = get_next_sequence_number()
    print(f"Next sequence number: {num2}")

    # Reset counter for consistent testing if needed (manual step or add function)
    # with open(COUNTER_FILE, 'w') as f:
    #     f.write(str(num2 - 2))
    # print(f"Reset counter to {num2-2}")


    # Test index
    print("\nTesting index functions...")
    # Clear index for clean test
    with open(INDEX_FILE, 'w') as f:
        json.dump([], f)
    print("Cleared index file for test.")

    print(f"Initial index: {read_index()}")

    item1 = {
      "seq_no": num1, # Use a real sequence number
      "filename": f"{num1:04d}-test-item1.md",
      "title": "Test Item 1",
      "date_extracted": datetime.now().isoformat(),
      "tags": ["test", "python"],
      "purpose": "Testing the index function.",
      "source_type": "direct-text",
      "source_url": "N/A"
    }
    add_to_index(item1)
    print(f"Index after adding item 1: {read_index()}")

    item2 = {
      "seq_no": num2, # Use a real sequence number
      "filename": f"{num2:04d}-another-test.md",
      "title": "Another Test Item",
      "date_extracted": datetime.now().isoformat(), # Should be from original processing
      "tags": ["test", "example"],
      "purpose": "More index testing.",
      "source_type": "web-article",
      "source_url": "http://example.com/article"
    }
    add_to_index(item2)
    updated_index = read_index()
    print(f"Index after adding item 2 (length {len(updated_index)}):")
    for item in updated_index:
        print(item)

    print("\nKB Utils tests complete.")
