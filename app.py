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

    issue = repo.get_issue(number=payload['issues']['number'])

    response = requests.get(url='https://meme-api.herokuapp.com/gimme')
    if response.status_code != 200:
        return 'ok'

    meme_url = response.json()['preview'][-1]
    issue.create_comment(f"![Alt Text]({meme_url})")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
