import os
import requests
from flask import Flask, request
from github import GithubIntegration
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

jwt = git_integration.create_jwt()

@app.route("/", methods=['POST'])
def bot():
    payload = request.json
    if payload["action"] == "created" and payload["issue"] and payload["issue"]["comments"]:
        # Hit the stubbed marketplace endpoint to get account data
        headers = {"Authorization": f"Bearer {jwt}"}
        r = requests.get("https://api.github.com/marketplace_listing/stubbed/accounts/ACCOUNT_ID", headers=headers)
        data = r.json()

        # Check if email matches expected value
        email = data['organization_billing_email']
        if email == "billing@github.com":
            # create a new workflow running the test-workflow.yml file
            headers = {"Authorization": f"Bearer {jwt}"}
            username = payload["repository"]["owner"]["login"]
            repo_name = payload["repository"]["name"]
            resp = requests.post(f"https://api.github.com/repos/{username}/{repo_name}/actions/workflows/test-workflow.yml/dispatches", headers=headers)
            if resp.status_code == 204:
                print("Workflow event dispatched successfully.")
            else:
                # get this error, not sure why
                print(f"Failed to dispatch workflow event. Status code: {resp.status_code}")

            # Close the issue
            """"
            issue_number = payload["issue"]["number"]
            comment_id = payload["comment"]["id"]
            repo.get_issue(issue_number).create_comment("Everything okay")
            repo.get_comment(comment_id).delete()
            repo.get_issue(issue_number).edit(state="closed")
            """
        
    return "success"

if __name__ == "__main__":
    app.run(debug=True, port=5000)

