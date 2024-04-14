from fastapi import APIRouter, HTTPException, Query

from ..dependencies import fetch_starred_repos

router = APIRouter()


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
        repo_info = []
        for repo in repos[:max_repos]:
            repo_full_name = repo["full_name"]
            repo_owner = repo_full_name.split("/")[0]
            repo_name = repo["name"]
            description = repo.get("description", "No description provided.")
            topics = repo.get("topics", [])
            repo_info.append(
                {
                    "owner_username": repo_owner,
                    "repository_name": repo_name,
                    "description": description,
                    "topics": topics,
                }
            )
        return repo_info
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
