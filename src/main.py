import asyncio
from chat_monitoring import ChatMonitoring
from commands import CommandsListener
from spongebob import SpongebobClass
from util.database import DatabaseClass
import discord
from shlex import split
import os
from dotenv import load_dotenv
import subprocess
import logging
import platform
import os.path

from util.reaction_handler import ReactionHandler

LOGFILE_ERROR = 'resources/log/bot_error.log'
LOGFILE_ALL = 'resources/log/bot.log'
logging.basicConfig(filename=LOGFILE_ERROR, level=logging.ERROR)
logging.basicConfig(filename=LOGFILE_ALL, level=logging.DEBUG)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# init client
client = discord.Client(intents=discord.Intents.all())

wdb = DatabaseClass()
all_words = wdb.getAllWords()
del wdb

jed_appreciate = False
ro_troll = False

def jedAppreciate():
    return not jed_appreciate

def roTroll():
    return not ro_troll

@client.event
async def on_ready():
    logging.debug('We have logged in as {0.user}'.format(client))
    s = client.guilds[0].text_channels
    for i in s:
        if str(i) == "bot":
            name = str(client.user).split("#")[0]
            await i.send("{0} online and feeling poggers!".format(name))
            return
    logging.error("Failed to locate channel named 'bot'.")

@client.event
async def on_message(message):
    # set global variables for this method
    global ro_troll

    ### DO NOT MOVE - MUST ALWAYS BE ON TOP
    if message.author == client.user:
        return

    ### GitHub webhook listener and automatic puller
    if str(message.author) == "GitHub#0000":
        try:
            if platform.system() == "Windows":
                logging.error("Cannot run this script on this machine!")
                return
            await message.channel.send("Updating...")
            subprocess.run(['${os.getenv("UPDATE_SCRIPT_PATH")}/resources/scripts/update.sh'], shell=True)
            await message.channel.send("Finished update!")
        except Exception as e:
            logging.error(e)
            await message.channel.send("Update has failed - please check the logs for more details.")
        return
    
    if message.content.startswith("$"): ### Process commands
        await CommandsListener.process_commands(message, client)
        return

    ### Chat monitoring
    await ChatMonitoring.chat_monitor(message)

    ### Reaction watcher
    try:
        rh = ReactionHandler(message)
        react = await client.wait_for('reaction_add', timeout=180.0, check=rh.check)
    except asyncio.TimeoutError:
        logging.debug("Timer ran out")
    else:
        await rh.process_reaction(react)
        return

client.run(TOKEN)