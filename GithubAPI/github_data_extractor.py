import json
class GithubDataExtractor:
    def __init__(self):
        pass
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
    def extract_star_history(self, repo_stars, creation_date):
        star_history = []
        stars = 0
        # Fetch repo creation date and set to 0 stars
        star_history.append({"date": creation_date.split("T")[0], "stars": 0})
        for entry in repo_stars:
            stars += 1
            date = entry["starred_at"].split("T")[0]
            star_history.append({"date": date, "stars": stars})
        return star_history