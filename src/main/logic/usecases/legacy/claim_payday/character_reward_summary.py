class CharacterRewardSummary:
    def __init__(self, name, level, money):
        self.name = name
        self.level = level
        self.money = money

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.level == other.level and self.money == other.money
        return False
