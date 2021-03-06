#Sample chat message in IRC protocol
#:bobvader2001!bobvader2001@bobvader2001.tmi.twitch.tv PRIVMSG #Rainbow6 :Rook Mine

import datetime
import json
import re
import socket
import sys


def analyse(msg, teams, counter, greedy):
    msg = msg.lower()
    for team, mentions in teams.items():
        for permutation in mentions:
            #Regex to find the permutation of the team name in the input  message
            #There will only be a match if there are no word characters adjacent to the permutation
            #This is to prevent team name abbreviations matching in larger words e.g. "eg" matching if someone types "egg"
            matches = re.findall(r'\b' + permutation + r'\b', msg)
            if greedy:
                counter[team] += len(matches)
            else:
                if matches:
                    counter[team] += 1
                    break
            if matches:
                print(f"Current total: {counter}", end="\r")


def main():
    HOST = "irc.twitch.tv"
    NICK = "chat_stats_bot" #Should be your Twitch username according to docs
    PORT = 6667
    PASS = "oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #OAuth token generated here: http://www.twitchapps.com/tmi
    CHANNEL = "#rainbow6" #Twitch channel name prefixed by a hash
    teams_file = "teams.json" #JSON file containing the teams you are looking for and the different ways they may be mentioned
    #If greedy is true, the counter will increase for every time a team is mentioned in one message
    #If greedy is false, the counter will increment 1, regardless of the number of times a team is mentioned in a message
    greedy = True
    output_file = "output" #Name of output CSV file

    try:
        with open(teams_file, "r") as fp:
            teams = json.load(fp)
    except:
        print("Error loading teams file")
        sys.exit(1)

    counter = {}
    for team in teams:
        counter[team] = 0

    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        s.send(("PASS " + PASS + "\r\n").encode())
        s.send(("NICK " + NICK + "\r\n").encode())
        s.send(("JOIN " + CHANNEL + "\r\n").encode())
    except:
        print("Error joining IRC")
        sys.exit(1)

    print(f"\nCurrent total: {counter}", end="\r")

    msg = ""
    try:
        while True:
            try:
                msg = s.recv(1024).decode()
            except:
                print("\nError decoding message!\n")
                continue
            if "PRIVMSG" in msg:
                author = msg.split("!")[0][1:]
                content = msg.split(CHANNEL)[1][2:].rstrip()
                analyse(content, teams, counter, greedy)
            elif "PING" in msg:
                #Replies PONG to any PING messages to prevent the server dropping the connection
                ping_arg = msg.split("PING ")[1]
                s.send(f"PONG {ping_arg}".encode())
    except KeyboardInterrupt:
        print("\n\nKeyboard Interrupt Detected...\n")
        print(f"Final Results:")
        for team, count in counter.items():
            print(f"{team}: {count}")
        print("\nOutputting to CSV...")
        with open(f"{output_file}.csv", "a") as fp:
            for team, count in counter.items():
                fp.write(f"{team},{count}\n")
            fp.write("\n")
        print("Done!")
        sys.exit(0)
    except Exception as e:
        print("There was an error but we shall attempt to continue anyway...")
        with open(f"{output_file}.csv", "a") as fp:
            for team, count in counter.items():
                fp.write(f"{team},{count}\n")
            fp.write("\n")
        print(e)
        print(msg)
        print(datetime.datetime.now())
        pass

if __name__ == "__main__":
    main()
