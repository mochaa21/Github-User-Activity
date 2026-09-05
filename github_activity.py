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

def display_activity(events):
    if not events:
        print("No recent activity found.")
        return
    for event in events:
        action = event['type']
        repo_name = event['repo']['name']
        if action == 'PushEvent':
            commits = event['payload'].get('commits', [])
            commit_count = len(commits)

            if commit_count == 0 and 'size' in event['payload']:
                commit_count = event['payload']['size']
            if commit_count > 0:
                print(f"- Pushed {commit_count} commits to {repo_name}")
            else:
                print(f"- Pushed to {repo_name}")
        elif action == 'IssuesEvent':
            issue_action = event['payload'][action]
            print(f"- {issue_action.capitalize()} an issue in {repo_name}")
        elif action == 'WatchEvent':
            print(f"- Starred {repo_name}")
        elif action == 'CreateEvent':
            print(f"- Created a new repository or branch in {repo_name}")
        else:
            print(f"- {action} at {repo_name}")


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
        display_activity(events)

if __name__ == "__main__":
    main()