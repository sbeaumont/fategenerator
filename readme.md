# Fate Core Generator

This generator is a personal project for me as GM to generate all kinds of things:
characters, rube goldberg machines, zones... to help me with inspiration to create
NPC's and situations on the spot.

The wordlists are all a combination of word lists found on the internet
, personal additions and reclassifications in new word lists. They can definitely use some improvement, but...
already work pretty well for me as is.

Overall working:
- word lists are loaded from the "wordlists" directory with a .txt extension
- each word list is registered under the name of the file without extenstion. Use a singular noun,
  this works better in template strings.
- the expansion code is smart enough that if multiple occurrences of something are in one string it ensures uniqueness.
  (this is done with random.sample)
- expansions can be nested, so a wordlist can have the $[xxx] notation. There is no circular ref protection (yet).
- The $[xx] notation is what gets expanded. Note: the notation ensures that it's easy to paste words together
  without relying on whitespace. $[gadget]$[gadget] is a LOT easier to parse than $[gadget]$[gadget]

- The archetypes are character templates to ensure that NPC's aren't totally random.
- The "modes" idea is  taken from the Atomic Robo RPG. A mode is a list of skills, and a character is a set of modes.
  A skill gets a +1 for each occurrence in a mode. You can construct characters from a set of modes.
- A finer grained way is the "pyramid" method. This gives more fine grained control since the skill level is chosen,
  and then the skill is either a fixes skill or a mode name, from which a random skill will be chosen. The generator
  will ensure that duplicate skills will not happen during generation.
- Note that this generator depends on all Skill and mode names being unique.

- The generator currently has some not yet fully fleshed out ideas for generators. There's a Rube Goldberg machine
  generator, zones generator, simple NPC generator... all that remains to improve, but already works as generator
  of inspiring ideas for me.
