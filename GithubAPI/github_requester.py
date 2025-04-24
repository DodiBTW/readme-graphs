import aiohttp
import asyncio
import json

class GithubRequester:
    def __init__(self, api_key):
        self.headers = {
            'Authorization': f'token {api_key}'
        }

    async def fetch(self, url, session, headers=None):
        async with session.get(url, headers=headers) as response:
            if response.status == 404:
                return None
            if response.status != 200:
                raise Exception(f"GitHub API error: {response.status} - {await response.text()}")
            return await response.json()

    async def get_user_repos(self, username):
        url = f"https://api.github.com/users/{username}/repos"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_user_details(self, username):
        url = f"https://api.github.com/users/{username}"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_repo_details(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_user_commits(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/commits"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_repo_commits(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/commits"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_repo_languages(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/languages"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_commit_details(self, username, repo, sha):
        url = f"https://api.github.com/repos/{username}/{repo}/commits/{sha}"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)

    async def get_user_languages(self, username, limit=99):
        repos = await self.get_user_repos(username)
        if repos is None:
            return None
        languages = {}
        async with aiohttp.ClientSession() as session:
            for repo in repos:
                if repo.get("fork"):
                    continue
                repo_languages = await self.get_repo_languages(username, repo["name"])
                for language, bytes_of_code in repo_languages.items():
                    languages[language] = languages.get(language, 0) + bytes_of_code
        languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
        other = 0
        for key in list(languages.keys())[limit:]:
            other += languages[key]
            del languages[key]
        total = sum(languages.values())
        for key in list(languages.keys()):
            if languages[key] / total < 0.05:
                other += languages[key]
                del languages[key]
        if other > 0:
            languages["Other"] = other
        return languages

    async def get_repo_star_history(self, username, repo):
        url = f"https://api.github.com/repos/{username}/{repo}/stargazers"
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.v3.star+json"
        all_stars = []
        
        async with aiohttp.ClientSession() as session:
            while url:
                response = await session.get(url, headers=headers, params={"per_page": 100})
                if response.status == 404:
                    return None
                if response.status != 200:
                    raise Exception(f"GitHub API error: {response.status} - {await response.text()}")
                
                all_stars.extend(await response.json())
                
                links = response.headers.get("Link", "")
                next_link = None
                for link in links.split(","):
                    if 'rel="next"' in link:
                        next_link = link.split(";")[0].strip("<> ")
                        break
                url = next_link
        
        return all_stars

    async def get_user_star_history(self, username):
        url = f"https://api.github.com/users/{username}/starred"
        async with aiohttp.ClientSession() as session:
            return await self.fetch(url, session, self.headers)
