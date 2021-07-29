import discord
from dotenv import load_dotenv
import time
import os


load_dotenv()
client = discord.Client()

localtime = time.asctime(time.localtime(time.time()))
localtime_call = "Local current time : ", localtime


@client.event
async def on_ready():
    print("We have attached to RPTR. ", localtime_call)
    

# Remembers what the player chose to do.
npc_memory = ''
# The NPC chosen.
npc = ""
# Calculates the score based off the choices.
npc_score = 0
# Checks to see if Jay approved NPC.
availability_memory = False
# Makes sure you can't request tea time when someone is alreadu queue'd.
wait = 'No'
# Stores the user id who requested tea time.
user = ''
# Stores the user nickname.
user2 = ''
# Makes all prompts don't happen at the same time.
status = 0


def npc_preferences(npc_memory, stage, npc):
    global npc_score
    local_npc_score = 0
    if stage == "start":
        start_preferences = {
                "Jay": "$$Greetings", "Clyde": "$$Compliment", "Dale": "$$Compliment",
                "Cloe": "$$Them", "Micka": "$$Greetings", "Keith": "$$Greetings",
                "Jordan": "$$Crumpets", "Joey": "$$Crumpets", "Julie": "$$Tea", "Trent": "$$Them",
                "April": "$$Them", "Myra": "$$Crumpets", "Alura": "$$Napkins",
                "Fiona": "$$Greetings", "Ulric": "$$Napkins", "Mai": "$$Prayer", 
                "Coby": "$$Tea", "Elroy": "$$Compliment", "Dain": "$$Compliment", 
                "Katherine": "$$Compliment", "Gron": "$$Tea", "Xavier": "$$Them",
                "Conway": "$$Greetings", "Lilly": "$$Crumpets", "Zoku": "$$Tea",
                "Ken": "$$Compliment", "Nicole": "$$Crumpets"
                }
        if npc_memory in start_preferences:
            local_npc_score += 1
            npc_score += 1

        start_disinclinations = {
            "Jay": "$$Napkins", "Clyde": "$$Crumpets", "Dale": "Let $$Them Choose", "Cloe": "$$Prayer",
            "Micka": "$$Compliment", "Keith": "$$Crumpets", "Jordan": "$$Napkins", "Joey": "$$Tea",
            "Julie": "$$Prayer", "Trent": "$$Greetings", "April": "$$Napkins", "Myra": "$$Napkins",
            "Alura": "$$Compliment", "Fiona": "$$Tea", "Ulric": "$$Compliment", "Mai": "Let $$Them Choose",
            "Coby": "$$Prayer", "Elroy": "$$Crumpets", "Dain": "Let $$Them Choose", "Katherine": "$$Greetings",
            "Gron": "$$Prayer", " Xavier": "$$Prayer", "Conway": "Let $$Them Choose", "Lilly": "$$Prayer",
            "Zoku": "$$Crumpets", "Ken": "$$Prayer", "Nicole": "$$Napkins"
        }
        if npc_memory in start_disinclinations:
            local_npc_score += -1
            npc_score += -1
    
    if stage == "add":
        add_preferences = {
            "Jay": "$$Apple", "Clyde": "$$Elderberry", "Dale": "$$Chai", "Cloe": "$$Coffee",
            "Micka": "$$Elderberry", "Keith": "$$Mint", "Jordan": "$$Lemon", "Joey": "$$Sugar",
            "Julie": "$$Coffee", "Trent": "$$Mint", "April": "$$Apple",
            "Myra": "$$Lemon", "Alura": "$$Mint", "Fiona": "$$Coffee",
            "Ulric": "$$Mint", "Mai": "$$Elderberry", "Coby": "$$Sugar", "Elroy": "$$Apple",
            "Dain": "$$Chai", "Katherine": "$$Lemon", "Gron": "$$Coffee",
            "Xavier": "$$Sugar", "Conway": "$$Sugar", "Lilly": "$$Sugar", "Zoku": "$$Mint",
            "Ken": "$$Mint", "Nicole": "$$Elderberry"
        }
        if npc_memory in add_preferences:
            local_npc_score += 1
            npc_score += 1

        add_disinclinations = {
            "Jay": "$$Coffee", "Clyde": "$$Mint", "Dale": "$$Coffee", "Cloe": "$$Sugar", "Micka": "$$Apple",
            "Keith": "$$Sugar", "Jordan": "$$Mint", "Joey": "$$Coffee", "Julie": "$$Lemon", "Trent": "$$Chai",
            "April": "$$Coffee", "Myra": "$$Elderberry", "Alura": "$$Chai", "Fiona": "$$Mint", "Ulric": "$$Chai",
            "Mai": "$$Chai", "Coby": "$$Coffee", "Elroy": "$$Lemon", "Dain": "$$Sugar", "Katherine": "$$Mint",
            "Gron": "$$Sugar", "Xavier": "$$Apple", "Conway": "$$Mint", "Lilly": "$$Elderberry",
            "Zoku": "$$Elderberry", "Ken": "$$Coffee", "Nicole": "$$Mint"
        }
        if npc_memory in add_disinclinations:
            local_npc_score += -1
            npc_score += -1

    if stage == "topic":
        topic_preferences = {
            "Jay": "$$Responsibilities", "Clyde": "$$Love", "Dale": "$$Hobbies", "Cloe": "$$Gossip",
            "Micka": "$$Gossip", "Keith": "$$Responsibilities", "Jordan": "$$Hobbies", "Joey": "$$Funny",
            "Julie": "$$Responsibilities", "Trent": "$$Silence", "April": "$$Love", "Myra": "$$Funny",
            "Alura": "$$Love", "Fiona": "$$Love", "Ulric": "$$Funny", "Mai": "$$$$Smalltalk",
            "Coby": "$$Silence", "Elroy": "$$Hobbies", "Dain": "$$Funny", "Katherine": "$$Gossip",
            "Gron": "$$Gossip", "Xavier": "$$Funny", "Conway": "$$Hobbies", "Lilly": "$$Hobbies",
            "Zoku": "$$$$Smalltalk", "Ken": "$$Funny", "Nicole": "$$Silence"
        }
        if npc_memory in topic_preferences:
            local_npc_score += 1
            npc_score += 1
        
        topic_disinclinations = {
            "Jay": "$$Gossip", "Clyde": "$$Silence", "Dale": "$$$$Smalltalk", "Cloe": "$$Love",
            "Micka": "$$Hobbies", "Keith": "$$Love", "Jordan": "$$Silence", "Joey": "$$$$Smalltalk",
            "Julie": "$$Funny", "Trent": "$$Funny", "April": "$$Hobbies", "Myra": "$$$$Smalltalk",
            "Alura": "$$Gossip", "Fiona": "$$Silence", "Ulric": "$$Gossip", "Mai": "$$Love",
            "Coby": "$$Hobbies", "Elroy": "$$Love", "Dain": "$$Silence", "Katherine": "$$Responsibilities",
            "Gron": "$$Hobbies", "Xavier": "$$Love", "Conway": "$$Silence", "Lilly": "$$$$Smalltalk",
            "Zoku": "$$Funny", "Ken": "$$Responsibilities", "Nicole": "$$Smalltalk"
        }
        if npc_memory in topic_disinclinations:
            local_npc_score += -1
            npc_score += -1

    if local_npc_score == 0:
        return "They didn't think much of that. 0"
    if local_npc_score == 1:
        return f"{npc} liked that. +1"
    if local_npc_score == -1:
        return f"{npc} disliked that. -1"

def npc_score_end_result(npc_score):
    if npc_score == 0:
        result = f"{npc} thanked you for the tea, but they felt it was a tad uneventful. Total: 0 loyalty."
    if npc_score == 1:
        result = f"{npc} liked the tea. Total: +1 loyalty!"
    if npc_score == 2:
        result = f"{npc} had a fun time today. Total: +2 loyalty!!"
    if npc_score == 3: 
        result = f"{npc} loved spending time with you Total: +3 loyalty!!!"
    if npc_score == -1:
        result = f"{npc} politely thanked you but left in a hurry Total: -1 loyalty."
    if npc_score == -2:
        result = f"{npc} seems put off by this exchange Total: -2 loyalty."
    if npc_score == -3:
        result = f"{npc} made an excuse to leave early Total: -3 loyalty."
    return result

@client.event
async def on_message(message):
    global npc_memory
    global npc
    global npc_score
    global availability_memory
    global wait
    global user
    global user2
    global status
    if message.author == client.user:
        return
    # Turn string into list of many strings based off the amount of spaces.
    list = message.content.split(" ")
    npcs_to_choose_from = [
                            "Jay", "Clyde", "Dale", "Cloe", "Micka", "Keith", "Jordan", "Joey,"
                            "Julie", "Trent", "April", "Myra", "Alura", "Fiona", "Ulric", "Mai",
                            "Coby", "Elroy", "Dain", "Katherine", "Gron", "Xavier", "Lilly",
                            "Zoku", "Ken", "Nicole"
                            ]
    if message.content.startswith("$tea ") and availability_memory == False and wait == 'No':
        npc = list[1]
        if npc in npcs_to_choose_from:
            print(localtime_call)
            wait = 'Yes'
            user = f'{message.author.mention}'
            user2 = f'{message.author.nick}'
            await message.channel.send('Someone wants tea time! \n<@335453916051275778>')
        else:
            await message.channel.send("Invalid NPC.")
    elif message.content.startswith("$tea ") and availability_memory == False and wait == 'Yes':
        await message.channel.send(f"{user2} is already waiting for a response.")
    if message.content.startswith("$no"):
        if message.author.id in [335453916051275778]:
            availability_memory = False
            wait = 'No'
            await message.channel.send(f"{npc} does not want to have tea right now.")
    if message.content.startswith("$yes"):
        if message.author.id in [335453916051275778]:
            availability_memory = True
            await message.channel.send(f'What will you and {npc} start with, {user}? \n Tea, Crumpets, Napkins, Prayer, Greetings, Compliment, or let Them choose?')
    if message.content.startswith("$") and availability_memory == True:
        await message.channel.send(f"{npc} is currently having tea time with {user2}.")
    if message.content.startswith("$$") and availability_memory == True and status == 2:
        npc_memory = list[0]
        availability_memory = False
        wait = 'No'
        user = ''
        await message.channel.send(f"{npc_preferences(npc_memory, 'topic', npc)} \n {npc_score_end_result(npc_score)}")
    if message.content.startswith("$$") and availability_memory == True and status == 1:
        npc_memory = list[0]
        status = 2
        await message.channel.send(f"{npc_preferences(npc_memory, 'add', npc)} \nWhat will you talk about? \nFunny, Love, Responsibilities, Smalltalk, Silence, Gossip, or Hobbies?")
    if message.content.startswith("$$") and availability_memory == True and status == 0:
        npc_memory = list[0]
        status = 1
        await message.channel.send(f"{npc_preferences(npc_memory, 'start', npc)} \nWill you add anything to the tea? \nSugar, Mint, Lemon, Elderberry, Apple, Chai, or drink Coffee instead?")

client.run(os.getenv('token'))