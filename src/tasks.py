from discord.ext import tasks, commands

class TaskClass(commands.Cog):
    def __init__(self):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(minutes=1.0)
    async def timer(self):
        print(self.index)
        self.index += 1