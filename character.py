from wordlists import lists
from random import choice
from skills import Skillset
import json

e = lists.expand

# The list of all archetypes
with open('archetypes.json') as f:
    archetypes = json.load(f)


class Character(object):
    """Character generator based on a given archetype."""
    Good = 3
    Fair = 2
    Average = 1

    def __init__(self, skills, archetype=None):
        self.archetype = archetype
        self.name = Character.name()
        self.high_concept = Character.high_concept()
        # The term archetype is overloaded now. I use it to mean character template, but the
        # "archetype" word list refers to literary archetypes, which is to determine
        # a tone of voice for this NPC.
        self.voice = lists.choice('archetype')
        self.trouble = Character.trouble()
        self.motivations = Character.motivations()
        self.skills = skills

    def __str__(self):
        return f"Name: {self.name}\n" \
            f"HC: {self.high_concept} ({self.archetype})\n" \
            f" V: {self.voice}\n" \
            f" T: {self.trouble}\n" \
            f" M: {' '.join(self.motivations)}\n" \
            f"Sk: {self.skills.pyramid}"

    @staticmethod
    def name():
        return e("$[first_name_male|first_name_female] $[last_name]")

    @staticmethod
    def motivations(amount=3):
        """A set of three 'for or against' motivations"""
        return [f"{choice(('+', '-'))}{m}" for m in lists.sample('motivation', amount)]

    @staticmethod
    def high_concept():
        return e("$[virtue] $[trait] $[job]")

    @staticmethod
    def trouble():
        return e("$[flaw], $[flaw], $[trouble]")

    @classmethod
    def from_archetype(cls, name):
        """Generate character from named archetype"""
        archetype = [a for a in archetypes if a['name'] == name][0]

        # Don't use both the modes and pyramid methods in one archetype. Currently the code
        # will just override the mode result with the pyramid result.
        skills = Skillset()
        if 'modes' in archetype:
            skills = Skillset.from_modes(archetype['modes'])
        if 'pyramid' in archetype:
            skills = Skillset.from_pyramid(archetype['pyramid'])
        return cls(skills, name)


if __name__ == '__main__':
    # Generate one character for each archetype
    for arc in archetypes:
        print(f"== {arc['name']} ==")
        print(Character.from_archetype(arc['name']))
        print()
