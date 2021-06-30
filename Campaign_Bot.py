#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import standard libraries
import numpy as np #numpy is great since it has a variety of function
import time
import discord
import os
import itertools, random
import re
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

localtime = time.asctime( time.localtime(time.time()) )
localtime_call = "Local current time : ",localtime

@client.event
async def on_ready():
  print('We have logged in as RPTR. ', localtime_call)
# In[2]:


def gen_states() -> np.ndarray:
    """
    Generates 12 random integers between 1 and 100, as if rolling
    a d100 die.
    Returns: Array-like with numbers between 1 and 100 of length 12
    """
    chance=np.random.randint(1,101,12) # Python generally doesn't include the end number
    return chance

def comp(chance,growths):
    """
    Compares each value of chance with growths to determine if chance is
    lower or equal to growths.
    Parameters:
        chance: Array-like containing integers in the range of 0 to 100
        growths: Array-like of the same length as chance containing integers
    Returns:
        inc: A boolean list (True/False) where True means chance was lower
             than growths
    """
    inc=[]
    for pos,i in enumerate(chance): # enumerate counts the position and gives it to pos (comparison function), i means index
        growth=growths[pos]
        if growth>100: # A check for if the growth is over 100%
            growth=growth-100
        if i <= growth: # The check to see if the value is less than or equal
            inc.append(True)
        else: 
            inc.append(False)
    return inc

def get_results(chance,growths):
    """
    Finds and prints what was obtained for the level up and the corresponding
    stats for the given chance and growth.
    Parameters:
        chance: array-like containing integers in the range of 0 to 100
        growths: array-like of the same length as chance containing integers
    Returns:
        get: Array-like containing the strings for which stats where increased
    """
    stats=['HP','STR' ,'MAG','SKL','SPD','LCK','DEF','RES','CON','CHA','INT','INV']
    num=len(stats) # Just to avoid random floating numbers
    increase=comp(chance,growths)
    content = 'Values rolled: \n'
    get=[]
    print('Values rolled: \n')
    for i in range(num):
        print(stats[i]+': '+str(chance[i]),'/ '+str(growths[i])) # This can be changed as desired
        content = content + str(stats[i])+': '+str(chance[i])+' / '+str(growths[i])+'\n'
        if growths[i]>100: # Checks to see if growth is greater than 100
            get.append(stats[i]) # if true, automatically adds stat to get
        if increase[i]==True: # Check to see if this stat was increased
            get.append(stats[i]) 
    return get, content

def get_lvlup(growths):
    """
    The main function to determine what is increased from the level up in a
    single neat function
    Parameters:
        growths: array-like of the same length as chance containing integers
    Returns: None, simply prints
    """
    chance=gen_states()
    got, content = get_results(chance, growths)
    return got, content



# In[6]:


# Starting with the first option, different files for every characters

directory = '.'
characters_directory = directory + '/Characters/'
gambling_hall_directory = "./Gambling Hall/ghall.txt"

def get_growths1(name):
    """
    Obtaines the growths from a file on the computer within a designated folder
    Parameters:
        name: String containing the character name to find the correct file
    Returns:
        growths: Dictionary containing the growths in integer value, along with a
                 string if they are capped and thus need to be ignored.
    """
    # First need to open and read the file
    filename=characters_directory+name+".txt"
    full_file=[]
    try:
        with open(filename,'rb') as fid: # Will close the file after the information has been pulled
            for line in fid:
                line=line.decode('cp1252').upper().split()
                line[1]=int(line[1])
                full_file.append(line)
    except FileNotFoundError:
        print("Error: Character not found!\nPlease ensure you have typed the name correctly and"                " that the first letter is capitalized.")   
    # Create a dictionary for easy reference of each growth
    growths={}
    for line in full_file:
        growths[line[0]]=line[1:]
        
    return growths

# This does however require a slight variation to the get_results() function
# in order to accomidate the use of a dictionary


def overwrite_char(name,growths):
    """
    
    """
    filename=characters_directory+name+".txt"

    with open(filename,'r+') as fid:
        new_file=''
        for stat,val in growths.items():
            new_line=stat.lower()
            for i in val:
                new_line=str(new_line+' '+str(i))
            new_file=new_file+new_line+'\n'
        fid.truncate() # New line added which was causing all the problems with remove_cap()
        fid.write(new_file)

def remove_cap(name,stat):
    """
    
    """
    stat=stat.upper()
    items=get_growths1(name)
    if stat.lower()=='all':
        print('Removing All.')
        for stat in items:
            remove_cap(name,stat)
    else:
        if len(items[stat])<2:
            print(name+"'s "+'stat is already uncapped.')
            return False
        else:
            items[stat]=[items[stat][0]]
            overwrite_char(name,items)
            print(name+"'s",stat.upper(),'is no longer capped')
            return True

def cap_it(name,stat):
    """
    
    """
    stat=stat.upper()
    items=get_growths1(name)
    if len(items[stat])>1:
        print('This stat is already capped')
        return False
    else:
        items[stat].append('capped')
        overwrite_char(name,items)
        print(name+"'s",stat.upper(),'is now capped.')
        return True


def update_growth(name,stat,val):
    """
    
    """
    stat=stat.upper()
    items=get_growths1(name)
    items[stat][0]=val
    overwrite_char(name,items)
    print(name+"'s ",stat.upper(),' has been updated to ', val)
    return True



gambling_hall_skill = {
'Clyde': 0, 'Dale': 0,
'Alura': 1, 'Jordan': 1, 'Micka': 1,
'Cloe': 2, 'Gron': 2, 'Joey': 2,
'Keith': 3, 'Xavier': 3, 'Myra': 3, 'Nobody': 0
}

chance_to_leave = {
'Clyde': 5, 'Dale': 20,
'Alura': 5, 'Jordan': 20, 'Micka': 15,
'Cloe': 20, 'Gron': 15, 'Joey': 5,
'Keith': 10, 'Xavier': 1, 'Myra': 15, 'Nobody': 0
}





def card_game(name):

    # make a deck of cards
    deck = list(itertools.product(range(1,14),['Spades','Hearts','Diamonds','Clubs']))
    if gambling_hall_skill[name] == 0:

        # shuffle the cards
        shuffle_amount = np.random.randint(1,51,1)
        count = 0
        while count < shuffle_amount:
            random.shuffle(deck)
            count += 1

        # draw five cards for the player
        player_hand = []
        for i in range(6):
            player_hand += [deck[i]]

        # shuffle the cards
        shuffle_amount = np.random.randint(1,51,1)
        count = 0
        while count < shuffle_amount:
            random.shuffle(deck)
            count +=1
        results = []
        npc_hand = []

        # draw five cards for the npc
        for i in range(6):
            npc_hand.append([deck[i][0], deck[i][1]])
        print(npc_hand)
        # choose a random number from the ordered list and subtract a random number
        random_card_index = np.random.randint(1,7)
        manip = npc_hand[random_card_index][0]
        sub = np.random.randint(3,8,1)
        sum = manip - sub[0]
        stuff = np.random.randint(1,4)
        sum = sum if sum > 0 else stuff
        npc_hand[random_card_index][0] = sum

        # format the list into a single string
        def format(var0, var1, var2, var3, var4, var5):
            return f'{var0}, {var1}, {var2}, {var3}, {var4}, and a {var5}'
        results = (f"**You got:** {format(*player_hand)}\n**{name} got:** {format(*npc_hand)}")
        return results
        
    if gambling_hall_skill[name] == 1:

        # shuffle the cards
        shuffle_amount = np.random.randint(1,51,1)
        count = 0
        while count < shuffle_amount:
            random.shuffle(deck)
            count += 1

        # draw five cards for the player
        player_hand = []
        for i in range(6):
            player_hand += [deck[i]]

        # shuffle the cards
        shuffle_amount = np.random.randint(1,51,1)
        count = 0
        while count < shuffle_amount:
            random.shuffle(deck)
            count +=1
        npc_hand = (f"**{name} got:** \n")
        results = []
        npc_hand = []

        # draw five cards for the npc
        for i in range(6):
            npc_hand += [deck[i]]

        # format the list into a single string
        def format(var0, var1, var2, var3, var4, var5):
            return f'{var0}, {var1}, {var2}, {var3}, {var4}, and a {var5}'
        results = (f"**You got:** {format(*player_hand)}\n**{name} got:** {format(*npc_hand)}")
        return results

print(card_game('Clyde'))

def RPS_loss(choice):
    if choice == 'rock':
        NPC_choice = 'paper'
    elif choice == 'paper':
        NPC_choice = 'scissors'
    elif choice == 'scissors':
        NPC_choice = 'rock'
    return NPC_choice

def RPS_win(choice):
    if choice == 'rock':
        NPC_choice = 'scissors'
    elif choice == 'paper':
        NPC_choice = 'rock'
    elif choice == 'scissors':
        NPC_choice = 'paper'
    return NPC_choice
    
def RPS_tie(choice):
    if choice == 'rock':
        NPC_choice = 'rock'
    elif choice == 'paper':
        NPC_choice = 'paper'
    elif choice == 'scissors':
        NPC_choice = 'scissors'
    return NPC_choice

def NPC_RPS_calc(chance, skill, choice, name):
    if skill == 0:
        if chance <= 25:
            result = str(name+' chose '+RPS_loss(choice)+'. You lose.')
        elif chance > 25 and chance <= 60:
            result = str(name+' chose '+RPS_win(choice)+'. You win!')
        elif chance > 60:
            result = str(name+' chose '+RPS_tie(choice)+'. You tied!')
    if skill == 1:
        if chance <= 33:
            result = str(name+' chose '+RPS_loss(choice)+'. You lose.')
        elif chance > 33 and chance <= 66:
            result = str(name+' chose '+RPS_win(choice)+'. You win!')
        elif chance > 66:
            result = str(name+' chose '+RPS_tie(choice)+'. You tied!')
    if skill == 2:
        if chance <= 40:
            result = str(name+' chose '+RPS_loss(choice)+'. You lose.')
        elif chance > 40 and chance <= 80:
            result = str(name+' chose '+RPS_win(choice)+'. You win!')
        elif chance > 80:
            result = str(name+' chose '+RPS_tie(choice)+'. You tied!')
    if skill == 3:
        if chance <= 80:
            result = str(name+' chose '+RPS_loss(choice)+'. You lose.')
        elif chance > 80 and chance <= 90:
            result = str(name+' chose '+RPS_win(choice)+'. You win!')
        elif chance > 90:
            result = str(name+' chose '+RPS_tie(choice)+'. You tied!')
    leave_calc = np.random.randint(1,101,1)        
    if leave_calc <= chance_to_leave.get(name):
        result += ' ' + name + ' has left the gambling hall. '
        filename=gambling_hall_directory
        with open(filename, 'wt') as fid:
            name = 'Nobody'
            fid.write(name)
    return result

def RPS_game(name, choice):
    skill = gambling_hall_skill[name]
    if name == 'Xavier':
        cheating = np.random.randint(1,101,1)
        if cheating <= 7:
            result = 'You caught Xavier cheating! He forfeits all his money for getting caught.'
            return result
    if skill == 0:
        chance = np.random.randint(1,101,1)
        result = NPC_RPS_calc(chance, skill, choice, name)
        return result
    if skill == 1:
        chance = np.random.randint(1,101,1)
        result = NPC_RPS_calc(chance, skill, choice, name)
        return result
    if skill == 2:
        chance = np.random.randint(1,101,1)
        result = NPC_RPS_calc(chance, skill, choice, name)
        return result
    if skill == 3:
        chance = np.random.randint(1,101,1)
        result = NPC_RPS_calc(chance, skill, choice, name)
        return result

localtime = time.asctime( time.localtime(time.time()) )
localtime_call = "Local current time : ",localtime

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    list = message.content.split(' ')  #Turn string into list of many strings based off the amount of spaces
    if message.content.startswith('$lvlup '): # $lvlup Thor
        print(localtime_call)
        name = list[1]
        records = [message.author.nick, name]
        print(records)
        growths = get_growths1(name)
        enumerated_growths = []
        for index, key in enumerate(growths.items()):
            enumerated_growths.insert(index, key[1][0])
        lvl = get_lvlup(enumerated_growths)
        if not growths: # If the player has typed the name wrong
            await message.channel.send("Error: Character not found!\nPlease ensure you have typed the name correctly and"              " that the first letter is capitalized.")
        elif not lvl: # Checks if the list is empty, designating a Null Level up and rerolling
            count = 0
            while not lvl and count < 6:
                channel = client.get_channel(847979864862883850)
                await channel.send(name+ " got a Null Level up!\nRerolling ...\n")
                lvl = get_lvlup(enumerated_growths)
                count += 1
                if count >5:
                    lvl = ["nothing."]
                    await message.channel.send("Too many Null levels ups in a row. Wow you're unlucky!")
        await message.channel.send(lvl[1]+'----------------\n'+name+' got '+ ', '.join(lvl[0]))
    list = message.content.split(' ')
    if message.content.startswith('$uncap '):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
        if authorized:
            name = list[1]
            stat = list[2]
            cap = remove_cap(name,stat)
            if cap:
                await message.channel.send(name+"'s "+stat+" has been uncapped.")
            else:
                await message.channel.send(name+"'s "+stat+" is already uncapped.")
        else:
            await message.channel.send('Only Jay may use this feature.')
    if message.content.startswith('$cap '):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
        if authorized:
            name = list[1]
            stat = list[2]
            was_capped = cap_it(name,stat)
            if was_capped:
                await message.channel.send(name+"'s "+stat.upper()+' is now capped.')
            else:
                await message.channel.send('This stat is already capped')
        else:
            await message.channel.send('Only Jay may use this feature.')
    if message.content.startswith('$update '):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
            if authorized:
                name = list[1]
                stat = list[2]
                value = list[3]
                update = update_growth(name,stat,value)
                if update:
                    await message.channel.send(name+"'s "+stat.upper()+' has been updated to '+value+".")
        else:
            await message.channel.send('Only Jay may use this feature.')
    if message.content.startswith('$stats '):
        print(localtime_call)
        name = list[1]
        growths=get_growths1(name)
        variable = '**' + name + "'s" + ' growths' ':' + '**' + '\n'
        stats=['HP','STR' ,'MAG','SKL','SPD','LCK','DEF','RES','CON','CHA','INT','INV']
        for key in stats:
            line=key.upper()+':'
            val=growths[key]
            for i in val:
                line=str(line+' '+str(i))
            variable=variable+line+'\n'
        records = [message.author.nick, name]
        print(records)
        print(variable)
        await message.channel.send(variable)
    if message.content.startswith('$inhall '):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
            if authorized:
                filename=gambling_hall_directory
                with open(filename, 'wt') as fid:
                    name = list[1]
                    fid.write(name)
                #gambling = in_gambling_hall(name)
                await message.channel.send(name+' is now in the gambling hall.')
        else:
            await message.channel.send('Only Jay may use this feature.')
    if message.content.startswith('$rps '):
        print(localtime_call)
        # filename='C:\\Users\\Raptor\\Desktop\\Discord Bot\\Gambling Hall\\ghall.txt'
        # with open(filename, 'r') as fid:
        #     name = list[1]
        # if name == 'Nobody' or 'nobody':
        #     await message.channel.send('Nobody is in the gambling hall right now, come back later.')
        # else:
        filename=gambling_hall_directory
        with open(filename, 'r+') as fid:
            for line in fid:
                npc = line.split()
            name = npc[0]
        choice = list[1]
        if name == 'Nobody':
            await message.channel.send("There's nobody in the gambling hall.")
        else:
            result = RPS_game(name, choice)
            await message.channel.send(result)
    if message.content.startswith('$create '):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
            if authorized:
                name = str(list[1]).title()
                path = characters_directory
                new_file = os.path.join(path, name+".txt")
                if os.path.isfile(new_file):
                    await message.channel.send(name+' already exists.')
                else:
                    with open(new_file, 'wt') as fid:
                        fid.write('')
                    stats = ['HP','STR' ,'MAG','SKL','SPD','LCK','DEF','RES','CON','CHA','INT','INV']
                    growths = {}
                    for item in stats:
                        growths[item] = [0]
                    overwrite_char(name, growths)
                    await message.channel.send(name+' has been created.')
    if message.content.startswith('$cards'):
        filename=gambling_hall_directory
        with open(filename, 'r+') as fid:
            for line in fid:
                npc = line.split()
            name = npc[0]
        if name == 'Nobody':
            await message.channel.send("There's nobody in the gambling hall.")
        else:
            result = card_game(name)
            await message.channel.send(result)
    
    if message.content.startswith('$test '):
        print(localtime_call)
        await message.channel.send(client.get_user(335453916051275778))



# @client.command()
# async def ping(ctx):
#     admin = client.get_user(335453916051275778)
#     await ctx.send(f"{admin.mention}")
    








client.run(os.getenv('token'))


# %%
