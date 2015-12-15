Virtual-PNP
===================

A chatroom website with D&D style dice-rolling features added in. Adding ability to save characters soon™.

Basic syntax is as follows:

ROLL <Dice Roll> EFFECT <Effect Text> OUTPUT <More Effect Text>

Where Effect Text can be whatever you wish (although using one of the three keywords is probably a recipe for trouble)

Dice rolls can be as simple as 1d20, 2D6, etc., and each set of dice is connected with a "+", e.g., 2d6 + 1d20. Naked numbers can also be added in this fashion: 2d8 + 4

Additionally, extra modifiers can be added by appending extra characters at the end of each set:

ADV (Advantage) - Roll the set twice and take the higher of the two tries\n
DIS (Disadvantage) - Roll the set twice and take the lower of the two tries\n
LUCKY (Lucky) - Re-roll each die in the set if that die initially rolls a 1\n
GREAT (Great Weapon) - As LUCKY, but re-rolling 1s and 2s\n
M10 (Minimum 10) - If, after re-rolls, a die gets rolls less than 10, the result is set to 10\n
B (Brutal) - Each B following a set of dice increases the number of dice rolled by 1 if the roll was a critical

As a special rule, if CRIT is anywhere in the dice roll, all the dice, aside from Brutal dice, are doubled

Example input strings and their output

"Hey people, what's up?" --> "Hey people, what's up?"\n
ROLL 1d10 --> Rolls 6\n
ROLL 1d20 ADV EFFECT I attack him from a height and roll OUTPUT! --> EFFECT I attack him from a height and roll 15
