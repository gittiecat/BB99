from database import DatabaseClass
from stats import StatsClass
import discord
import random
from datetime import datetime
from shlex import split
import asyncio

client = discord.Client()

wdb = DatabaseClass()
all_words = wdb.getAllWords()
del wdb

jed_appreciate = False

def jedAppreciate():
    return not jed_appreciate

def splitMessage(message):
    split_message = split(message.content)
    return split_message

@client.event
async def on_read():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    ### DO NOT MOVE - MUST ALWAYS BE ON TOP
    if message.author == client.user:
        return

    global jed_appreciate

    if message.content.startswith("$jed") and not str(message.author) == "Jed#4434":
        jed_appreciate = jedAppreciate()
        print(jed_appreciate)
        if jed_appreciate == True:
            await message.add_reaction(emoji="🔇")
        else:
            await message.add_reaction(emoji="🔊")
        return

    if str(message.author) == "Jed#4434" and jed_appreciate == True:
        r = int(random.random()*10)
        if r == 0:
            await message.channel.send("")
        return

    ### NOT COMMANDS - MONITOR CHAT
    if not message.content.startswith('$'):
        if str(message.author) == "Jed#4434" and "valheim" in str(message.content).lower():
            await message.add_reaction(emoji="❤")
            await message.author.send("Hey, man! I just want to tell you that we all appreciate you very much and that I really like your dedication for this 'Valheim' game. I hope we play together at some point!")
            return

        num = int(random.random()*50)
        if num == 0:
            await message.channel.send("I agree with this statement.")
            return
        if num == 1:
            await message.channel.send("I respect your opinion but I have to disagree.")
            return
        elif 'pog' in str(message.content).lower():
            await message.add_reaction("<:PogU:784563515716665364>")
            return

        for w in all_words:
            db = DatabaseClass()
            if w in str(message.content).lower():
                db.addToCount(w)
        del db
    ##########

    if message.content.startswith("$s4y"):
        params = splitMessage(message)
        send = " ".join(params[1:])
        s = client.guilds[0].text_channels[0]
        await s.send(send)
        return

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
 
    ### OVERWATCH ACCOUNT STATS
    if message.content.startswith('$acc'):
        params = splitMessage(message)
        acc = StatsClass(params[1], message.author)
        await message.channel.send(acc.toMessage())
    ##########

    ### HELP MESSAGE
    if message.content.startswith('$help'):
        help_message = "Hi! I am a bot for the **{server}** server!\n"
        help_message = help_message + "1) $help - to get help\n"
        help_message = help_message + "2) $badwordstats <no. top(optional)> - get the stats on the top bad words of the server!\n"
        help_message = help_message + "3) $badwordnew <word> - add a new bad word to the list of bad words!\n"
        help_message = help_message + "4) $acc <BattleTag> - to get account info (must be public!)\n"
        help_message = help_message + "5) $hi - say hello to me and I'll respond back!\n"
        help_message = help_message + "6) $jed - mute Jed whenever you want if he gets annoying!"\
                            .format(server = message.guild)
        await message.channel.send(help_message)
        return
    ########## EASY TO READ FORMAT

    ### SAY HELLO TO MESSAGE AUTHOR
    if message.content.startswith('$hi'):
        send = 'Hello, ' + str(message.author) + '!'
        await message.channel.send(send)
        return
    ##########


client.run('ODg2MjIxMTE3ODAxNTAwNzAy.YTybuw.yGf3-crpCBmFn6bRjL6z3UsuHBM')