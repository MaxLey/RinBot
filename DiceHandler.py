import random
import re
from collections import defaultdict


def parse_dice_string(instring):
    terms = instring.replace(" ", "").replace("-", "+-").split('+')
    dice = defaultdict(int)
    if not terms:
        return {}
    for term in terms:
        term_split = re.split('[dD]', term)
        if len(term_split) is 0 or len(term_split) > 2:
            return {}
        if term_split[0] is "":
            continue
        if len(term_split) is 1:
            term_split.append('1')
        if term_split[0].startswith('-'):
            term_split[1] = '-' + term_split[1]
            term_split[0] = term_split[0][1:]
        try:
            term_split[0] = int(term_split[0])
            term_split[1] = int(term_split[1])
        except ValueError:
            return {}
        dice[term_split[1]] += term_split[0]
    return dice

def roll_dice_dict(dicedict):
    total = []
    for (die, number) in dicedict.items():
        if die < 0:
            multiplier = -1
        else:
            multiplier = 1
        for i in range(0, number):
            newval = random.randint(1, abs(die)) * multiplier
            total.append(newval)
    return total
