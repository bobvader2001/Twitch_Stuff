# Twitch_Stuff
Twitch related data things

## Viewers.py
Requests the viewers of a given Twitch stream `target_twitch` (and optionally a YouTube stream, `youtube_id`) every `interval` seconds. The output is saved in a csv format with the output file named \[target_twitch\].csv. 

### Instructions
The only things that need to be changed are the variable names at the top of the `main()` function:
`client_id` is the ID of your Twitch app
`target_twitch` is the target channel name (can be found in the URL bar when on their channel)
`youtube_id` is the ID of the YouTube stream (everything after "v=" in the URL) - Can be left empty if there is no YouTube stream
`interval` is the time interval in seconds between requests (unauthenticated Twitch apps are limited to 30 requests per minute)

Then just run the Python file!
