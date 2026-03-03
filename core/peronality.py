class Personality:
    def __init__(self, traits):
        self.traits = traits

    def adjust_trait(self, trait_name, value):
        if trait_name in self.traits:
            self.traits[trait_name] += value
            self.traits[trait_name] = max(0, min(100, self.traits[trait_name]))