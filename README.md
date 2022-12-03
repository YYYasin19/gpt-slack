# ChatGPT Slack Integration

This very simple bot allows one to use Slack as an interface for ChatGPT.
The only requirements are some Slack Authentication credentials you can get from Slack's Developer page.

The bot is designed to only answer on messages that are posted in a specific channel and have a 'robot_face' reaction.
The channel is determined by the CHANNEL_ID environment variable. You can the ID of a channel by visiting the channel in our browser and extracting it from the URL.

Most of the bot was written by ChatGPT itself (ironic).

Beware that this was created on a train ride and seemed to work for the simple use cases I tested and with some elavated rate limitations. Some of the timings etc. might need to be adjusted for you.
The first time, the bot might need to login. After that, it should reuse the session parameters.

I'll try and improve this further in the future! (e.g. add scheduling for faster response, multiple workers, other browsers per config file)