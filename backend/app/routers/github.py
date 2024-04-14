from typing import Any

from fastapi import APIRouter, HTTPException, Query

from ..services.github_service import fetch_starred_repos, format_repos
from ..services.topic_analysis_service import perform_topic_analysis

router = APIRouter()


@router.get("/analyze/user/{username}/analysis")
async def analysis(
    username: str,
    max_repos: int | None = Query(
        5,
        title="Max Repos",
        description="Maximum number of repositories to retrieve information from",
    ),
) -> dict[str, Any]:
    """指定されたGitHubユーザーのスター付きリポジトリから説明文を取得し、トピック分析を実行して結果を返す"""
    try:
        repos = fetch_starred_repos(username)
        repos = format_repos(repos, max_repos)
        descriptions = [(repo["description"] or "") + " " + " ".join(repo["topics"]) for repo in repos]
        if not descriptions:
            raise ValueError("No descriptions available for topic analysis.")

        analysis_results = perform_topic_analysis(descriptions)
        return {
            "repository_info": repos,
            "topic_analysis": analysis_results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/repos/{username}/info", response_model=list[dict])
async def get_repo_info(
    username: str,
    max_repos: int | None = Query(
        5, title="Max Repos", description="Maximum number of repositories to retrieve information from"
    ),
) -> list[dict]:
    """指定されたGitHubユーザーのスター付きリポジトリから説明文とトピックタグを取得し、整理した情報を含むリストで返す"""
    try:
        repos = fetch_starred_repos(username)
        repo_info = format_repos(repos, max_repos)
        return repo_info
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
