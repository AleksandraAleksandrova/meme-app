// this app is doing the same as app.py
// but it is written in JS and it uses the Octokit library

import { appID, pemPath, whSecret} from './config.mjs';
import { Octokit } from '@octokit/rest';
import { createAppAuth } from '@octokit/auth-app';
import { readFileSync } from 'fs';
import { Webhooks } from '@octokit/webhooks';
import http from 'http';
import axios from 'axios';

const privateKey = readFileSync(pemPath);

const auth = createAppAuth({
  appId: appID,
  privateKey: privateKey.toString(),
});

const octokit = new Octokit();
octokit.auth = auth;

const webhooks = new Webhooks({
  secret: whSecret,
});

const server = http.createServer(webhooks.middleware);
server.listen(5000, () => {
  console.log('Webhook server started on port 5000');
});

webhooks.on("issues", async ({ id, name, payload }) => {
  console.log("event is issues")
  if(payload.action === 'opened'){
    console.log("the action  is opened")
    const issue_number = payload.issue.number;

    const { data } = await axios.get('https://meme-api.com/gimme');
    console.log("fetched a meme")

    const response = await octokit.issues.createComment({
      owner: payload.repository.owner.login,
      repo: payload.repository.name,
      issue_number,
      body: `**${data.title}**\n\n![${data.title}](${data.url})`,
    });
    console.log("comment must be ok")

  } else {
    console.log(`Received unsupported event: ${payload.action}`);
  }
  
});

// This code doesn't work yet, smee channel didn't get any kind of event so no payload was received and no actions were performed
