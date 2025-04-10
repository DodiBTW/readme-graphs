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
    def get_user_languages(self, username, limit=99):
        repos = self.get_user_repos(username)
        if repos is None:
            return None
        languages = {}
        for repo in repos:
            if repo.get("fork"):
                continue
            repo_languages = self.get_repo_languages(username, repo["name"])
            for language, bytes_of_code in repo_languages.items():
                languages[language] = languages.get(language, 0) + bytes_of_code
        languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
        other = 0
        for key in list(languages.keys())[limit:]:
            other += languages[key]
            del languages[key]
        if other > 0:
            languages["Other"] = other
        return languages