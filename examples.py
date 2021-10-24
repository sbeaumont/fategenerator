"""
Examples of generators you can make with the tools.

The expansion strings use a $[name_of_word_list] to randomly choose items from the word lists.
This works recursively. If you have a word list with $[xxx] syntax in it, that will get expanded as well,
so you can build more complex structures. You can use a | (the "or" sign) to have one expansion choose
from multiple lists, so $[aaa|bbb] will give you one item from list aaa or list bbb.

Adding a new list is really easy. All lists in the wordlists directory automatically get
picked up. Just add a mynewlist.txt into the wordlists directory and refer to
it in your expansion strings as $[mynewlist].

Wrap an expansion string in the lists.expand() (shorthand e()) function to let the generator do its magic.
From that point you can get as creative as you want. This file shows some example uses.

The Skillset and Character classes offer some intelligence in dealing with Fate characters and skill sets.

The skills_modes.json and character_template.json files can be expanded with your own lists and templates.
"""


from random import choice, randint
from wordlists import lists
from skills import Skillset
import string
from character import character_templates, Character

e = lists.expand


# Create some zones, like a quick combat
def zone():
    return {
        'name': lists.choice('zone'),
        'aspects': [e(f"$[color] $[quality] $[material] {obj}") for obj in lists.sample('object_outside', 3)]
    }


print("\nZones\n")
for i in range(4):
    print(zone())

# Rube Goldberg machine generator

print(e(f"\nRube Goldberg machine: The $[gadget]$[gadget]-{choice(string.ascii_uppercase)}{randint(1000, 9999)}\n"))
for i in range(randint(5, 10)):
    print(e("$[color] $[material] $[object_outside|object_small] $[movement] $[direction]"))

# A simple random town street generator: this one prints 5 to 10 stores.

print("\nA Street\n")
for i in range(randint(5, 10)):
    print(e("$[store]"))

# NPC Maker

print("\nSimple NPC")
print(e("\n$[first_name_male|first_name_female] $[last_name]"))
print(e("$[motivation] $[motivation] $[motivation]"))
print(lists.sample('job'), Skillset.single_list(3))

print("\nAnother simple NPC, but with the more advanced +/- motivation generator")
print(e("\n$[first_name_male|first_name_female] $[last_name]"))
print(Character.motivations(3))
print(lists.sample('job'), Skillset.single_list(3))

# Generate one character for each archetype

print("\nAn instance of each character template")
for ct in character_templates:
    print(f"\n== {ct['name']} ==")
    print(Character.from_archetype(ct['name']))

# Convenient ways to create skill lists.
# The "pyramid" creates a dictionary that collects all equal level skills together, indexed by skill level

print("\nSingle skill list NPCs\n")
print(lists.sample('job'), Skillset.single_list(3))
print(lists.sample('job'), Skillset.single_list(2))
print(lists.sample('job'), Skillset.single_list(1))

print("\nEasy ways to create skill pyramids\n")
def_pyrmd = Skillset.default_pyramid()
# Showing difference between flat list and pyramid version
print(def_pyrmd.pyramid)
print("(Flat list format)", def_pyrmd)
print()
print(Skillset.default_pyramid(3).pyramid)
print(Skillset.default_pyramid(2).pyramid)
print(Skillset.default_pyramid(1).pyramid)
print(Skillset.single_list(2, "combat").pyramid)

print("\nGenerate skill lists from Atomic Robo style modes\n")
ss = Skillset.from_modes(["Action", "Automata", "Beast", "Hunter"])
print(f"Skillset: {ss}")
print(f"Skillset pyramid: {ss.pyramid}")

print("\nGenerate skill set from a combination of fixed skills and skill lists\n")
pyramid_in = {3: ['combat', 'physical'], 2: ['Athletics', 'core'], 1: ['mental', 'Rapport', 'Fight', 'Drive']}
ss2 = Skillset.from_pyramid(pyramid_in)
print(f"Skillset {ss2.pyramid} from pyramid {pyramid_in}")