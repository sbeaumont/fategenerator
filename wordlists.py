import re
import os
from os import listdir
from os.path import splitext
from collections import Counter
from random import sample, choice

WORD_LISTS_DIR = 'wordlists'


def load_list(filename):
    """Load a single word list"""
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def load_lists(dir_name):
    """Load all word lists with .txt extension from given directory"""
    result = dict()
    for file in listdir(dir_name):
        name, ext = splitext(file)
        if ext == '.txt':
            result[name] = load_list(os.path.join(dir_name, file))
    return result


class WordLists(object):
    """One word list with ways to randomly choose one or more words"""
    def __init__(self, lists_of_words: dict):
        self._lists = lists_of_words

    def sample(self, list_name, amount=1):
        """Return multiple random choices without duplicates"""
        assert amount >= 1, f"amount must be 1 or higher but was {amount}"
        return sample(self._lists[list_name], amount)

    def choice(self, list_name):
        """Return a single random choices"""
        return choice(self._lists[list_name])

    def get(self, list_name):
        return self._lists[list_name]

    def expand(self, s):
        return expand(s, self)


# This is the list of lists!
lists = WordLists(load_lists(WORD_LISTS_DIR))


def expand(s_expand, context: WordLists = lists):
    """For each occurrence of a field get a random value, making sure there are no doubles.
       Also can deal with nested expansions."""
    # Match $[xxx], with name being xxx at slice [2:-1]
    re_fields = re.compile(r'(\$\[[a-zA-Z_|]+\])')
    field_names = [names[2:-1] for names in re_fields.findall(s_expand)]

    values = dict()
    for field_name, cnt in Counter(field_names).items():
        # Determine from which list or lists the sample should be taken
        list_names = field_name.split('|')
        if len(list_names) > 1:
            # Multiple options, choose one of them
            chosen_list = choice(list_names)
        else:
            chosen_list = field_name
        # Take the sample of words from the chosen list
        values[field_name] = context.sample(chosen_list, cnt)

    # From this point the replacement starts
    def get_sample(m):
        return values[m[0][2:-1]].pop()

    expanded = re_fields.sub(get_sample, s_expand)
    # Does the text we just replaced have replacement tags?
    if re_fields.findall(expanded):
        # The expanded text has replacement tags in it, so call expand to replace those. Yay, recursion!
        return expand(expanded, context)
    else:
        return expanded


if __name__ == '__main__':
    test_list = {
        'normal': ['two'],
        'embedded': ['one of $[normal]']
    }
    wl = WordLists(test_list)
    assert wl.expand("$[normal]") == 'two'
    assert wl.expand("$[embedded]") == 'one of two'
    assert wl.expand("$[embedded|normal]") in ('two', 'one of two')
