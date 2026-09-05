import sys
import json
import urllib.request
import urllib.error


# fetch sys
def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e == 404:
            print(f"Error: GitHub user '{username}' not found.")
        else:
            print(f"Error: Failed to retrieve data. HTTP code: {e.code}")
        return None
    except urllib.error.URLError:
        print("Error: No internet connection.")
        return None

# main menu
def main():
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        return
    username = sys.argv[1]
    events = fetch_activity(username)
    if events:
        print(f"Success! Found {len(events)} activities.")
        print("--- A Peek at the First Event's Raw Data ---")
        print(json.dumps(events[0], indent=4))

if __name__ == "__main__":
    main()