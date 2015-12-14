__author__ = 'anthony'

#TODO: Make ROLL a class, it looks shoddy and amateur as it is
#TODO: In parse string, convert all values enclosed in square brackets to their numerical values
#Note: It's perhaps best to link this up to a DB first /before/ getting all the syntax set exactly
#TODO: Implement EXECUTE in parse_input

from flask import session

import random

ROLL_KEYWORD = "ROLL"
EFFECT_KEYWORD = "EFFECT"
OUTPUT_KEYWORD = "OUTPUT"
EXECUTE_KEYWORD = "EXECUTE"
ADVANTAGE_CODE = "ADV"
DISADVANTAGE_CODE = "DIS"
LUCKY_CODE = "LUCKY"
GREAT_WEAPON_CODE = "GREAT"
BRUTAL_CODE = "B"
MINIMUM_10_CODE = "M10"
CRITICAL_CODE = "CRIT"

def parse_input(player_string):
    """Takes any text a player inputs, and formats the output if they include the keywords ROLL or EFFECT"""
    caps_player_string = player_string.upper()
    roll_position = caps_player_string.find(ROLL_KEYWORD)
    effect_position = caps_player_string.find(EFFECT_KEYWORD)
    action_name = ""
    if roll_position == -1 and effect_position == -1:
        return player_string
    elif roll_position == -1 and effect_position > -1:
        action_name = player_string[:effect_position]
        effect_text = player_string[effect_position+len(EFFECT_KEYWORD):]
        if action_name != "":
            return action_name + ": " + effect_text
        else:
            return effect_text
    elif roll_position > -1 and effect_position == -1:
        action_name = player_string[:roll_position]
        roll_text = caps_player_string[roll_position+len(ROLL_KEYWORD):]
        roll_output = parse_roll(roll_text)
        if action_name != "":
            return action_name + " and rolls " + roll_output
        else:
            return "Rolls " + roll_output
    elif roll_position != -1 and effect_position != -1:
        if roll_position < effect_position:
            action_name = player_string[:roll_position]
            roll_text = caps_player_string[roll_position+len(ROLL_KEYWORD):effect_position]
            roll_output = parse_roll(roll_text)
            effect_text = player_string[effect_position+len(EFFECT_KEYWORD):]
        else:
            action_name = player_string[:effect_position]
            effect_text = player_string[effect_position+len(EFFECT_KEYWORD):roll_position]
            roll_text = caps_player_string[roll_position+len(ROLL_KEYWORD):]
            roll_output = parse_roll(roll_text)
        if action_name != "":
            return action_name + ", rolls " + roll_output + " and " + effect_text
        else:
            return "Rolls " + roll_output + " and " + effect_text
    else:
        return "This wasn't supposed to happen"

def nice_parse_input(player_string):
    """Takes any text a player inputs, and formats the output if they include the keywords ROLL or EFFECT"""
    player_string = replace_keywords(player_string)
    caps_player_string = player_string.upper()
    roll_position = player_string.find(ROLL_KEYWORD)
    effect_position = player_string.find(EFFECT_KEYWORD)
    if roll_position == -1 and effect_position == -1:
        return player_string
    elif roll_position == -1 and effect_position > -1:
        effect_text = player_string[effect_position+len(EFFECT_KEYWORD):]
        return effect_text
    elif roll_position > -1 and effect_position == -1:
        roll_text = caps_player_string[roll_position+len(ROLL_KEYWORD):]
        roll_output = parse_roll(roll_text)
        if roll_output != "Error":
            return "Rolls " + roll_output
        else:
            return "The syntax for your roll (" + roll_text + ") is off. Check the example rolls for guidelines on making your own rolls"
    elif roll_position > -1 and effect_position > -1:
        if roll_position < effect_position:
            roll_text = caps_player_string[roll_position+len(ROLL_KEYWORD):effect_position]
            effect_text = player_string[effect_position+len(EFFECT_KEYWORD):]
        else:
            roll_text = caps_player_string[roll_position+len(ROLL_KEYWORD):]
            effect_text = player_string[effect_position+len(EFFECT_KEYWORD):roll_position]
        roll_output = parse_roll(roll_text)
        if roll_output != "Error":
            effect_text = (effect_text.replace(OUTPUT_KEYWORD,roll_output)).lstrip(" ")
        else:
            return "The syntax for your roll (" + roll_text + ") is off. Check the example rolls for guidelines on making your own rolls"
        return effect_text
    else:
        return "This wasn't supposed to happen"

def replace_keywords(player_string):
    replaced = False
    while not replaced:
        keyword_start = player_string.find("[") + 1
        if keyword_start == 0:
            replaced = True
        else:
            keyword_end = player_string.find("]")
            if keyword_end < keyword_start:
                return "The syntax for your keywords is off. Check the example rolls for guidelines on making your own rolls"
            keyword = player_string[keyword_start:keyword_end]
            keyword_value = session.get(keyword)
            if keyword_value == None:
                return "Keyword '" + keyword + "' not found. Check your spelling and try again"
            player_string = player_string.replace("[" + keyword + "]",keyword_value)
    return player_string

def parse_roll(roll_text):
    """Takes an uppercase string, rolls the appropiate dice and adds all modifiers, and returns the sum of the roll"""
    roll_text = roll_text.replace(" ","")
    rolls_total = 0
    critical_hit = False
    if CRITICAL_CODE in roll_text:
        critical_hit = True
        roll_text = roll_text.replace(CRITICAL_CODE,"")
    rolls = roll_text.split("+")
    for roll in rolls:
        modifiers = get_modifiers(roll,critical_hit)
        roll = resolve_modifiers(roll)
        roll = resolve_naked_numbers(roll)
        d_position = roll.find("D")
        if d_position == -1:
            rolls_total += int(roll)
            continue
        try:
            rolls_total += roll_dice(roll, modifiers)
        except TypeError:
            return "Error"

    return str(rolls_total)

def resolve_naked_numbers(roll):
    """Resolves multiplication between and integer and <= 1 die, resolves division between two numbers"""
    if "*" in roll:
        first_factor = roll.split("*")[0]
        second_factor = roll.split("*")[1]
        if "D" in first_factor:
            roll = str(int(int(first_factor.split("D")[0]) * float(second_factor))) + first_factor.split("D")[1]
        elif "D" in second_factor:
            roll = str(int(int(second_factor.split("D")[0]) * float(first_factor))) + second_factor.split("D")[1]
        else:
            roll = str(int(float(first_factor)) * int(float(second_factor)))
    if "/" in roll:
        dividend = roll.split("/")[0]
        divisor = roll.split("/")[1]
        roll = str(int(float(dividend)/float(divisor)))
    return roll

def get_modifiers(roll, critical_hit):
    """Reads a dice roll's string for modifiers, and returns a dictionary with those modifiers"""
    modifiers  = {"Advantage": False, "Disadvantage": False, "Lucky": False, "Great Weapon": False, "Brutal": 0,
                  "Critical": critical_hit, "Minimum Roll": 1}
    if ADVANTAGE_CODE in roll:
        modifiers["Advantage"] = True
    if DISADVANTAGE_CODE in roll:
        modifiers["Disadvantage"] = True
    if LUCKY_CODE in roll:
        modifiers["Lucky"] = True
    if GREAT_WEAPON_CODE in roll:
        modifiers["Great Weapon"] = True
    modifiers["Brutal"] += roll.count("B")
    if MINIMUM_10_CODE in roll:
        modifiers["Minimum Roll"] = 10
    return modifiers

def resolve_modifiers(roll):
    """Removes all modifiers from a roll. Should be called after get_modifiers"""
    roll.replace(ADVANTAGE_CODE,"")
    roll.replace(DISADVANTAGE_CODE,"")
    roll.replace(LUCKY_CODE,"")
    roll.replace(GREAT_WEAPON_CODE,"")
    roll.replace(BRUTAL_CODE,"")
    roll.replace(MINIMUM_10_CODE,"")
    return roll

def roll_dice(roll, modifiers):
    """Rolls X number of Y kind of dice with modifiers Z, given a string of the form 'XDYZ'
    Modifier effects:
    Advantage: Makes the roll twice, and takes the higher of the two. Cancels out disadvantage
    Disadvantage: Makes the roll twice, and takes the lower of the two. Cancels out advantage
    Critical: Doubles the number of all the dice in the roll
    Brutal: Increases the number of dice in the roll by the brutal rating
    Lucky: Re-roll once dice that land on 1
    Great Weapon: Re-roll once dice that land on 1 or 2
    Minimum Roll: If the dice goes below this value, treat it as this value"""
    try:
        if modifiers["Advantage"] and not modifiers["Disadvantage"]:
            modifiers["Advantage"] = False
            return max(roll_dice(roll, modifiers), roll_dice(roll,modifiers))
        if modifiers["Disadvantage"] and not modifiers["Advantage"]:
            modifiers["Disadvantage"] = False
            return min(roll_dice(roll, modifiers), roll_dice(roll, modifiers))
        num_dice = int(roll.split("D")[0])
        if modifiers["Critical"]:
            num_dice*=2
            num_dice+=modifiers["Brutal"]
        die_type = roll.split("D")[1]
        if die_type[0] == "4" or die_type[0] == "6" or die_type[0] == "8":
            die_type = int(die_type[0])
        elif die_type[:3] == "100" or die_type[0] == "%":
            die_type = 100
        elif die_type[:2] == "10" or die_type[:2] == "12" or die_type[:2] == "20":
            die_type = int(die_type[:2])
        else:
            die_type = 6
        roll_total = 0
        critical_success = False
        critical_failure = False
        for die in range(num_dice):
            die_result = random.randint(1,die_type)
            if die_result == 1 and modifiers["Lucky"] or die_result <= 2 and modifiers["Great Weapon"]:
                die_result = random.randint(1,die_type)
            if die_result < modifiers["Minimum Roll"]:
                die_result = modifiers["Minimum Roll"]
            if die_result == 20 and die_type == 20:
                critical_success = True
            if die_result == 1 and die_type == 20:
                critical_failure = True
            roll_total += die_result
        return roll_total
    except ValueError:
        return "Error"
