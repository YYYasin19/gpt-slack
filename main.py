import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from gpt import GPT
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
load_dotenv()

# Get the current time
current_time = datetime.now()

# Subtract one hour from the current time
max_past = current_time - timedelta(hours=1)

# Set the SLACK_BOT_TOKEN and SLACK_BOT_ID environment variables
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_BOT_ID = os.environ['SLACK_BOT_ID']
SIGNING_SECRET = os.environ['SIGNING_SECRET']

client = WebClient(token=SLACK_BOT_TOKEN)

import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# Create a table to store the message IDs
cursor.execute("CREATE TABLE IF NOT EXISTS messages (id text)")

# Function to insert a message ID into the database
def insert_message_id(message_id):
  cursor.execute("INSERT INTO messages (id) VALUES (?)", (message_id,))
  conn.commit()

# Function to check if a message ID exists in the database
def message_id_exists(message_id):
  cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
  return cursor.fetchone() is not None

def message_filter(slack_msg) -> bool:
    return any(['robot_face' in r['name'] for r in slack_msg['reactions']])\
        and 'subtype' not in slack_msg\
        and slack_msg['user'] != SLACK_BOT_ID \
        and not message_id_exists(slack_msg['ts'])\
        and datetime.fromtimestamp(int(slack_msg['ts'].split('.')[0]))

def slack_worker():
    gpt = GPT()

    ### The following code was written 95%+ by ChatGPT itself ###
    try:
        # Use the Slack API to listen for messages in the specified channel
        response = client.conversations_list(exclude_archived=True, limit=5)
        channels = response['channels']
        for channel in channels:
            if channel['name'] == 'dev-helpdesk':
                channel_id = channel['id']
                break

        # Use a while loop to keep the bot running indefinitely
        while True:
            print('Waiting..')
            # Use the Slack API to listen for messages in the specified channel
            messages = client.conversations_history(channel=channel_id)['messages']

            for message in filter(message_filter, messages):
                print(f"New Message!\nSample:{message['text'][:30]}")
                
                # Use the web query function to perform the search
                gpt_response = gpt.query(message['text'])
                # Use the Slack API to send a message with the query results back to the channel
                client.chat_postMessage(
                    channel=channel_id,
                    text=gpt_response,
                    thread_ts=message['ts']
                )
                # Insert the message ID into the database
                insert_message_id(message['ts'])
                time.sleep(5) # don't get over the rate limit for slack apps
    
    except SlackApiError as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    slack_worker()
