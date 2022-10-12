# Natalie Abrams interview task - sleuth.io 2022
import os

from flask import Flask, Response, request
from flask import jsonify

import logging

from github import GithubREST
from query_params import DEFAULT_PAGE, DEFAULT_PER_PAGE

dev_mode = True
app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s %(message)s",
)


@app.route("/")
def health_check() -> dict:
    return {
        "data": "Hello, welcome to Sleuth backend interview task. Please see instructions in README.md"
    }


@app.route("/health/github")
def github_api_root_example() -> dict:
    return GithubREST().get("/")


@app.route("/github/repos/<path:repository>/pulls", methods=["GET"])
def github_repository_pull_requests(repository: str):
    # collect query params
    page = request.args.get("page", DEFAULT_PAGE)
    per_page = request.args.get("per_page", DEFAULT_PER_PAGE)
    query_params = {
        "page":page,
        "per_page":per_page
        }

    repo_pulls_request_url = f"/repos/{repository}/pulls"
    # need error handling for api request
    repo_pulls_response =  GithubREST().get(url_path=repo_pulls_request_url, params=query_params)    
    response_data = repo_pulls_response["data"]
    
    repo_pr_data =[
        {
            "repo_name": repository,
            "query_params":query_params
            }]
    for pr in response_data:
        pull_number = pr["number"]
        pr_commits_url = f"/repos/{repository}/pulls/{pull_number}/commits"
        # need error handling for api request
        pr_commits_response = GithubREST().get(pr_commits_url)
        number_of_commits = len(pr_commits_response["data"])
        single_pr_data = {
            "title": pr["title"],
            "username": pr["user"]["login"],
            "num_commits": number_of_commits,
            "head_sha": pr["head"]["sha"],
            "last_updated": pr["updated_at"]                  
            }

        repo_pr_data.append(single_pr_data)

    return {"data":repo_pr_data}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
