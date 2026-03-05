def extract_repo_details(repo_url):

    parts = repo_url.strip().split("/")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


def create_project_key(owner, repo):
    return f"{owner}_{repo}"