from flask import Flask
import configparser, requests

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('bot_conf.ini')
WEBHOOK_URL = config['DEFAULT']['WEBHOOK_URL']

def send_command(url,command):
    content = {"content":command}
    response = requests.post(url, content)
    print(command)
    return response.content

@app.get("/")
def slash():
    return send_command(WEBHOOK_URL,
        command = "Commander reporting for duty!"
    )

@app.get("/test")
def test():
    return send_command(WEBHOOK_URL,
        command = "test"
    )

@app.get("/tracks/<track>")
def play_track(track):
    return send_command(WEBHOOK_URL,
        command = f"track {track}"
    )

@app.get("/clips/<clip>")
def play_clip(clip):
    return send_command(WEBHOOK_URL,
        command = f"clip {clip}"
    )

@app.get("/refresh")
def refresh():
    return send_command(WEBHOOK_URL,
        command = "refresh"
    )

@app.get("/join")
def join():
    return send_command(WEBHOOK_URL,
        command = "join"
    )

@app.get("/leave")
def leave():
    return send_command(WEBHOOK_URL,
        command = "leave"
    )

@app.get("/stop")
def stop():
    return send_command(WEBHOOK_URL,
        command = "stop"
    )

@app.get("/shutdown")
def shutdown():
    return send_command(WEBHOOK_URL,
        command = "shutdown"
    )
