import requests
import datetime
import time
import sys

def parse_time(td):
    """Return a tuple of hours, minutes and seconds of the input time delta"""
    days, seconds = td.days, td.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return (hours, minutes, seconds)

def main():
    first_run = True
    interval = 30 #Sleep time between requests

    # TWITCH CONFIG
    client_id = "<Twitch Client ID Here>"
    headers = {"Client-ID": client_id}
    target_twitch = "Rainbow6" #Target Twitch channel name

    # YOUTUBE CONFIG
    youtube_key = "<YouTube API Key Here>"
    youtube_id = "" #Target YouTube stream ID (everything after ?v= in URL)

    try:
        while(True):
            print("Requesting Stream Data...")
            twitch_data = requests.get("https://api.twitch.tv/kraken/streams/" + target_twitch, headers=headers).json()
            if twitch_data["stream"] == None:
                print("Channel not currently streaming!\n")
                time.sleep(interval)
                continue
            if youtube_id:
                #If a YouTube ID is given, get the current viewers
                yt_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?key={youtube_key}&part=liveStreamingDetails&id={youtube_id}").json()
                yt_viewers = yt_data["items"][0]["liveStreamingDetails"]["concurrentViewers"]
            print("Processing Stream Data...")
            if first_run:
                #Convert the stream start time to a datetime object
                start_time = datetime.datetime.strptime(twitch_data["stream"]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                first_run = False
            twitch_viewers = twitch_data["stream"]["viewers"] #Twitch viewer count
            #Generate (hours, minutes, seconds) tuple between current time and
            #stream start time
            stream_time_tuple = parse_time(datetime.datetime.utcnow() - start_time)
            #Create a formatted string (HH:MM:SS) out of the tuple
            stream_time = f"{stream_time_tuple[0]}:{stream_time_tuple[1]}:{stream_time_tuple[2]}"
            print("Writing To File...")
            with open(f"{target_twitch}.csv", "a") as fp:
                #Write the Twitch and, if specified, YouTube data to a csv
                if youtube_id:
                    fp.write(f"{stream_time},{twitch_viewers},{yt_viewers}\n")
                else:
                    fp.write(f"{stream_time},{twitch_viewers}\n")
            print("Done!\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
