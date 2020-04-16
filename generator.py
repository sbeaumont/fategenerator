from random import choice, randint
from wordlists import lists
from skills import Skillset
import string

e = lists.expand


def zone():
    return {
        'name': lists.choice('zone'),
        'aspects': [e(f"$[color] $[quality] $[material] {obj}") for obj in lists.sample('object_outside', 3)]
    }


if __name__ == '__main__':
    print("Single skill list NPCs")
    print(lists.sample('job'), Skillset.single_list(3))
    print(lists.sample('job'), Skillset.single_list(2))
    print(lists.sample('job'), Skillset.single_list(1))

    # Inspiration for Zones, like a quick combat
    print("\nZones")
    for i in range(4):
        print(zone())

    # Rube Goldberg machine generator
    print(e(f"\nThe $[gadget]$[gadget]-{choice(string.ascii_uppercase)}{randint(1000, 9999)}\n"))
    for i in range(randint(5, 10)):
        print(e("$[color] $[material] $[object_outside|object_small] $[movement] $[direction]"))

    # Initial version of a random town street generator
    print("\nA Street\n")
    for i in range(randint(5, 10)):
        print(e("$[store]"))
