import random

class CommandsListener:
    @classmethod
    async def process_commands(cls, message):
        self = CommandsListener()
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
        case _:
            await com_help(self, True)

async def com_hi(self):
    author = self.message.author.mention
    greetings_file = open("greetings_list.txt", "r", encoding="utf8") # read greetings from file
    greetings_list = greetings_file.read().split("\n")
    rand = random.randrange(1,len(greetings_list))
    response = greetings_list[rand].format(author)
    await self.message.channel.send(response)

async def com_help(self, err=False):
    if err == True:
        help_message = "This command does not exist! \"$help\" provides a list all available commands.\n---\n"
    else:
        help_message += "Hi! I am a bot for the **{server}** server!\n".format(server = self.message.guild)
    help_file = open("help_list.txt", "r", encoding="utf8") # read help messages from file
    help_list = help_file.read().split("\n")
    
    for idx, commands in enumerate(help_list, start=1):
        mod_string = str(idx) + ") " + commands + "\n"
        help_message += mod_string
    await self.message.channel.send(help_message)