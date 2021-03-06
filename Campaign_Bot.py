#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import standard libraries
import numpy as np  # numpy is great since it has a variety of function
import time
import discord
import os
import itertools, random
import re
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

localtime = time.asctime(time.localtime(time.time()))
localtime_call = "Local current time : ", localtime


@client.event
async def on_ready():
    print("We have logged in as RPTR. ", localtime_call)


# In[2]:


def gen_states() -> np.ndarray:
    """
    Generates 12 random integers between 1 and 100, as if rolling
    a d100 die.
    Returns: Array-like with numbers between 1 and 100 of length 12
    """
    chance = np.random.randint(
        1, 101, 12
    )  # Python generally doesn't include the end number
    return chance


def comp(chance, growths):
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
    inc = []
    for pos, i in enumerate(
        chance
    ):  # enumerate counts the position and gives it to pos (comparison function), i means index
        growth = growths[pos]
        if growth > 100:  # A check for if the growth is over 100%
            growth = growth - 100
        if i <= growth:  # The check to see if the value is less than or equal
            inc.append(True)
        else:
            inc.append(False)
    return inc


def get_results(chance, growths):
    """
    Finds and prints what was obtained for the level up and the corresponding
    stats for the given chance and growth.
    Parameters:
        chance: array-like containing integers in the range of 0 to 100
        growths: array-like of the same length as chance containing integers
    Returns:
        get: Array-like containing the strings for which stats where increased
    """
    stats = [
        "HP",
        "STR",
        "MAG",
        "SKL",
        "SPD",
        "LCK",
        "DEF",
        "RES",
        "CON",
        "CHA",
        "INT",
        "INV",
    ]
    num = len(stats)  # Just to avoid random floating numbers
    increase = comp(chance, growths)
    content = "Values rolled: \n"
    get = []
    print("Values rolled: \n")
    for i in range(num):
        print(
            stats[i] + ": " + str(chance[i]), "/ " + str(growths[i])
        )  # This can be changed as desired
        content = (
            content
            + str(stats[i])
            + ": "
            + str(chance[i])
            + " / "
            + str(growths[i])
            + "\n"
        )
        if growths[i] > 100:  # Checks to see if growth is greater than 100
            get.append(stats[i])  # if true, automatically adds stat to get
        if increase[i] == True:  # Check to see if this stat was increased
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
    chance = gen_states()
    got, content = get_results(chance, growths)
    return got, content


# In[6]:


# Starting with the first option, different files for every characters

directory = "."
characters_directory = directory + "/Characters/"
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
    filename = characters_directory + name + ".txt"
    full_file = []
    try:
        with open(
            filename, "rb"
        ) as fid:  # Will close the file after the information has been pulled
            for line in fid:
                line = line.decode("cp1252").upper().split()
                line[1] = int(line[1])
                full_file.append(line)
    except FileNotFoundError:
        print(
            "Error: Character not found!\nPlease ensure you have typed the name correctly and"
            " that the first letter is capitalized."
        )
    # Create a dictionary for easy reference of each growth
    growths = {}
    for line in full_file:
        growths[line[0]] = line[1:]

    return growths


# This does however require a slight variation to the get_results() function
# in order to accomidate the use of a dictionary


def overwrite_char(name, growths):
    """ """
    filename = characters_directory + name + ".txt"

    with open(filename, "r+") as fid:
        new_file = ""
        for stat, val in growths.items():
            new_line = stat.lower()
            for i in val:
                new_line = str(new_line + " " + str(i))
            new_file = new_file + new_line + "\n"
        fid.truncate()  # New line added which was causing all the problems with remove_cap()
        fid.write(new_file)


def remove_cap(name, stat):
    """ """
    stat = stat.upper()
    items = get_growths1(name)
    if stat.lower() == "all":
        print("Removing All.")
        for stat in items:
            remove_cap(name, stat)
    else:
        if len(items[stat]) < 2:
            print(name + "'s " + "stat is already uncapped.")
            return False
        else:
            items[stat] = [items[stat][0]]
            overwrite_char(name, items)
            print(name + "'s", stat.upper(), "is no longer capped")
            return True


def cap_it(name, stat):
    """ """
    stat = stat.upper()
    items = get_growths1(name)
    if len(items[stat]) > 1:
        print("This stat is already capped")
        return False
    else:
        items[stat].append("capped")
        overwrite_char(name, items)
        print(name + "'s", stat.upper(), "is now capped.")
        return True


def update_growth(name, stat, val):
    """ """
    stat = stat.upper()
    items = get_growths1(name)
    items[stat][0] = val
    overwrite_char(name, items)
    print(name + "'s ", stat.upper(), " has been updated to ", val)
    return True


gambling_hall_skill = {
    "Clyde": 0,
    "Dale": 0,
    "Alura": 1,
    "Jordan": 1,
    "Micka": 1,
    "Cloe": 2,
    "Gron": 2,
    "Joey": 2,
    "Keith": 3,
    "Xavier": 3,
    "Myra": 3,
    "Nobody": 0,
    "nobody": 0
}

chance_to_leave = {
    "Clyde": 17,
    "Dale": 20,
    "Alura": 20,
    "Jordan": 25,
    "Micka": 25,
    "Cloe": 20,
    "Gron": 25,
    "Joey": 17,
    "Keith": 25,
    "Xavier": 20,
    "Myra": 25,
    "Nobody": 0,
    "nobody": 0
}


# Manipulate the cards that the NPC recieves:
# EASY: Less likely to get high numbers, less likley to get duplicate numbers, less likely to get straights.
# NORMAL: Normal RNG.
# HARD: More likely to get high numbers.
# INSANE: More likely to get high numbers, duplicate numbers, and straights.


def shuffle(deck):
    # shuffle the cards
    shuffle_amount = np.random.randint(1, 51, 1)
    count = 0
    while count < shuffle_amount:
        random.shuffle(deck)
        count += 1

# def shuffle(deck):
#     # shuffle the cards
#     shuffle_amount = np.random.randint(1, 51)
#     for _ in range(shuffle_amount):
#         random.shuffle(deck)

# Makes sure you can't get multiple of the same card.
def exists_in_hand(hand, new_card):
    for old_card in hand:
        if old_card[0] == new_card[0] and old_card[1] == new_card[1]:
            return True
    return False


# Makes card number pairs only able to happen once.
def has_pairs(hand, new_card):
    for old_card in hand:
        if old_card[0] == new_card[0]:
            return True
    return False


# Lowers the likelihood of getting a straight.
def has_straight(hand, new_card):
    for old_card in hand:
        if old_card[0] == new_card[0] + 1 or old_card[0] == new_card[0] - 1:
            return True
    return False

def has_four_of_a_kind(hand, new_card):
    count_array: list[int] = [0] * 13
    temp_hand = hand.copy()
    temp_hand.append(new_card)
    # Accumulate the possible of-a-kinds
    for value in temp_hand:
        count_array[value[0] - 1] += 1

    # BEDMAS: brackets, exponents, divide, multiply, addition, subtraction
    # Calculate and return the scores
    for num in count_array:
        if num > 3:
            return True
    return False

# Creates the NPC's deck.
def deal0(deck, hand_size):
    hand = []
    count = 0
    count2 = 0
    count3 = 0
    while len(hand) < hand_size:
        card = deck[0]
        if card[0] > 9:
            if count3 < 3:
                count3 += 1
                shuffle(deck)
                continue

        if exists_in_hand(hand, card):
            shuffle(deck)
            continue

        if has_pairs(hand, card):
            if card[0] < 10 and count < 1:
                count += 1
            else:
                shuffle(deck)
                continue

        if has_straight(hand, card):
            if count2 < 3:
                count2 += 1
                shuffle(deck)
                continue

        hand.append(card)
        shuffle(deck)
    return hand


def deal2(deck, hand_size):
    hand = []
    count = 0
    while len(hand) < hand_size:
        card = deck[0]
        if exists_in_hand(hand, card):
            shuffle(deck)
            continue
        
        if card[0] < 4 and count < 1:
            count += 1
            shuffle(deck)
            continue

        hand.append(card)
        shuffle(deck)
    return hand


def deal3(deck, hand_size):
    hand = []
    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    rndm = np.random.randint(1, 50, 1)
    card = deck[0]
    hand.append(card)
    shuffle(deck)
    while len(hand) < hand_size:
        card = deck[0]
        if exists_in_hand(hand, card):
            shuffle(deck)
            continue

        if len(hand) < 2:
            chance = np.random.randint(1, 3)
            if chance == 1:
                if card[0] > 9:
                    shuffle(deck)
                    continue

        if card[0] < 6 and count < 20:
            count += 1
            shuffle(deck)
            continue

        if not has_pairs(hand, card) and count2 < 14 and rndm <= 35:
            count2 += 1
            shuffle(deck)
            continue

        if not has_straight(hand, card) and count3 < 27 and rndm >35:
            count3 += 1
            shuffle(deck)
            continue

        if len(hand) > 2 and has_four_of_a_kind(hand, card):
            count4 += 1
            shuffle(deck)
            continue


        hand.append(card)
        shuffle(deck)
    return hand

def deal_kanan(deck, hand_size):
    hand = []
    count = 0
    while len(hand) < hand_size:
        card = deck[0]
        if exists_in_hand(hand, card):
            shuffle(deck)
            continue

        if card[0] < 2 and count < 3:
            count += 1
            shuffle(deck)
            continue

        hand.append(card)
        shuffle(deck)
    return hand

def scan_for_of_a_kind(hand_values) -> list[int]:
    count_array: list[int] = [0] * 13

    # Accumulate the possible of-a-kinds
    for value in hand_values:
        count_array[value - 1] += 1

    # BEDMAS: brackets, exponents, divide, multiply, addition, subtraction
    # Calculate and return the scores
    score_array: list[int] = list()
    index: int = 1
    for num in count_array:
        if num > 1:
            score_array.append((num - 1) * index)
        index += 1

    return score_array

def scan_for_has_four_of_a_kind(hand_values, old_score) -> int:
    count_array: list[int] = [0] * 13

    # Accumulate the possible of-a-kinds
    for value in hand_values:
        count_array[value - 1] += 1

    # BEDMAS: brackets, exponents, divide, multiply, addition, subtraction
    # Calculate and return the scores
    score = old_score
    for num in count_array:
        if num > 3:
            score = 1000

    return score


def scan_for_straight(hand_values) -> int:
    score = 0

    count_array: list[int] = [0] * 13

    # Count the cards
    for value in hand_values:
        count_array[value - 1] += 1

    # Count the longest stretch of counted cards
    longest_count = 0
    current_count = 0
    for value in count_array:
        if value > 0:
            current_count += 1
        else:
            longest_count = (
                current_count if current_count > longest_count else longest_count
            )
            current_count = 0

    if longest_count == 3:
        score = 5
    elif longest_count > 3:
        score = 5 + (longest_count - 3 * 2)

    return score


def count_points(hand) -> int:
    total_score = 0

    of_a_kind_score = scan_for_of_a_kind(hand)
    for score in of_a_kind_score:
        total_score += score

    # Second, count the straights.
    total_score += scan_for_straight(hand)

    # Third, cound base points.
    total_score += sum(hand)

    total_score = scan_for_has_four_of_a_kind(hand, total_score)

    return total_score


def card_game(name, kanan_skill):
    if kanan_skill == 0:
        if name == "Xavier":
            cheating = np.random.randint(1, 101, 1)
            if cheating <= 7:
                result = "You caught Xavier cheating! He forfeits all his money for getting caught."
                result += " " + name + " has left the gambling hall. "
                filename = gambling_hall_directory
                with open(filename, "wt") as fid:
                    name = "Nobody"
                    fid.write(name)
                    return result

        # make a deck of cards
        deck = list(
            itertools.product(range(1, 14), ["Spades", "Hearts", "Diamonds", "Clubs"])
        )
        # Logic depending on the skill of the NPC skill
        if gambling_hall_skill[name] == 0:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1

            # draw five cards for the player
            player_hand = []
            for i in range(6):
                player_hand += [deck[i]]
            deck = deck [ 6 : -1 : 1 ]

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            npc_hand = []
            npc_hand = deal0(deck, 6)

        if gambling_hall_skill[name] == 1:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1

            # draw five cards for the player
            player_hand = []
            for i in range(6):
                player_hand += [deck[i]]
                deck = deck [ 6 : -1 : 1 ]

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            npc_hand = f"**{name} got:** \n"
            results = []
            npc_hand = []

            # draw five cards for the npc
            for i in range(6):
                npc_hand += [deck[i]]

        # Logic depending on the skill of the NPC skill
        if gambling_hall_skill[name] == 2:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 3, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1

            # draw five cards for the player
            player_hand = []
            for i in range(6):
                player_hand += [deck[i]]
            deck = deck [ 6 : -1 : 1 ]
            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            npc_hand = []
            npc_hand = deal2(deck, 6)

        if gambling_hall_skill[name] == 3:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1

            # draw five cards for the player
            player_hand = []
            for i in range(6):
                player_hand += [deck[i]]
            deck = deck [ 6 : -1 : 1 ]

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            npc_hand = []
            npc_hand = deal3(deck, 6)

        # Game logic
        player_points = 0
        npc_points = 0

        # Sets the card numbers up to be checked.
        pcard0 = player_hand[0][0]
        pcard1 = player_hand[1][0]
        pcard2 = player_hand[2][0]
        pcard3 = player_hand[3][0]
        pcard4 = player_hand[4][0]
        pcard5 = player_hand[5][0]
        # ph stands for player hand.
        ph = [pcard0, pcard1, pcard2, pcard3, pcard4, pcard5]

        ncard0 = npc_hand[0][0]
        ncard1 = npc_hand[1][0]
        ncard2 = npc_hand[2][0]
        ncard3 = npc_hand[3][0]
        ncard4 = npc_hand[4][0]
        ncard5 = npc_hand[5][0]
        # nh stands for npc hand.
        nh = [ncard0, ncard1, ncard2, ncard3, ncard4, ncard5]

        player_points += count_points(ph)
        npc_points += count_points(nh)

        if player_points > npc_points:
            card_game_result = f"You win!"
        elif npc_points > player_points:
            card_game_result = f"{name} won!"
        elif player_points == npc_points:
            card_game_result = f"You tied!"

        # format the list into a single string
        def format(var0, var1, var2, var3, var4, var5):
            return f"{format_card(var0)}, {format_card(var1)}, {format_card(var2)}, {format_card(var3)}, {format_card(var4)}, and a {format_card(var5)}"
        
        # Change 1 11 12 and 13 to Ace Jack Queen King.
        def format_card(card):
            if card[0] == 1:
                return f"{'Ace'} of {card[1]}"
            if card[0] == 11:
                return f"{'Jack'} of {card[1]}"
            if card[0] == 12:
                return f"{'Queen'} of {card[1]}"
            if card[0] == 13:
                return f"{'King'} of {card[1]}"
            else:
                return f"{card[0]} of {card[1]}"
        
        if player_points > 999 and npc_points > 999:
            results = (f"**You got:** {format(*player_hand)} which has a four-of-a-kind!!.\n**{name} got:** {format(*npc_hand)} which has a four-of-a-kind!!. \n**You tied?!?!**")
            return results
        elif player_points > 999:
            results = (f"**You got:** {format(*player_hand)} which adds up to **{player_points}**.\n**{name} got:** {format(*npc_hand)} which adds up to **{npc_points}**. \n**{card_game_result}**")
            return results
        elif npc_points > 999:
            results = (f"**You got:** {format(*player_hand)} which adds up to **{player_points}**.\n**{name} got:** {format(*npc_hand)} which adds up to **{npc_points}**. \n**{card_game_result}**")
            return results
        else:
            results = (f"**You got:** {format(*player_hand)} which adds up to **{player_points}**.\n**{name} got:** {format(*npc_hand)} which adds up to **{npc_points}**. \n**{card_game_result}**")
            return results
    if kanan_skill == 1:
        if name == "Xavier":
            cheating = np.random.randint(1, 101, 1)
            if cheating <= 7:
                result = "You caught Xavier cheating! He forfeits all his money for getting caught."
                result += " " + name + " has left the gambling hall. "
                filename = gambling_hall_directory
                with open(filename, "wt") as fid:
                    name = "Nobody"
                    fid.write(name)
                    return result

        # make a deck of cards
        deck = list(
            itertools.product(range(1, 14), ["Spades", "Hearts", "Diamonds", "Clubs"])
        )
        # Logic depending on the skill of the NPC skill
        if gambling_hall_skill[name] == 0:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            player_hand = []
            player_hand = deal_kanan(deck, 6)

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            npc_hand = []
            npc_hand = deal0(deck, 6)

        if gambling_hall_skill[name] == 1:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            player_hand = []
            player_hand = deal_kanan(deck, 6)

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            npc_hand = f"**{name} got:** \n"
            results = []
            npc_hand = []

            # draw five cards for the npc
            for i in range(6):
                npc_hand += [deck[i]]

        # Logic depending on the skill of the NPC skill
        if gambling_hall_skill[name] == 2:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            player_hand = []
            player_hand = deal_kanan(deck, 6)

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            npc_hand = []
            npc_hand = deal2(deck, 6)

        if gambling_hall_skill[name] == 3:

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            player_hand = []
            player_hand = deal_kanan(deck, 6)

            # shuffle the cards
            shuffle_amount = np.random.randint(1, 51, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            results = []
            npc_hand = []
            npc_hand = deal3(deck, 6)

        # Game logic
        player_points = 0
        npc_points = 0

        # Sets the card numbers up to be checked.
        pcard0 = player_hand[0][0]
        pcard1 = player_hand[1][0]
        pcard2 = player_hand[2][0]
        pcard3 = player_hand[3][0]
        pcard4 = player_hand[4][0]
        pcard5 = player_hand[5][0]
        # ph stands for player hand.
        ph = [pcard0, pcard1, pcard2, pcard3, pcard4, pcard5]

        ncard0 = npc_hand[0][0]
        ncard1 = npc_hand[1][0]
        ncard2 = npc_hand[2][0]
        ncard3 = npc_hand[3][0]
        ncard4 = npc_hand[4][0]
        ncard5 = npc_hand[5][0]
        # nh stands for npc hand.
        nh = [ncard0, ncard1, ncard2, ncard3, ncard4, ncard5]

        player_points += count_points(ph)
        npc_points += count_points(nh)

        if player_points > npc_points:
            card_game_result = f"You win!"
        elif npc_points > player_points:
            card_game_result = f"{name} won!"
        elif player_points == npc_points:
            card_game_result = f"You tied!"

        # format the list into a single string
        def format(var0, var1, var2, var3, var4, var5):
            return f"{format_card(var0)}, {format_card(var1)}, {format_card(var2)}, {format_card(var3)}, {format_card(var4)}, and a {format_card(var5)}"

        def format_card(card):
            return f"{card[0]} of {card[1]}"
        if player_points > 999 and npc_points > 999:
            results = (f"**You got:** {format(*player_hand)} which has a four-of-a-kind!!.\n**{name} got:** {format(*npc_hand)} which has a four-of-a-kind!!. \n**You tied?!?!**")
        elif player_points > 999:
            results = (f"**You got:** {format(*player_hand)} which adds up to **{player_points}**.\n**{name} got:** {format(*npc_hand)} which adds up to **{npc_points}**. \n**{card_game_result}**")
        elif npc_points > 999:
            results = (f"**You got:** {format(*player_hand)} which adds up to **{player_points}**.\n**{name} got:** {format(*npc_hand)} which adds up to **{npc_points}**. \n**{card_game_result}**")
        else:
            results = (f"**You got:** {format(*player_hand)} which adds up to **{player_points}**.\n**{name} got:** {format(*npc_hand)} which adds up to **{npc_points}**. \n**{card_game_result}**")

        leave_calc = np.random.randint(1, 101, 1)
        if leave_calc <= chance_to_leave.get(name):
            results += "\n" + name + " has left the gambling hall. <@335453916051275778>"
            filename = gambling_hall_directory
            with open(filename, "wt") as fid:
                name = "Nobody"
                fid.write(name)
    return results



def RPS_loss(choice):
    if choice == "rock":
        NPC_choice = "paper"
    elif choice == "paper":
        NPC_choice = "scissors"
    elif choice == "scissors":
        NPC_choice = "rock"
    return NPC_choice


def RPS_win(choice):
    if choice == "rock":
        NPC_choice = "scissors"
    elif choice == "paper":
        NPC_choice = "rock"
    elif choice == "scissors":
        NPC_choice = "paper"
    return NPC_choice


def RPS_tie(choice):
    if choice == "rock":
        NPC_choice = "rock"
    elif choice == "paper":
        NPC_choice = "paper"
    elif choice == "scissors":
        NPC_choice = "scissors"
    return NPC_choice


def NPC_RPS_calc(chance, skill, choice, name):
    if skill == 0:
        if chance <= 25:
            result = str(name + " chose " + RPS_loss(choice) + ". You lose.")
        elif chance > 25 and chance <= 60:
            result = str(name + " chose " + RPS_win(choice) + ". You win!")
        elif chance > 60:
            result = str(name + " chose " + RPS_tie(choice) + ". You tied!")
    if skill == 1:
        if chance <= 33:
            result = str(name + " chose " + RPS_loss(choice) + ". You lose.")
        elif chance > 33 and chance <= 66:
            result = str(name + " chose " + RPS_win(choice) + ". You win!")
        elif chance > 66:
            result = str(name + " chose " + RPS_tie(choice) + ". You tied!")
    if skill == 2:
        if chance <= 40:
            result = str(name + " chose " + RPS_loss(choice) + ". You lose.")
        elif chance > 40 and chance <= 80:
            result = str(name + " chose " + RPS_win(choice) + ". You win!")
        elif chance > 80:
            result = str(name + " chose " + RPS_tie(choice) + ". You tied!")
    if skill == 3:
        if chance <= 80:
            result = str(name + " chose " + RPS_loss(choice) + ". You lose.")
        elif chance > 80 and chance <= 90:
            result = str(name + " chose " + RPS_win(choice) + ". You win!")
        elif chance > 90:
            result = str(name + " chose " + RPS_tie(choice) + ". You tied!")
    leave_calc = np.random.randint(1, 101, 1)
    if leave_calc <= chance_to_leave.get(name):
        result += "\n" + name + " has left the gambling hall. <@335453916051275778>"
        filename = gambling_hall_directory
        with open(filename, "wt") as fid:
            name = "Nobody"
            fid.write(name)
    return result


def RPS_game(name, choice, kanan_skill):
    if kanan_skill == 0:
        skill = gambling_hall_skill[name]
        if name == "Xavier":
            cheating = np.random.randint(1, 101, 1)
            if cheating <= 7:
                result = "You caught Xavier cheating! He forfeits all his money for getting caught."
                result += " " + name + " has left the gambling hall. "
                filename = gambling_hall_directory
                with open(filename, "wt") as fid:
                    name = "Nobody"
                    fid.write(name)
                return result
        if skill == 0:
            chance = np.random.randint(1, 101, 1)
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
        if skill == 1:
            chance = np.random.randint(1, 101, 1)
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
        if skill == 2:
            chance = np.random.randint(1, 101, 1)
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
        if skill == 3:
            chance = np.random.randint(1, 101, 1)
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
    elif kanan_skill == 1:
        skill = gambling_hall_skill[name]
        if name == "Xavier":
            cheating = np.random.randint(1, 101, 1)
            if cheating <= 7:
                result = "You caught Xavier cheating! He forfeits all his money for getting caught."
                result += " " + name + " has left the gambling hall. "
                filename = gambling_hall_directory
                with open(filename, "wt") as fid:
                    name = "Nobody"
                    fid.write(name)
                return result
        if skill == 0:
            chance = np.random.randint(1, 101, 1)
            chance += 5
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
        if skill == 1:
            chance = np.random.randint(1, 101, 1)
            chance += 5
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
        if skill == 2:
            chance = np.random.randint(1, 101, 1)
            chance += 5
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result
        if skill == 3:
            chance = np.random.randint(1, 101, 1)
            chance += 5
            result = NPC_RPS_calc(chance, skill, choice, name)
            return result

localtime = time.asctime(time.localtime(time.time()))
localtime_call = "Local current time : ", localtime

tarot_memory = []

def pull_tarot_card(player_name):
    global tarot_memory
    good_cards = [
                    f"Lion: {player_name} gains +4 Lck and Skl. They also gain 1 movement.",
                    f"Eagle: {player_name} gains +4 Spd and Int. They also are not hindered by forest tiles.",
                    f"Bear: {player_name} gains +4 Str and Defense. They also can't be critically hit.",
                    f"Dragon: {player_name} gains +4 Mag and Res. They also intimidate foes."
    ]
    neutral_cards = [
                    f"Dagger: {player_name} gains a new weapon, but they lose a sum of gold for it.",
                    f"Arrow: {player_name} gains a Forge Coin, but they lose 1 stamina for the week.",
                    f"Flame: Nothing changes for {player_name}.",
                    f"Flower: {player_name} gains a new statbooster, but will be cursed with bad luck in the next rp session."
    ]
    bad_cards = [
                    f"Broken Bone: {player_name} loses 4 Def and Spd. They also lose 1 movement.",
                    f"Serpent: {player_name} loses 4 Cha and Str. They also start the next map poisoned.",
                    f"Target: {player_name} loses 20 Avoid. They also draw more aggro.",
                    f"Devil: {player_name} is struck with a random curse."
        ]
    chance = np.random.randint(1, 13, 1)
    # chance = np.random.randint(1, 13) returns a single integer, don't add size!
    if chance <= 4:
        card_chance = np.random.randint(0, 4)
        if card_chance == tarot_memory:
            chance_to_get_same_card = np.random.randint(0,2)
            if chance_to_get_same_card == 0:
                card_chance = np.random.randint(0, 4)
        result = good_cards[card_chance]
    if chance > 4 and chance <= 8:
        card_chance = np.random.randint(0, 4)
        if card_chance == tarot_memory:
            chance_to_get_same_card = np.random.randint(0,2)
            if chance_to_get_same_card == 0:
                card_chance = np.random.randint(0, 4)
        result = neutral_cards[card_chance]
    if chance > 8:
        card_chance = np.random.randint(0, 4)
        if card_chance == tarot_memory:
            chance_to_get_same_card = np.random.randint(0,2)
            if chance_to_get_same_card == 0:
                card_chance = np.random.randint(0, 4)
        if card_chance == 0:
            chance_to_get_broken_bone = np.random.randint(0,2)
            if chance_to_get_broken_bone == 0:
                card_chance = np.random.randint(0, 4)
        result = bad_cards[card_chance]
    result += '\n<@335453916051275778>'
    tarot_memory = card_chance
    return result

def custom_dice_roll(num_of_dice, sides):
    sides = sides + 1
    count = 0
    result = ''
    if num_of_dice > 30:
        result = 'You cannot roll more than 30 dice at once.'
    elif sides > 10001:
        result = 'You cannot roll a dice with more than 10,000 sides.'
    else:
        while count < num_of_dice:
            result += f'{np.random.randint(1, sides)} \n'
            count += 1
    
    return result


# The go fish card game.
def go_fish(npc, kanan_skill, player_name):
    # Change 1 11 12 and 13 to Ace Jack Queen King.
    def format_card(card):
        if card[0] == 1:
            return f"{'Ace'} of {card[1]}"
        if card[0] == 11:
            return f"{'Jack'} of {card[1]}"
        if card[0] == 12:
            return f"{'Queen'} of {card[1]}"
        if card[0] == 13:
            return f"{'King'} of {card[1]}"
        else:
            return f"{card[0]} of {card[1]}"
    # Change 1 11 12 and 13 to Ace Jack Queen King, but for the NPC's card pick.
    def special_formatting(card):
        if card == 1:
            return 'Aces'
        if card == 11:
            return 'Jacks'
        if card == 12:
            return 'Queens'
        if card == 13:
            return 'Kings'
        else:
            return str(card) + "'s"
    
    # Determine who goes first.
    who_goes_first = np.random.randint(0,1)
    if who_goes_first == 0:
        # Checks for Kanan skill.
        if kanan_skill == 0:
            # Makes a deck of cards.
            deck = list(
                itertools.product(range(1, 14), ["Spades", "Hearts", "Diamonds", "Clubs"])
            )
            shuffle(deck)
            # Shuffle the cards a lot.
            shuffle_amount = np.random.randint(1, 31, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            # Draw 7 cards for the NPC's hand.
            npc_hand = []
            for i in range(7):
                npc_hand += [deck[i]]
            deck = deck [ 7 : -1 : 1 ]
            # Organize NPC's hand.
            npc_hand = sorted(npc_hand)
            # Shuffle the cards a lot.
            shuffle_amount = np.random.randint(1, 31, 1)
            count = 0
            while count < shuffle_amount:
                random.shuffle(deck)
                count += 1
            # Draw 7 cards for the player's hand.
            player_hand = []
            for i in range(7):
                player_hand += [deck[i]]
            deck = deck [ 7 : -1 : 1 ]
            # Organize player's hand.
            player_hand = sorted(player_hand)
            old_player_hand = sorted(player_hand)
            # NPC picks a random card from its deck to ask for.
            # Checks the skill level of the NPC.
            if gambling_hall_skill[npc] == 0:
                #chance = np.random.randint(0,101)
                chance = 19
                if chance <= 20:
                    count = 0
                    temp_list1 = []
                    temp_list2 = []
                    while count < 10:
                        random_card = np.random.randint(0,7)
                        for card in player_hand:
                            temp_list1.append(card[0])
                        for card in npc_hand:
                            temp_list2.append(card[0])
                        if npc_hand[random_card][0] in temp_list1 and chance in temp_list2:
                            npc_card_pick = npc_hand[random_card][0]
                            count = 11
                        else:
                            npc_card_pick = npc_hand[random_card][0]
                            count += 1
                elif chance > 20:
                    random_card = np.random.randint(0,7)
                    npc_card_pick = npc_hand[random_card][0]
            # Checks to see if the player has the card.
            for number, suite in player_hand:
                if npc_card_pick == number:
                    pick_result = f"{player_name}: Yes, here you go. Do you have a..."
                    pick = True
                    break
                else:
                    pick_result = f"{player_name}: No, go fish!"
                    pick = False
            if pick == False:
                npc_hand += [deck[i]]
            # Remove every instance of the card the NPC has picked from the player's hand.
            filtered_hand = list(filter(lambda card: card[0] != npc_card_pick, player_hand))
            player_hand = filtered_hand
            # Format the list into a single string
            def format(player_hand):
                result = ''
                count = -1
                len_of_hand_minus_one = len(player_hand) - 2
                for item in player_hand:
                    count += 1
                    result += f"{format_card(item)}, "
                    if count == len_of_hand_minus_one:
                        break
                final_index = count + 1
                result += f"and a {format_card(player_hand[final_index])}. "
                return result
            if gambling_hall_skill[npc] == 1:
                pass
            print(npc_hand)
            # Puts together the end string to be sent to Discord.
            if pick == True: 
                results = (f"**{player_name}'s old hand:**\n{format(old_player_hand)}\n\nAfter a coin was flipped to decide, {npc} will go first.\n{npc}: Do you have any {special_formatting(npc_card_pick)}?\n{pick_result}\n\n**{player_name}'s current hand:**\n{format(player_hand)}")
            elif pick == False:
                results = (f"**{player_name}'s hand:**\n{format(player_hand)}\n\nAfter a coin was flipped to decide, {npc} will go first.\n{npc}: Do you have any {special_formatting(npc_card_pick)}?\n{pick_result}")
            return results

print(go_fish('Dale',0, 'Thor'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    list = message.content.split(
        " "
    )  # Turn string into list of many strings based off the amount of spaces
    if message.content.startswith("$lvlup "):  # $lvlup Thor
        print(localtime_call)
        name = list[1]
        records = [message.author.nick, name]
        print(records)
        growths = get_growths1(name)
        enumerated_growths = []
        for index, key in enumerate(growths.items()):
            enumerated_growths.insert(index, key[1][0])
        lvl = get_lvlup(enumerated_growths)
        if not growths:  # If the player has typed the name wrong
            await message.channel.send(
                "Error: Character not found!\nPlease ensure you have typed the name correctly and"
                " that the first letter is capitalized."
            )
        elif (
            not lvl
        ):  # Checks if the list is empty, designating a Null Level up and rerolling
            count = 0
            while not lvl and count < 6:
                channel = client.get_channel(847979864862883850)
                await channel.send(name + " got a Null Level up!\nRerolling ...\n")
                lvl = get_lvlup(enumerated_growths)
                count += 1
                if count > 5:
                    lvl = ["nothing."]
                    await message.channel.send(
                        "Too many Null levels ups in a row. Wow you're unlucky!"
                    )
        await message.channel.send(
            lvl[1] + "----------------\n" + name + " got " + ", ".join(lvl[0])
        )
    list = message.content.split(" ")
    if message.content.startswith("$uncap "):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
        if authorized:
            name = list[1]
            stat = list[2]
            cap = remove_cap(name, stat)
            if cap:
                await message.channel.send(name + "'s " + stat + " has been uncapped.")
            else:
                await message.channel.send(
                    name + "'s " + stat + " is already uncapped."
                )
        else:
            await message.channel.send("Only Jay may use this feature.")
    if message.content.startswith("$cap "):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
        if authorized:
            name = list[1]
            stat = list[2]
            was_capped = cap_it(name, stat)
            if was_capped:
                await message.channel.send(
                    name + "'s " + stat.upper() + " is now capped."
                )
            else:
                await message.channel.send("This stat is already capped")
        else:
            await message.channel.send("Only Jay may use this feature.")
    if message.content.startswith("$update "):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            for character in message.content:
                symbols = ['!', '@', '#', '%', '^', '&', '*', '(', ')', '-', '=', '_', '+', '`', '~'] 
                if character in symbols:
                    await message.channel.send("Don't use symbols!!")
            authorized = True
            if authorized and character not in symbols:
                name = list[1]
                stat = list[2]
                value = list[3]
                update = update_growth(name, stat, value)
                if update:
                    await message.channel.send(
                        name
                        + "'s "
                        + stat.upper()
                        + " has been updated to "
                        + value
                        + "."
                    )
        else:
            await message.channel.send("Only Jay may use this feature.")
    if message.content.startswith("$stats "):
        print(localtime_call)
        name = list[1]
        growths = get_growths1(name)
        variable = "**" + name + "'s" + " growths" ":" + "**" + "\n"
        stats = [
            "HP",
            "STR",
            "MAG",
            "SKL",
            "SPD",
            "LCK",
            "DEF",
            "RES",
            "CON",
            "CHA",
            "INT",
            "INV",
        ]
        for key in stats:
            line = key.upper() + ":"
            val = growths[key]
            for i in val:
                line = str(line + " " + str(i))
            variable = variable + line + "\n"
        records = [message.author.nick, name]
        print(records)
        print(variable)
        await message.channel.send(variable)
    if message.content.startswith("$inhall "):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
            if authorized:
                filename = gambling_hall_directory
                with open(filename, "wt") as fid:
                    name = list[1]
                    fid.write(name)
                # gambling = in_gambling_hall(name)
                await message.channel.send(name + " is now in the gambling hall.")
        else:
            await message.channel.send("Only Jay may use this feature.")
    if message.content.startswith("$rps "):
        print(localtime_call)
        filename = gambling_hall_directory
        with open(filename, "r+") as fid:
            for line in fid:
                npc = line.split()
            name = npc[0]
        choice = list[1]
        if name == "Nobody" or name == 'nobody':
            await message.channel.send("There's nobody in the gambling hall.")
        elif message.author.id != 796135159971446824:
            records = [message.author.nick]
            print(records)
            kanan_skill = False
            result = RPS_game(name, choice, kanan_skill)
            print(result)
            await message.channel.send(result)
        elif message.author.id == 796135159971446824:
            records = [message.author.nick]
            print(records)
            kanan_skill = True
            result = RPS_game(name, choice, kanan_skill)
            print(result)
            await message.channel.send(result)
    if message.content.startswith("$create "):
        print(localtime_call)
        admin = client.get_user(335453916051275778)
        dev = client.get_user(234087004877357056)
        authorized = False
        if message.author.id in [234087004877357056, 335453916051275778]:
            authorized = True
            if authorized:
                name = str(list[1]).title()
                path = characters_directory
                new_file = os.path.join(path, name + ".txt")
                if os.path.isfile(new_file):
                    await message.channel.send(name + " already exists.")
                else:
                    with open(new_file, "wt") as fid:
                        fid.write("")
                    stats = [
                        "HP",
                        "STR",
                        "MAG",
                        "SKL",
                        "SPD",
                        "LCK",
                        "DEF",
                        "RES",
                        "CON",
                        "CHA",
                        "INT",
                        "INV",
                    ]
                    growths = {}
                    for item in stats:
                        growths[item] = [0]
                    overwrite_char(name, growths)
                    await message.channel.send(name + " has been created.")
    if message.content.startswith("$cards"):
        filename = gambling_hall_directory
        with open(filename, "r+") as fid:
            for line in fid:
                npc = line.split()
            name = npc[0]
        if name == "Nobody" or name == "nobody":
            await message.channel.send("There's nobody in the gambling hall.")
        elif message.author.id != 796135159971446824:
            records = [message.author.nick, name]
            print(records)
            kanan_skill = 0
            result = card_game(name, kanan_skill)
            print(result)
            await message.channel.send(result)
        elif message.author.id == 796135159971446824:
            records = [message.author.nick, name]
            print(records)
            kanan_skill = 1
            result = card_game(name, kanan_skill)
            print(result)
            await message.channel.send(result)
    if message.content.startswith("$tarot"):
        name = str(list[1]).title()
        print(localtime_call)
        print(f'{message.author.nick} pulled a tarot card for {name}.')
        path = characters_directory
        new_file = os.path.join(path, name + ".txt")
        if os.path.isfile(new_file):
            result = pull_tarot_card(name)
            await message.channel.send(result)
        if not os.path.isfile(new_file):
            await message.channel.send("Please specify the character pulling the tarot card.")
    if message.content.startswith("$roll"): 
        print(localtime_call)
        try:
            print(message.author.nick+" rolled dice.")
            dice = re.findall(r'\d+', list[1])
            if 'd' in list[1]:
                try:
                    result = custom_dice_roll(int(dice[0]), int(dice[1]))
                    await message.channel.send(result)
                except IndexError as err:
                    print(err)
                    await message.channel.send("Incorrect usage of command. Example: $roll 1d100")
            else:
                await message.channel.send("Incorrect usage of command. Example: $roll 1d100")
        except TypeError:
            dice = re.findall(r'\d+', list[1])
            if 'd' in list[1]:
                try:
                    result = custom_dice_roll(int(dice[0]), int(dice[1]))
                    await message.channel.send(result)
                except IndexError as err:
                    print(err)
                    await message.channel.send("Incorrect usage of command. Example: $roll 1d100")
            else:
                await message.channel.send("Incorrect usage of command. Example: $roll 1d100")
    if message.content.startswith('$gofish'):
        try:
            player = str(list[1]).title()
            person_playing_go_fish = message.author.nick
            filename = gambling_hall_directory
            with open(filename, "r+") as fid:
                for line in fid:
                    npc = line.split()
                name = npc[0]
            if name == "Nobody" or name == "nobody":
                await message.channel.send("There's nobody in the gambling hall.")
            elif message.author.id != 796135159971446824:
                await message.channel.send(go_fish(name, 0, player))
        except IndexError:
            await message.channel.send("Incorrect usage of command.")
#client.run(os.getenv('token'))