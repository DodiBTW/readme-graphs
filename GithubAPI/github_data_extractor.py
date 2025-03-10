import json
class GithubDataExtractor:
    def extract_user_details(self, user_details):
        return {
            "username": user_details["login"],
            "name": user_details["name"],
            "email": user_details["email"],
            "location": user_details["location"],
            "bio": user_details["bio"],
            "public_repos": user_details["public_repos"],
            "followers": user_details["followers"],
            "following": user_details["following"]
        }
    def commits_by_year(self, commits):
        commits_by_year = {}
        for commit in commits:
            date = commit["commit"]["author"]["date"]
            year = date.split("-")[0]
            if year in commits_by_year:
                commits_by_year[year] += 1
            else:
                commits_by_year[year] = 1
        return commits_by_year
    def get_all_year_commits(self, commits, year):
        year_commits = []
        for commit in commits:
            date = commit["commit"]["author"]["date"]
            if date.startswith(year):
                year_commits.append(commit)
        return year_commits