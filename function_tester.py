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

    languages = requester.get_user_languages(user_to_request, limit=5)

    out = generator.generate_donut_chart(f"{user_to_request}'s top languages",languages)
    # Out variable contains the svg content of the donut chart
    # save temporarily
    with open("donut_chart.svg", "w") as f:
        f.write(out)