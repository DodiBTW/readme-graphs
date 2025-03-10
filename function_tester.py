# This file is used to test the different functions of the program
import GithubAPI.github_requester as github_requester
import GithubAPI.github_data_extractor as github_data_extractor
import Graphs.graph_generator as graph_generator
import os
from dotenv import load_dotenv
if __name__ == "__main__":
    user_to_request = "DodiBTW"
    # Get githubapikey from env
    load_dotenv()
    api_key = os.getenv("GITHUB_API_KEY")
    if not api_key:
        raise ValueError("Github API Key not found")
    requester = github_requester.GithubRequester(api_key)
    extractor = github_data_extractor.GithubDataExtractor()
    generator = graph_generator.GraphGenerator()
    user_details = requester.get_user_details(user_to_request)
    repos = requester.get_user_repos(user_to_request)

    languages = {}
    for repo in repos:
        repo_languages = requester.get_repo_languages(user_to_request, repo["name"])
        for language, bytes_of_code in repo_languages.items():
            if language in languages:
                languages[language] += bytes_of_code
            else:
                languages[language] = bytes_of_code

    if len(languages) > 5:
        # sort by amount
        languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
        other = 0
        for key in list(languages.keys())[5:]:
            other += languages[key]
            del languages[key]
        languages["Other"] = other

    generator.generate_donut_chart(user_to_request,languages)