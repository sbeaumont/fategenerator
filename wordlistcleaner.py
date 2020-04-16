"""
Parse files with "first name first name last name" records into first name and last name files.
Just a helper to deal with name lists found on the internet.
"""

import os

INPUT_DIR = 'wordlists_new'
MALE_FILE_IN = os.path.join(INPUT_DIR, 'steampunk_names.txt')
FEMALE_FILE_IN = os.path.join(INPUT_DIR, 'steampunk_names_female.txt')
OUTPUT_DIR = 'wordlists'
MALE_FIRST_NAME_OUT = os.path.join(OUTPUT_DIR, 'first_name_male.txt')
FEMALE_FIRST_NAME_OUT = os.path.join(OUTPUT_DIR, 'first_name_female.txt')
LAST_NAME_OUT = os.path.join(OUTPUT_DIR, 'last_name.txt')

with open(MALE_FILE_IN) as f:
    male_names_in = [name.strip() for name in f.readlines()]

with open(FEMALE_FILE_IN) as f:
    female_names_in = [name.strip() for name in f.readlines()]

if os.path.exists(MALE_FIRST_NAME_OUT):
    with open(MALE_FIRST_NAME_OUT, 'r') as f:
        male_first_names = set([name.strip() for name in f.readlines()])
else:
    male_first_names = set()

if os.path.exists(FEMALE_FIRST_NAME_OUT):
    with open(FEMALE_FIRST_NAME_OUT, 'r') as f:
        female_first_names = set([name.strip() for name in f.readlines()])
else:
    female_first_names = set()

if os.path.exists(LAST_NAME_OUT):
    with open(LAST_NAME_OUT, 'r') as f:
        last_names = set([name.strip() for name in f.readlines()])
else:
    last_names = set()

for name in male_names_in:
    fn1, fn2, ln = name.split()
    male_first_names.add(fn1)
    male_first_names.add(fn2)
    last_names.add(ln)

for name in female_names_in:
    fn1, fn2, ln = name.split()
    female_first_names.add(fn1)
    female_first_names.add(fn2)
    last_names.add(ln)

with open(MALE_FIRST_NAME_OUT, 'w') as f:
    f.writelines('\n'.join(sorted(list(male_first_names))))

with open(FEMALE_FIRST_NAME_OUT, 'w') as f:
    f.writelines('\n'.join(sorted(list(female_first_names))))

with open(LAST_NAME_OUT, 'w') as f:
    f.writelines('\n'.join(sorted(list(last_names))))


