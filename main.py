from time import sleep
import bot, subprocess, threading

server_proc = None

def create_server():
    global server_proc
    server_proc = subprocess.Popen(["flask", "--app", "server", "run", "--host=0.0.0.0"])


if __name__=='__main__':
    bot_thread = threading.Thread(target=bot.run_discord_bot)
    server_thread = threading.Thread(target=create_server)

    bot_thread.start()
    server_thread.start()

    while bot_thread.is_alive():
        sleep(5)

    server_proc.terminate()
