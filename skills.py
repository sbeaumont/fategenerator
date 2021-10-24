import json
from collections import defaultdict, Counter, UserDict
from random import sample, choice


SKILL_REPO_FILE = 'skills_modes.json'


class Skillset(UserDict):
    """Smart dictionary of skills that understands the pyramid and mode methods of generation."""
    @classmethod
    def single_list(cls, peak_level: int, from_list="core"):
        """Return a list of skills chosen from source list from 1 to peak level."""
        with open(SKILL_REPO_FILE) as f:
            skills = json.load(f)
            source_list = skills[from_list]
        return cls(dict(zip(sample(source_list, k=peak_level), range(1, peak_level + 1))))

    @classmethod
    def from_pyramid(cls, pyramid_in):
        """Parse a pyramid skill template into an actual set of skills. Also ensures all skills are unique."""
        def remove_skill(skill_repo, skill_name):
            for mode in skill_repo:
                skill_repo[mode] = [sk for sk in skill_repo[mode] if sk != skill_name]

        with open(SKILL_REPO_FILE) as f:
            skills_source = json.load(f)
        skills_out = dict()
        # First pass to determine skills that are already defined
        for level, names in pyramid_in.items():
            for name in names:
                if name not in skills_source.keys():
                    skills_out[name] = level
                    remove_skill(skills_source, name)
        # Second pass to replace mode names with skills
        for level, names in pyramid_in.items():
            for name in names:
                if name in skills_source.keys():
                    chosen_skill = choice(skills_source[name])
                    skills_out[chosen_skill] = level
                    remove_skill(skills_source, chosen_skill)
        return cls(skills_out)

    @classmethod
    def default_pyramid(cls, level=4):
        return cls.from_pyramid({i: ['core'] * (level - i + 1) for i in range(level, 0, -1)})

    @classmethod
    def from_modes(cls, mode_names: list):
        """Parse a set of modes into a set of concrete skills."""
        with open(SKILL_REPO_FILE) as f:
            modes = json.load(f)
            cntr = Counter()
            for mode_name in mode_names:
                cntr.update(modes[mode_name])
        return cls(dict(cntr))

    @property
    def pyramid(self):
        """Return a dictionary of 'level: [skill, skill, ..]' items which is the natural Fate representation."""
        result = defaultdict(list)
        for skill, level in self.items():
            result[level].append(skill)
        return dict(result)


if __name__ == '__main__':
    print(Skillset.single_list(3).pyramid)
    print(Skillset.single_list(2, "combat").pyramid)
    print(Skillset.single_list(1).pyramid)

    ss = Skillset.from_modes(["Action", "Automata", "Beast", "Hunter"])
    print(f"Skillset: {ss}")
    print(f"Skillset pyramid: {ss.pyramid}")

    pyramid_in = {3: ['combat', 'physical'], 2: ['Athletics', 'core'], 1: ['mental', 'Rapport', 'Fight', 'Drive']}
    ss2 = Skillset.from_pyramid(pyramid_in)
    print(f"Skillset {ss2.pyramid} from pyramid {pyramid_in}")

    assert {'Rapport', 'Fight', 'Drive'}.issubset(ss2.pyramid[1])
    with open(SKILL_REPO_FILE) as f:
        skills_repo = json.load(f)
    l1_diff = set(ss2.pyramid[1]).difference(['Rapport', 'Fight', 'Drive'])
    assert len(l1_diff) == 1
    assert set(l1_diff).issubset(skills_repo['mental'])
