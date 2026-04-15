# memory.py — Stores and retrieves last 5 strategies
 
import json
import os
 
MEMORY_FILE = "core/memory.json"
MAX_ENTRIES = 5
 
 
def _load() -> list:
    """Load memory from file. Return empty list if file doesn't exist."""
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)
 
 
def _save(data: list):
    """Save memory list to file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
 
 
def save_memory(strategy: dict):
    """
    Input:  strategy (dict)
    Saves to memory. Removes oldest if more than 5 entries.
    """
    data = _load()
    data.append(strategy)
 
    # Keep only last 5
    if len(data) > MAX_ENTRIES:
        data = data[-MAX_ENTRIES:]
 
    _save(data)
 
 
def get_memory() -> list:
    """
    Output: list of stored strategies, latest first.
    """
    data = _load()
    return list(reversed(data))
 