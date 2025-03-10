import requests
import json

class GithubRequester:
    def __init__(self, api_key):
        self.headers = {
            'Authorization': f'token {api_key}'
        }

    def get_user_repos(self, username):
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)

    def get_user_details(self, username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)

    def get_repo_details(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)

    def get_user_commits(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/commits"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)

    def get_repo_commits(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/commits"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)

    def get_repo_languages(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/languages"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)
    def get_commit_details(self, username, repo, sha):
        url = f"https://api.github.com/repos/{username}/{repo}/commits/{sha}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return json.loads(response.text)