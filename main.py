from commands import CommandsListener
from tasks import TaskClass
from database import DatabaseClass
from stats import StatsClass
import discord
import random
from datetime import datetime
from shlex import split
import os
from dotenv import load_dotenv
import subprocess
import logging
import platform
from timeit import default_timer as timer
from datetime import timedelta

# create these files to enable logging
LOGFILE_ERROR = 'bot_error.log'
LOGFILE_ALL = 'bot.log'
logging.basicConfig(filename=LOGFILE_ERROR, level=logging.ERROR)
logging.basicConfig(filename=LOGFILE_ALL, level=logging.DEBUG)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# init client
client = discord.Client()

# testing cog
# cog = TaskClass(client)

wdb = DatabaseClass()
all_words = wdb.getAllWords()
del wdb

jed_appreciate = False
ro_troll = False

def jedAppreciate():
    return not jed_appreciate

def roTroll():
    return not ro_troll

def splitMessage(message):
    split_message = split(message.content)
    return split_message

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
    global jed_appreciate
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
            subprocess.run(['/home/misha/dev/BB99/update.sh'], shell=True)
            await message.channel.send("Finished update!")
        except Exception as e:
            logging.error(e)
            await message.channel.send("Update has failed - please check the logs for more details.")
        return
    
    ### Process commands
    if message.content.startswith("$"):
        await CommandsListener.process_commands(message)

    ### COMMAND LISTENERS 
    if message.content.startswith("$jed") and not str(message.author) == "Jed#4434":
        jed_appreciate = jedAppreciate()
        if jed_appreciate:
            await message.add_reaction(emoji="💙")
            await message.channel.send("We are now appreciating Jed!")
        else:
            await message.add_reaction(emoji="💔")
        return

    if message.content.startswith("$ro") and not str(message.author) == "Stokey™#9852":
        ro_troll = roTroll()
        if ro_troll:
            await message.add_reaction(emoji="😈")
        else:
            await message.add_reaction(emoji="😇")
        return

    if str(message.author) == "Stokey™#9852" and ro_troll:
        await message.add_reaction(emoji = "<:bronzerank:890252007468838984>")

    if str(message.author) == "Jed#4434" and jed_appreciate:
        r = int(random.random()*30)
        if r == 0:
            await message.channel.send("I'm with you 100%!")
        elif r == 1:
            await message.channel.send("That's a very good point, Jed.")
        elif r == 2:
            await message.channel.send("Hey, I think we should all play Valheim some day.")
        elif r == 3:
            await message.channel.send("Sending you lots of love and kisses 💙")
        elif r == 4:
            await message.add_reaction(emoji="🙌")
        elif r == 5:
            await message.add_reaction(emoji="😍")
        elif r == 6:
            await message.add_reaction(emoji="💯")
        elif r == 7:
            await message.add_reaction(emoji="🔥")
        return
    
    if message.content.startswith("$s4y"):
        params = splitMessage(message)
        send = " ".join(params[1:])
        s = client.guilds[0].text_channels[0]
        await s.send(send)
        await message.delete()
        return

    ### NOT COMMANDS - MONITOR CHAT
    if not message.content.startswith('$'):
        if str(message.author) == "Jed#4434" and ("valheim" in str(message.content).lower()):
            await message.add_reaction(emoji="❤")
            await message.channel.send("Buy the game here: https://store.steampowered.com/app/892970/Valheim/")
            await message.author.send("Hey, man! I just want to tell you that we all appreciate you very much and that I really like your dedication for this 'Valheim' game. I hope we play together at some point!")
            return

        num = int(random.random()*500)
        if num == 0:
            await message.channel.send("I agree with this statement.")
            return
        if num == 1:
            await message.channel.send("I respect your opinion but I have to disagree.")
            return
        elif 'pog' in str(message.content).lower():
            await message.add_reaction("<:PogU:784563515716665364>")
            return

        db = DatabaseClass()
        for w in all_words:
            if w in str(message.content).lower():
                db.addToCount(w)
        del db
    ##########
    
    ### OVERWATCH ACCOUNT STATS
    if message.content.startswith('$acc'):
        params = splitMessage(message)
        start_time = timer()
        acc = StatsClass(params[1], message.author)
        logging.debug(timedelta(seconds=timer()-start_time))
        await message.channel.send(acc.toMessage())
    ##########
    
    ### EVENT COMMANDS
    if message.content.startswith("$event"):
        params = splitMessage(message)
        if (len(params) < 4):
            await message.add_reaction("👎")
            return
        category = params[1]
        # date parser
        date = params[2]
        print(date.split("/")[2])
        try:
            if (date == "today"):
                date = datetime.today().strftime("%d/%m/%y")
            else:
                date = datetime.strptime(date,"%d/%m/%y")
        except ValueError as err:
            print(err)
        time = params[3]
        comments = " ".join(params[4:])
        print(comments)
    ##########

    ### BAD WORDS COMMANDS
    if message.content.startswith("$badwordstats"):
        params = splitMessage(message)
        if (len(params) == 2 and params[1].isnumeric()):
            num_top = params[1]
        else:
            num_top = 3
        db = DatabaseClass()
        await message.channel.send(db.getTopWords(num_top))

    if message.content.startswith('$badwordnew'):
        if (len(all_words) < 25):
            params = splitMessage(message)
            db = DatabaseClass()
            db.addNewWord(params[1])
            all_words.append(params[1])
            await message.add_reaction("<a:Clap:788103361622179901>")
        else:
            await message.channel.send("You have reached limit of bad words.")
    ##########

client.run(TOKEN)
