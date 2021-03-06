# import os
# from slackclient import SlackClient

# SLACK_TOKEN = os.environ["SLACKBOT_SPONGEBOB_TOKEN"]
# print SLACK_TOKEN
# SC = SlackClient(SLACK_TOKEN)

# SC.api_call(
#     "chat.postMessage",
#     channel="#general",
#     text="Hello from Python! :tada:"
# )

import os
from flask import Flask, request
from slackclient import SlackClient

client_id = os.environ["SLACK_SPONGEBOB_CLIENT_ID"]
client_secret = os.environ["SLACK_SPONGEBOB_CLIENT_SECRET"]
oauth_scope = os.environ["SLACK_SPONGEBOB_BOT_SCOPE"]

app = Flask(__name__)

@app.route("/begin_auth", methods=["GET"])
def pre_install():
    return '''
        <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
            Add to Slack
        </a>
    '''.format(oauth_scope, client_id)

@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    # Retrieve the auth code from the request params
    auth_code = request.args['code']
    # An empty string is a valid token for this request
    sc = SlackClient("")
    # Request the auth tokens from Slack
    auth_response = sc.api_call(
        "oauth.access",
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code
    )

    # Save the bot token to an environmental variable or to your data store
    # for later use
    # os.environ["SLACK_USER_TOKEN"] = auth_response['access_token']
    os.environ["SLACKBOT_SPONGEBOB_TOKEN"] = auth_response['bot']['bot_access_token']
    SLACK_TOKEN = os.environ["SLACKBOT_SPONGEBOB_TOKEN"]
    sc = SlackClient(SLACK_TOKEN)

    sc.api_call(
        "chat.postMessage",
        channel="#general",
        text="Hello from Python! :tada:"
    )

    # Don't forget to let the user know that auth has succeeded!
    return "Auth complete!"
