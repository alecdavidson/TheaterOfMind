import asyncio, configparser, discord, io, os, requests
from time import sleep

class Bot(discord.Client):
    # Bot Startup
    async def on_ready(self):
        print(f'Finding Channels...')
        for i in self.guilds:
            if str(i) == self._g:
                self.guild = i

        self.cchannel,self.vchannel = None,None

        self.cchannel = discord.utils.get(self.get_all_channels(), guild__name=self.guild.name, name=self._c)
        self.vchannel = discord.utils.get(self.get_all_channels(), guild__name=self.guild.name, name=self._v)

        if self.cchannel==None: print(f"▲ Could not find Command Channel {self._c}")
        if self.vchannel==None: print(f"▲ Could not find Voice Channel {self._v}")

        print(f'▲ {self.user} is now running!')
        print(f'▲ Joining {self.vchannel} (Voice)!')
        self._loop = False

        await self.join_vc()

    # Triggers on Messages
    async def on_message(self, message):
        guild = message.guild
        channel = message.channel

        if guild != self.guild or channel != self.cchannel or message.author == self.user:
            return

        username = str(message.author)
        cmd = str(message.content).lower()

        print(f'▲ {username} said: "{cmd}" ({guild}: {channel})')

        # Parse Commands
        try:
            if cmd == 'join': await self.join_vc()
            elif cmd == 'leave': await self.leave_vc()
            elif cmd == 'refresh': await self.refresh_vc()
            elif cmd == 'stop': await self.stop_sound()
            elif 'track' in cmd:
                file = cmd.split(' ')[1]
                await self.stop_sound()
                await self.play_sound('track',file)
            elif 'clip' in cmd:
                file = cmd.split(' ')[1]
                await self.play_sound('clip',file)
            elif cmd == 'shutdown': await self.shutdown()
        except Exception as e:
            print(f"on_message error: {e}")

    # Join a Voice Channel
    async def join_vc(self):
        print(f"▲ Attempting to Join {self.vchannel}")
        try:
            self.VClient = await self.vchannel.connect(self_mute=True)
        except Exception as e:
            print(f"join_vc error: {e}")

    # Leave Active Voice Channel
    async def leave_vc(self):
        print(f"▲ Attempting to Disconnect from {self.vchannel}")
        try:
            await self.stop_sound()
            await self.VClient.disconnect()
        except Exception as e:
            print(f"▲ leave_vc error: {e}")

    # Leave and Rejoin Active Voice Channel
    async def refresh_vc(self):
        print(f"▲ Attempting to Refresh {self.vchannel}")
        try:
            await self.leave_vc()
            await self.join_vc()
        except Exception as e:
            print(f"▲ refresh_vc error: {e}")

    # Stream Audio into Active Voice Channel
    async def play_sound(self,type,file):
        base_path = os.path.abspath(os.getcwd())
        looping = self._loop
        if type == "track":
            looping = True
            sound_path = f"{base_path}/sounds/tracks/{file}"
        elif type == "clip":
            looping = False
            sound_path = f"{base_path}/sounds/clips/{file}"

        print(f"Attempting to play {sound_path}")
        audio = discord.FFmpegPCMAudio(source=sound_path,executable=self.ffmpeg)

        # Stream Audio Source to Voice Channel
        try:
            await self.stop_sound()
            self._loop = looping
            self.VClient.play(audio,after=lambda e:self.looper(type,file))
        except Exception as e:
            print(f"▲ play_sound error (Playback): {e}")

    async def stop_sound(self):
        try:
            self._loop = False
            if self.VClient.is_playing(): self.VClient.stop()
        except Exception as e:
            print(f"▲ stop error: {e}")

    async def shutdown(self):
        await self.leave_vc()
        await self.close()

    def looper(self,type,file):
        print("Looping")
        if self._loop:
            if type == 'track': req = f"/tracks/{file}"
            else: req = f"/clips/{file}"
            requests.get(f"http://127.0.0.1:5000{req}")

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    TOKEN = config['DEFAULT']['TOKEN']
    INTENTS = discord.Intents.default()
    INTENTS.messages = bool(config['PERMS']['COMMS_PERMS'])
    INTENTS.message_content = bool(config['PERMS']['COMMS_PERMS'])
    INTENTS.voice_states = bool(config['PERMS']['VOICE_PERMS'])

    _g = config['CHANNELS']['GUILD']
    _c = config['CHANNELS']['COMMS_CHANNEL']
    _v = config['CHANNELS']['VOICE_CHANNEL']
    _f = config['DEFAULT']['FFMPEG']

    return INTENTS,TOKEN,{"_guild":_g,"_commands":_c,"_voice":_v,"_ffmpeg":_f}

def run_discord_bot():
    INTENTS,TOKEN,CONF = load_config('bot_conf.ini')
    BOT = Bot(intents=INTENTS)
    BOT._g = CONF['_guild']
    BOT._c = CONF['_commands']
    BOT._v = CONF['_voice']
    BOT.ffmpeg = CONF['_ffmpeg']
    BOT.run(TOKEN)

if __name__=='__main__':
    run_discord_bot()
