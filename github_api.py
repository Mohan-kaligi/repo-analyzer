import requests


def check_repo_exists(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data["private"] is False:
            return True

    return False