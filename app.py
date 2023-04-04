import os
import requests
from flask import Flask, request
from github import GithubIntegration, Github
import vars

app = Flask(__name__)
app_id = vars.app

with open(
        os.path.normpath(os.path.expanduser(vars.private_key_path)),
        'r'
) as cert_file:
    app_key = cert_file.read()


git_integration = GithubIntegration(
    app_id,
    app_key,
)

# post a meme when an issue is created
"""
@app.route("/", methods=['POST'])
def bot():
    payload = request.json

    if not all(k in payload.keys() for k in ['action', 'issue']) and \
            payload['action'] == 'opened':
        return "ok"

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(number=payload['issue']['number'])

    response = requests.get(url='https://meme-api.com/gimme')
    if response.status_code != 200:
        return 'ok'

    meme_url = response.json()['preview'][-1]
    issue.create_comment(f"![Alt Text]({meme_url})")
    return "ok"
"""

# close all the opened issues when a new issue with "close all" body is created
"""
@app.route("/", methods=['POST'])
def bot():
    payload = request.json

    if all(k in payload.keys() for k in ['action', 'issue']) and payload['action'] == 'opened' and payload['issue']['body'] == 'close all':

        owner = payload['repository']['owner']['login']
        repo_name = payload['repository']['name']

        git_connection = Github(
            login_or_token=git_integration.get_access_token(
                git_integration.get_installation(owner, repo_name).id
            ).token
        )
        repo = git_connection.get_repo(f"{owner}/{repo_name}")

        for issue in repo.get_issues(state='open'):
            issue.edit(state='closed')

    return "ok"
"""

@app.route("/", methods=['POST'])
def bot():
    payload = request.json

    if 'commits' in payload and 'before' in payload and 'after' in payload:
        owner = payload['repository']['owner']['login']
        repo_name = payload['repository']['name']
        commits = payload['commits']

        git_connection = Github(
            login_or_token=git_integration.get_access_token(
                git_integration.get_installation(owner, repo_name).id
            ).token
        )
        repo = git_connection.get_repo(f"{owner}/{repo_name}")

        for commit in commits:
            commit_sha = commit['id']
            commit_message = commit['message']
            commit_url = commit['url']
            author_name = commit['author']['name']
            author_email = commit['author']['email']

            comment_body = f"""
                New commit pushed by {author_name} ({author_email}):
                Commit message: {commit_message}
                Commit URL: {commit_url}
                """

            repo.get_commit(commit_sha).create_comment(comment_body)

    return "ok"

if __name__ == "__main__":
    app.run(debug=False, port=5000)
