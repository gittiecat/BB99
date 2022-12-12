
import random
from database import DatabaseClass


class ChatMonitoring:
    @classmethod
    async def chat_monitor(cls, message):
        self = ChatMonitoring()
        self.message = message
        self.response = await createResponse(self)

async def createResponse(self):
    message = self.message
    if str(message.author) != "strööp#6969" and \
                    not not DatabaseClass().checkSwitches("bored")[0][0]:
        await message.channel.send("?")
        await message.add_reaction("❓")

    if str(message.author) == "Stokey™#9852" and \
                        not not DatabaseClass().checkSwitches("ro_troll")[0][0]:
        await message.add_reaction(emoji = "<:bronzerank:890252007468838984>")

    if str(message.author) == "Jed#4434" and \
                        not not DatabaseClass().checkSwitches("jed_appreciate")[0][0]:
        appreciateJed(message)

    if not message.content.startswith('$'):
        if str(message.author) == "Jed#4434" and ("valheim" in str(message.content).lower()):
            await message.add_reaction(emoji="❤")
            await message.channel.send("Buy the game here: https://store.steampowered.com/app/892970/Valheim/")
        
        if 'pog' in str(message.content).lower():
            await message.add_reaction("<:PogU:784563515716665364>")
        
        db = DatabaseClass()
        all_words = db.getAllWords()
        for w in all_words:
            if w in str(message.content).lower():
                db.addToCount(w)
        del db
        
        num = int(random.random()*500)
        if num == 0:
            await message.channel.send("I agree with this statement.")
        if num == 1:
            await message.channel.send("I respect your opinion but I have to disagree.")

async def appreciateJed(message):
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