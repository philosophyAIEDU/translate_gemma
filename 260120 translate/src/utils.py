import json
import os
from typing import List, Dict, Any

def load_languages(filepath: str) -> Dict[str, str]:
    """Load supported languages from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def chunk_text(text: str, max_chars: int = 1000) -> List[str]:
    """Split text into chunks."""
    chunks = []
    current_chunk = ""
    words = text.split() 
    for word in words:
        if len(current_chunk) + len(word) + 1 > max_chars:
            chunks.append(current_chunk)
            current_chunk = word
        else:
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def save_history(record: Dict[str, Any], filepath: str):
    """Save a translation record to history."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                history = json.load(f)
            except (json.JSONDecodeError, ValueError):
                history = []
    else:
        history = []
    
    history.append(record)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_history(filepath: str) -> List[Dict[str, Any]]:
    """Load translation history."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []

def load_glossary(filepath: str) -> List[Dict[str, str]]:
    """Load glossary terms."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []

def save_glossary(glossary: List[Dict[str, str]], filepath: str):
    """Save glossary terms."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(glossary, f, ensure_ascii=False, indent=2)

def save_history_list(history: List[Dict[str, Any]], filepath: str):
    """Save the entire history list (used for clearing history)."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
