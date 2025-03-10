import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import GithubAPI.github_requester as github_requester
import GithubAPI.github_data_extractor as github_data_extractor
import Graphs.graph_generator as graph_generator

if __name__ == "__main__":
    print("Starting API server...")
    load_dotenv()
    api_key = os.getenv("GITHUB_API_KEY")
    if not api_key:
        raise ValueError("Github API Key not found")
    requester = github_requester.GithubRequester(api_key)
    extractor = github_data_extractor.GithubDataExtractor()
    generator = graph_generator.GraphGenerator()
    app = FastAPI()
