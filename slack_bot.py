import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

#from google.colab import userdata

bot_token = userdata.get("SLACK_BOT_TOKEN")
app_token = userdata.get("SLACK_APP_TOKEN")

print("Bot token:",bot_token)
print("App token:",app_token)

# Initialize your app with your bot token and socket mode handler
app = App(token=bot_token)


# Function to fetch user information
def get_user_info(user_id):
    try:
        client = app.client
        response = client.users_info(user=user_id)
        if response['ok']:
            user_info = response['user']
            return user_info['real_name'], user_info['profile']['email']
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
    return None, None

@app.message("")
def handle_message_events(message, say):
    try:
        # Get the message text
        text = message['text']
        user_id = message['user']

        # Fetch user information
        real_name, email = get_user_info(user_id)
        print(f"Message is {message}")
        slack_msg=f"Request: {text}\nUser: {real_name}\nEmail: {email}"

        print(f"******\nGot message: {slack_msg}\n******")
        p = process_llm_request(GPT_MODEL,[PROMPT_CLASSIFY],text)
        print(f"Processed request: {p}")
        # Send the processed text back to the channel
        if(len(p)>1):
          say(p)

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == "__main__":
    # Get your Bot token and App-level token from the environment variables
    app_token = app_token
    bot_token = bot_token

    # Start your app
    #SocketModeHandler(app, app_token).start()