import os
import json
import requests
from pathlib import Path

WEBHOOK = os.environ["SHEET_WEBHOOK"]

# Find latest LeetHub folder
folders = [
    f for f in Path(".").iterdir()
    if f.is_dir() and f.name[:4].isdigit()
]

latest = max(folders, key=lambda x: x.stat().st_mtime)

folder_name = latest.name

title_slug = folder_name.split("-", 1)[1]

query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    difficulty
  }
}
"""

variables = {
    "titleSlug": title_slug
}

response = requests.post(
    "https://leetcode.com/graphql",
    json={
        "query": query,
        "variables": variables
    }
)

question = response.json()["data"]["question"]

payload = {
    "id": question["questionFrontendId"],
    "name": question["title"],
    "difficulty": question["difficulty"],
    "date": os.popen("date +%F").read().strip(),
    "github": f"https://leetcode.com/problems/{question['titleSlug']}/"
}

requests.post(
    WEBHOOK,
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

print("Google Sheet Updated Successfully")
