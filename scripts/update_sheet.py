import json
import os
import requests

WEBHOOK = os.environ["SHEET_WEBHOOK"]

# Change this before running
title_slug = "palindrome-number"

query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    difficulty
    titleSlug
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
    "id": question["questionId"],
    "name": question["title"],
    "difficulty": question["difficulty"],
    "date": "",
    "github": f"https://leetcode.com/problems/{question['titleSlug']}/"
}

r = requests.post(WEBHOOK, json=payload)

print(r.text)
