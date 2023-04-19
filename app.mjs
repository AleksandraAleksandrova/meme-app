import { readFileSync } from 'node:fs';
import { appId, pemPath } from './config.mjs';
import express from 'express';
import { App } from "octokit";

const privateKey = readFileSync(pemPath);

const server = express();
server.use(express.json());

const app = new App({
  appId: appId,
  privateKey: privateKey,
});

server.post("/", async (req, res) => {
  const event = req.headers["x-github-event"];
  const payload = req.body;
  const owner = payload.repository.owner.login;
  const repo_name = payload.repository.name;
  const installationId = payload.installation.id;

  if (payload.action != 'opened' || event != 'issues') {
    console.log("not supported event and action right now")
    return res.send("ok");
  }

  const octokit = await app.getInstallationOctokit(installationId);
  const repo = await octokit.rest.repos.get({ owner, repo: repo_name });

  /*
  const response = await fetch('https://meme-api.com/gimme');
  if (!response.ok) {
      return res.send('ok');
  }

  const meme_url = (await response.json()).preview.slice(-1)[0];
  await octokit.rest.issues.createComment({ owner, repo: repo_name, issue_number: payload.issue.number, body: `![Alt Text](${meme_url})` });
  return res.send("ok");
*/
});


server.listen(5000, () => {
  console.log(`Server listening on port 5000`);
});


