import requests
import json

class GithubRequester:
    def get_user_repos(self, username):
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        return json.loads(response.text)
    def get_user_details(self, username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        return json.loads(response.text)
    def get_repo_details(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        return json.loads(response.text)