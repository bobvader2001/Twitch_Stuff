# Twitch_Stuff
Twitch related data things (designed with Rainbow6 in mind).

## Viewers.py
Requests the viewers of a given Twitch stream `target_twitch` (and optionally a YouTube stream, `youtube_id`) every `interval` seconds. The output is saved in a csv format with the output file named \[target_twitch\].csv. 


### Instructions
The only things that need to be changed are the variable names at the top of the `main()` function:  
`client_id` is the ID of your Twitch app  
`target_twitch` is the target channel name (can be found in the URL bar when on their channel)  
`youtube_id` is the ID of the YouTube stream (everything after "v=" in the URL) - Can be left empty if there is no YouTube stream  
`interval` is the time interval in seconds between requests (unauthenticated Twitch apps are limited to 30 requests per minute)  

Then just run the Python file!

## Chat.py
Records the number of times each team in `teams_file` is mentioned in any of the ways specified in the list using the Twitch Chat IRC and outputs to a .csv file.


###Instructions
A few things need to be changed at the top of the `main()` function for the script to work:  
`NICK` should be set to your Twitch username according to the IRC docs  
`PASS` should be set to your OAuth token for your Twitch account (your OAuth token can be generated [here](http://www.twitchapps.com/tmi/))
`CHANNEL` should be set to the target Twitch channel name prefixed by a hash  


#### teams_file
`teams_file` is the JSON file that is read in containing the team names and the different ways of saying them. I have included a sample `teams.json` file that 
includes the NA, EU and LATAM teams for Season 9 of Pro League and the different ways I could think of typing them. If you decided to edit this file, or create 
your own, be careful of multiple matches of the same thing (e.g. if you include "g2" and "g2 esports", the phrase "g2 esports" would be matched twice, even if 
it is only mentioned once). Additionally, all ways of saying a team name should be lowercase as the message string is converted to lowercase before the regex is 
run.


#### greedy
`greedy` is a boolean that is used to control how the matching works. If it is set to true, all occurences of a team name in a message will be counted (e.g. if 
"ENCE" is mentioned twice in a message, the counter will be incremented by 2). If greedy is set to false, the counter will only increment by 1, regardless of 
the number of times and in how many different forms a team is mentioned (e.g. if "EG", "EG" and "Evil Geniuses" occur within the same message, the counter will 
still only increment by 1).


#### output_file
`output_file` is the name of the csv file the results will be output to. This should be changed for each run, but in the event you forget to change it, the 
results will be appended to the file that already exists with a new line separating the 2 runs that have been saved within that file.
