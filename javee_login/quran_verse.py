import requests
import json
import os
from datetime import datetime
import sys

# Constants
API_URL = "http://api.alquran.cloud/v1/ayah/random"
CACHE_FILE = "verse_cache.json"

def fetch_verse():
    """Fetch a random Quranic verse from the API."""
    print("Attempting to fetch verse from API...")
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Raw API response:", json.dumps(data, indent=2))
        verse_data = data.get("data", {})
        if not verse_data:
            print("Error: No 'data' in API response.")
            return None
        return {
            "verse_number": verse_data.get("number", 0),
            "text": verse_data.get("text", "No text available"),
            "surah_name": verse_data.get("surah", {}).get("name", " Unknown"),
            "surah_number": verse_data.get("surah", {}).get("number", 0),
            "timestamp": datetime.now().isoformat()
        }
    except requests.RequestException as e:
        print(f"Error fetching verse: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing API response: {e}")
        return None

def load_cached_verse():
    """Load the cached verse from the JSON file."""
    if not os.path.exists(CACHE_FILE):
        print(f"Cache file {CACHE_FILE} does not exist.")
        return None
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading cache file: {e}")
        return None

def save_verse(verse):
    """Save the verse to the JSON file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(verse, f, indent=4)
        print(f"Saved verse to {CACHE_FILE}")
    except IOError as e:
        print(f"Error saving cache file: {e}")

def is_new_day(timestamp):
    """Check if a new day has passed since the timestamp."""
    try:
        last_date = datetime.fromisoformat(timestamp)
        return datetime.now().date() > last_date.date()
    except ValueError as e:
        print(f"Error parsing timestamp: {e}")
        return True

def get_daily_verse():
    """Get the daily verse, fetching a new one if needed."""
    cached_verse = load_cached_verse()
    if cached_verse and "timestamp" in cached_verse and not is_new_day(cached_verse["timestamp"]):
        print("Using cached verse.")
        return cached_verse
    else:
        print("Fetching new verse...")
        new_verse = fetch_verse()
        if new_verse:
            save_verse(new_verse)
            return new_verse
        print("Falling back to cached verse or default.")
        return cached_verse or {
            "text": "Unable to fetch verse.",
            "surah_name": "",
            "surah_number": 0,
            "verse_number": 0,
            "timestamp": datetime.now().isoformat()
        }

def display_verse(verse):
    """Display the verse in a formatted way."""
    print("-" * 50)
    print(f"Surah {verse['surah_name']} ({verse['surah_number']}:{verse['verse_number']})")
    print(f"Verse: {verse['text']}")
    print(f"Last updated: {verse['timestamp']}")
    print("-" * 50)

def main():
    """Main function to run the daily verse application."""
    print("Starting Daily Quranic Verse Application")
    print(f"Python version: {sys.version}")
    print(f"Running from: {os.getcwd()}")
    verse = get_daily_verse()
    display_verse(verse)

if __name__ == "__main__":
    main()