# Rock-paper-scissor autoplayer

### The bots are designed to be as simple as possible:
* Bots only play as player A, which means a bot never deploys a contract.
* Bots do not verify signatures
* Bots do very little to check validity of incoming messages.

### How do bots receive messages?
* For each bot, there is a permanent entry in the Challenges table in Firebase.
* A GC function monitors Firebase for new messages: https://github.com/magmo/rps-functions
* A GC function forwards new messages to Google App Engine (which is the bot server).

### What tools should I use for development?
* Use VS Code python extension.
* For testing, pytest is used (modify VS Code settings to enable pytest)

### How do I test the bots?
* Rely as much as you can on unit testing (pytest).
* The bots are NOT setup to be run as a local server. This can be changed if needed.
* For integration testing, the code base has to be deployed to App Engine (takes about 3 minutes), then the client application (the manual player) needs to be run with .env file containing TARGET_NETWORK=ropsten.
* You can look in the App Engine console for errors.

## How do I deploy the bots to the app engine?
* Deployment to the development environment is done via the `gcloud` command: `gcloud app deploy` from the root directory.
* Deployment to the production environment is automatically triggered from the `deploy` branch. 
