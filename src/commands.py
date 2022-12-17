import discord
from database import DatabaseClass
from image_processor import ImageProcessor
from openai_impl.dalle2 import GenDallE2
from valheim import ValheimClass
from shlex import split
import re


error_emoji = "\U0001F6B1"

class CommandsListener:
    @classmethod
    async def process_commands(cls, message, client):
        self = CommandsListener()
        self.client = client
        self.message = message
        msg_array = message.content.split(" ")
        self.base_command = msg_array[0]
        self.param_command = msg_array[1:]
        self.response = await processor(self)
        return self

async def processor(self):
    match self.base_command:
        case "$hi":
            await com_hi(self)
        case "$help":
            await com_help(self)
        case "$acc":
            await com_acc(self)
        case "$jed":
            await com_jed(self)
        case "$ro":
            await com_ro(self)
        case "$valheim":
            await com_valheim(self)
        case "$bored":
            await com_bored(self)
        case "$badwordstats":
            await com_bw_stats(self)
        case "$badwordnew":
            await com_bw_new(self)
        case "$generate":
            await com_generate(self)
        case _:
            await com_help(self, True)

async def com_generate(self):
    message = str(self.message.content)
    user = str(self.message.author)
    remove_command = message.replace("$generate ", "")
    command_list = re.findall(r'\$\w*', remove_command)
    size = None
    num = 1
    flag = False
    for command in command_list[:2]:
        comm = command[1:]
        if (comm in ['small', 'medium', 'large']):
            size = comm
        if (re.match("^[1-9]$|^10$", comm)):
            num = comm

    
    prompt_word_list = [word for word in remove_command.split() if word.lower() not in command_list]
    prompt = ' '.join(prompt_word_list)
    
    gen = GenDallE2()
    response = gen.generate(prompt, size, num)
    if isinstance(response, str):
        await self.message.channel.send("OpenAI: *" + response + "*")
    else:
        for img in response["data"]:
            image_path = ImageProcessor.create_image(img["b64_json"])
            await self.message.channel.send(file=discord.File(image_path))
    
async def com_bored(self):
    isAuthor = str(self.message.author) == "strööp#6969"
    if not isAuthor:
        return
    db = DatabaseClass()
    switch = db.checkSwitches("bored")[0][0]
    reverse = (switch+1)%2
    db.reverseSwitch(reverse, "bored")
    if reverse == 1:
        await self.message.add_reaction("💢")
    else:
        await self.message.add_reaction("😒")

async def com_hi(self):
    author = self.message.author.mention
    greetings_file = open("resources/greetings_list.txt", "r", encoding="utf8") # read greetings from file
    greetings_list = greetings_file.read().split("\n")
    rand = random.randrange(1,len(greetings_list))
    response = greetings_list[rand].format(author)
    await self.message.channel.send(response)

async def com_help(self, err=False):
    if err == True:
        help_message = "This command does not exist! \"$help\" provides a list all available commands.\n---\n"
    else:
        help_message = "Hi! I am a bot for the **{server}** server!\n".format(server = self.message.guild)
    help_file = open("resources/help_list.txt", "r", encoding="utf8") # read help messages from file
    help_list = help_file.read().split("\n")
    
    for idx, commands in enumerate(help_list, start=1):
        mod_string = str(idx) + ") " + commands + "\n"
        help_message += mod_string
    await self.message.channel.send(help_message)

async def com_acc(self):
    # if not self.param_command:
    #     await self.message.add_reaction(error_emoji)
    #     return
    # params = self.param_command[0]
    # acc = StatsClass(params, self.message.author)
    # response = acc.toMessage()
    # await self.message.channel.send(acc.toMessage())
    await self.message.channel.send("This functionality has been temporarily disabled until Blizzard fix their bloody api")
    return

async def com_jed(self):
    if str(self.message.author) == "Jed#4434":
        return
    db = DatabaseClass()
    switch = db.checkSwitches("jed_appreciate")[0][0]
    reverse = (switch+1)%2
    db.reverseSwitch(reverse, "jed_appreciate")
    if reverse == 1:
        await self.message.add_reaction("💙")
    else:
        await self.message.add_reaction("💔")

async def com_ro(self):
    if str(self.message.author) == "Stokey™#9852":
        return
    db = DatabaseClass()
    switch = db.checkSwitches("ro_troll")[0][0]
    reverse = (switch+1)%2
    db.reverseSwitch(reverse, "ro_troll")
    if reverse == 1:
        await self.message.add_reaction("😈")
    else:
        await self.message.add_reaction("😇")

async def com_valheim(self):
    command = self.param_command[0]
    user = str(self.message.author)
    if command in ["start", "restart", "status"]:
        val = ValheimClass(command)
        response = val.response
        await self.message.channel.send(response)

def splitMessage(message):
        split_message = split(message.content)
        return split_message

async def com_bw_stats(self):
    params = splitMessage(self.message)
    if (len(params) == 2 and params[1].isnumeric()):
        num_top = params[1]
    else:
        num_top = 3
    db = DatabaseClass()
    await self.message.channel.send(db.getTopWords(num_top))

async def com_bw_new(self):
    db = DatabaseClass()
    all_words = db.getAllWords()
    if (len(all_words) < 25):
        params = splitMessage(self.message)
        db.addNewWord(params[1])
        all_words.append(params[1])
        await self.message.add_reaction("<a:Clap:788103361622179901>")
    else:
        await self.message.channel.send("You have reached limit of bad words.")

