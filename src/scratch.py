import os
import httpx
from dotenv import load_dotenv
from json import dump, load
from pathlib import Path
CACHE_FILE = Path(__file__).resolve().parent/"cache.json"
cache = {}
try:
    with open(CACHE_FILE, "r") as f:
        cache = load(f)
except FileNotFoundError:
    print("No cached file. Making one now.")

def main():
    load_dotenv()
    url = "https://api.apilayer.net/mediastack/v1/news"
    params = {
            "access_key": os.getenv("API_KEY"),
            "countries": "us",
            "limit": "100",
            "offset": "0"
            }

    r = httpx.get(url, params=params)
    with open(CACHE_FILE, "w") as f:
        dump(r.json(), f, indent=2)
    for i in range(len(r.json().get("data"))):
        curr = r.json().get("data")[i]
        print(f"Source: {i + 1}")
        print(f"  Author = {curr.get("author")}")
        print(f"  Title = {curr.get("title")}")
        print(f"  Description = {curr.get("description")}")
        print(f"  Link = {curr.get("url")}\n")

if __name__ == "__main__":
    main()
