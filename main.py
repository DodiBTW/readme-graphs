import os
import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import GithubAPI.github_requester as github_requester
import GithubAPI.github_data_extractor as github_data_extractor
import Graphs.graph_generator as graph_generator
import uvicorn

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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/language-donut-chart")
    async def create_donut_chart(user: str):
        repo_data = await requester.get_user_languages(user, limit=5)
        if repo_data is None:
            return {"error": "Error fetching user languages"}
        donut_chart_svg = generator.generate_donut_chart(f"{user}'s top languages",repo_data)
        svg_stream = io.StringIO(donut_chart_svg)
        return StreamingResponse(svg_stream, media_type="image/svg+xml")
    @app.get("/repo-star-history")
    async def get_repo_star_history(user: str, repo: str):
        repo_stars = await requester.get_repo_star_history(user, repo)
        if repo_stars is None:
            return {"error": "Repository not found"}
        creation_date = await requester.get_repo_details(user, repo)
        creation_date = creation_date["created_at"]
        star_history = extractor.extract_star_history(repo_stars, creation_date)
        star_history_svg = generator.generate_history_chart(f"{user}/{repo}'s star history", star_history)
        svg_stream = io.StringIO(star_history_svg)
        return StreamingResponse(svg_stream, media_type="image/svg+xml")

    uvicorn.run(app, host="0.0.0.0", port=8000)