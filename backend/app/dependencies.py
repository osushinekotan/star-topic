import base64
import os
import re

import markdown  # type: ignore
import requests  # type: ignore
from bs4 import BeautifulSoup


def get_github_token() -> str:
    """環境変数からGitHubのトークンを取得する。"""
    token = os.getenv("GITHUB_PAT")
    if not token:
        raise Exception("GitHub token not found in environment variables.")
    return token


def fetch_starred_repos(username: str) -> list[dict]:
    """GitHubユーザーのスター付きリポジトリを取得する。"""
    token = get_github_token()
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/users/{username}/starred"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    return response.json()


def fetch_readme(repo_full_name: str) -> str:
    """指定されたリポジトリのREADMEを取得し、クレンジングしてテキストを返す。"""
    token = get_github_token()
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/repos/{repo_full_name}/readme"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        return cleanse_markdown(content)
    else:
        raise Exception(f"Failed to fetch README: {response.status_code}")


def cleanse_markdown(markdown_text: str) -> str:
    """Markdown形式のテキストからMarkdownの記法を削除してプレーンテキストを抽出する。

    Args:
        markdown_text (str): Markdown形式のテキスト。

    Returns:
        str: クレンジングされたプレーンテキスト。
    """
    html = markdown.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\[!\[.*?\]\(.*?\)\]\(.*?\)", "", text)  # ネストされた画像リンクの除去
    text = re.sub(r"\[!\[.*?\]\(.*?\)\]", "", text)  # 通常の画像リンクの除去
    return text
