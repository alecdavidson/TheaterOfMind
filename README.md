# TheaterOfMind

Virtual Environment (Optional)

pip install -r requirements.txt

install ffmpeg - https://ffmpeg.org/download.html

Create Bot - https://discord.com/developers/applications/

Invite Bot to Discord

Create Webhook for Text Channel

Fill out bot_conf.ini, no need to touch PERMS, everything is Case Sensitive

Throw your music into ./sounds/tracks and sound bites into ./sounds/clips

# Commands
join - Tells ToM to join the Voice Channel Specified in bot_conf.ini
leave - Tells ToM to leave the Voice Channel
refresh - Executes leave and then join commands
stop - Stop playing current track
track  {file} - Play a file from the tracks folder and loop it
clip {file} - Play a file from the clips folder
shutdown - Shutdown the Bot and Command Server
