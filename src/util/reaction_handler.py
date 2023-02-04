
import discord
from spongebob import SpongebobClass


class ReactionHandler():

    def __init__(self, message):
        self.reaction_list = self.get_reaction_list()
        self.message = message

    async def process_reaction(self, reaction):
        idx = 0
        for key, value in enumerate(reaction):
            if isinstance(value, discord.reaction.Reaction):
                idx = key
        
        r = reaction[idx].emoji.name
        if r == "SpongebobMock":
            await self.spongebob(self.message)

    def check(self, reaction):
        return str(reaction.emoji) in self.reaction_list

    def get_reaction_list(self):
        return ["SpongebobMock"]

    async def spongebob(self, message):
        response = SpongebobClass().spongebob_format(message.content)
        await self.message.channel.send(response)