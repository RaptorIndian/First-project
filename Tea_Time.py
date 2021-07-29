import discord
from dotenv import load_dotenv
import time

load_dotenv()
client = discord.Client()

localtime = time.asctime(time.localtime(time.time()))
localtime_call = "Local current time : ", localtime


@client.event
async def on_ready():
    print("We have attached to RPTR. ", localtime_call)
    

# Remembers what the player chose to do.
npc_memory = []
# The NPC chosen.
npc = ""
# Calculates the score based off the choices.
npc_score = 0
# Checks to see if Jay approved NPC.
availability_memory = False


def npc_preferences(npc_memory, stage, npc):
    global npc_score
    local_npc_score = 0
    if stage == "start":
        start_preferences = {
                "Jay": "Greetings", "Clyde": "Compliment", "Dale": "Compliment",
                "Cloe": "They Choose", "Micka": "Greetings", "Keith": "Greetings",
                "Jordan": "Crumpets", "Joey": "Crumpets", "Julie": "Tea", "Trent": "They Choose",
                "April": "They Choose", "Myra": "Crumpets", "Alura": "Napkins",
                "Fiona": "Greetings", "Ulric": "Napkins", "Mai": "Prayer", 
                "Coby": "Tea", "Elroy": "Compliment", "Dain": "Compliment", 
                "Katherine": "Compliment", "Gron": "Tea", "Xavier": "They Choose",
                "Conway": "Greetings", "Lilly": "Crumpets", "Zoku": "Tea",
                "Ken": "Compliment", "Nicole": "Crumpets"
                }
        if npc_memory in start_preferences:
            local_npc_score += 1
            npc_score += 1

        start_disinclinations = {
            "Jay": "Napkins", "Clyde": "Crumpets", "Dale": "Let Them Choose", "Cloe": "Prayer",
            "Micka": "Compliment", "Keith": "Crumpets", "Jordan": "Napkins", "Joey": "Tea",
            "Julie": "Prayer", "Trent": "Greetings", "April": "Napkins", "Myra": "Napkins",
            "Alura": "Compliment", "Fiona": "Tea", "Ulric": "Compliment", "Mai": "Let Them Choose",
            "Coby": "Prayer", "Elroy": "Crumpets", "Dain": "Let Them Choose", "Katherine": "Greetings",
            "Gron": "Prayer", " Xavier": "Prayer", "Conway": "Let Them Choose", "Lilly": "Prayer",
            "Zoku": "Crumpets", "Ken": "Prayer", "Nicole": "Napkins"
        }
        if npc_memory in start_disinclinations:
            local_npc_score += -1
            npc_score += -1
    
    if stage == "add":
        add_preferences = {
            "Jay": "Apple", "Clyde": "Elderberry", "Dale": "Chai", "Cloe": "Coffee Instead",
            "Micka": "Elderberry", "Keith": "Mint", "Jordan": "Lemon", "Joey": "Sugar",
            "Julie": "Coffee Instead", "Trent": "Mint", "April": "Apple",
            "Myra": "Lemon", "Alura": "Mint", "Fiona": "Coffee Instead",
            "Ulric": "Mint", "Mai": "Elderberry", "Coby": "Sugar", "Elroy": "Apple",
            "Dain": "Chai", "Katherine": "Lemon", "Gron": "Coffe Instead",
            "Xavier": "Sugar", "Conway": "Sugar", "Lilly": "Sugar", "Zoku": "Mint",
            "Ken": "Mint", "Nicole": "Elderberry"
        }
        if npc_memory in add_preferences:
            local_npc_score += 1
            npc_score += 1

        add_disinclinations = {
            "Jay": "Coffee", "Clyde": "Mint", "Dale": "Coffee", "Cloe": "Sugar", "Micka": "Apple",
            "Keith": "Sugar", "Jordan": "Mint", "Joey": "Coffee", "Julie": "Lemon", "Trent": "Chai",
            "April": "Coffee", "Myra": "Elderberry", "Alura": "Chai", "Fiona": "Mint", "Ulric": "Chai",
            "Mai": "Chai", "Coby": "Coffee", "Elroy": "Lemon", "Dain": "Sugar", "Katherine": "Mint",
            "Gron": "Sugar", "Xavier": "Apple", "Conway": "Mint", "Lilly": "Elderberry",
            "Zoku": "Elderberry", "Ken": "Coffee", "Nicole": "Mint"
        }
        if npc_memory in add_disinclinations:
            local_npc_score += -1
            npc_score += -1

    if stage == "topic":
        topic_preferences = {
            "Jay": "Responsibilities", "Clyde": "Love", "Dale": "Hobbies", "Cloe": "Gossip",
            "Micka": "Gossip", "Keith": "Responsibilities", "Jordan": "Hobbies", "Joey": "Funny",
            "Julie": "Responsibilities", "Trent": "Silence", "April": "Love", "Myra": "Funny",
            "Alura": "Love", "Fiona": "Love", "Ulric": "Funny", "Mai": "Small Talk",
            "Coby": "Silence", "Elroy": "Hobbies", "Dain": "Funny", "Katherine": "Gossip",
            "Gron": "Gossip", "Xavier": "Funny", "Conway": "Hobbies", "Lilly": "Hobbies",
            "Zoku": "Small Talk", "Ken": "Funny", "Nicole": "Silence"
        }
        if npc_memory in topic_preferences:
            local_npc_score += 1
            npc_score += 1
        
        topic_disinclinations = {
            "Jay": "Gossip", "Clyde": "Silence", "Dale": "Small Talk", "Cloe": "Love",
            "Micka": "Hobbies", "Keith": "Love", "Jordan": "Silence", "Joey": "Small Talk",
            "Julie": "Funny", "Trent": "Funny", "April": "Hobbies", "Myra": "Small Talk",
            "Alura": "Gossip", "Fiona": "Silence", "Ulric": "Gossip", "Mai": "Love",
            "Coby": "Hobbies", "Elroy": "Love", "Dain": "Silence", "Katherine": "Responsibilities",
            "Gron": "Hobbies", "Xavier": "Love", "Conway": "Silence", "Lilly": "Small Talk",
            "Zoku": "Funny", "Ken": "Responsibilities", "Nicole": "Small Talk"
        }
        if npc_memory in topic_disinclinations:
            local_npc_score += -1
            npc_score += -1
        
    if local_npc_score == 0:
        return ""
    if local_npc_score == 1:
        return f"{npc} liked that."
    if local_npc_score == -1:
        return f"{npc} disliked that."


@client.event
async def on_message(message):
    global npc_memory
    global npc
    global npc_score
    global availability_memory
    if message.author == client.user:
        return
    # Turn string into list of many strings based off the amount of spaces.
    list = message.content.split(" ")
    if message.content.startswith("$tea ") and availability_memory == False:
        npc = list[1]
        print(localtime_call)
        player = message.author.mention
        await message.channel.send('Someone wants tea time \n<@335453916051275778>')
    if message.content.startswith("$no"):
        if message.author.id == '335453916051275778':
            availability_memory = False
            await message.channel.send(f"{npc} does not want to have tea right now.")
    if message.content.startswith("$yes"):
        if message.author.id == '335453916051275778':
            availability_memory = True
            await message.channel.send(f'What will you and {npc} start with, {player}? \n Tea, Crumpets, Napkins, Prayer, Greetings, Compliment, or They Choose?')
    if message.content.startswith("$start") and availability_memory == True:
        npc_memory[0] = list[1]
        await message.channel.send(f"{npc_preferences(npc_memory, 'start', npc)} Will you add anything to the tea? \n Sugar, Mint, Lemon, Elderberry, Apple, Chai, or Nothing?")
    if message.content.startswith("$add") and availability_memory == True:
        npc_memory[1] = list[1]
        await message.channel.send(f"{npc_preferences(npc_memory, 'add', npc)} What will you talk about? \nFunny, Love, Responsibilities, Small Talk, Silence, Gossip, or Hobbies?")
    if message.content.startswith("$topic") and availability_memory == True:
        npc_memory[2] = list[1]
        availability_memory = False
        await message.channel.send(f"{npc_preferences(npc_memory, 'add', npc)}")
        