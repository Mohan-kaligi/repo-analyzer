import requests
import os

SONAR_TOKEN = os.getenv("SONAR_TOKEN")

SONAR_ORG = "mohan-kaligi"

BASE_URL = "https://sonarcloud.io/api"


def check_project_exists(project_key):

    url = f"{BASE_URL}/projects/search"

    response = requests.get(
        url,
        params={
            "organization": SONAR_ORG,
            "projects": project_key
        },
        auth=(SONAR_TOKEN, "")
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code != 200:
        return False

    data = response.json()

    if data["paging"]["total"] > 0:
        return True

    return False


def get_issues(project_key):

    url = f"{BASE_URL}/issues/search"

    response = requests.get(
        url,
        params={
            "componentKeys": project_key,
            "resolved": "false",
            "ps": 100
        },
        auth=(SONAR_TOKEN, "")
    )

    if response.status_code != 200:
        return []

    try:
        data = response.json()
    except:
        return []

    return data.get("issues", [])