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
        repo_data = requester.get_user_languages(user, limit=5)
        donut_chart_svg = generator.generate_donut_chart(f"{user}'s top languages",repo_data)

        svg_stream = io.StringIO(donut_chart_svg)
        return StreamingResponse(svg_stream, media_type="image/svg+xml")

    uvicorn.run(app, host="0.0.0.0", port=8000)
