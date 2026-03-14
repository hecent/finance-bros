class Player:
    def __init__(self,money,happiness,grades):
        self.money = money
        self.happiness = happiness
        self.grades = grades

    def apply_effect(self, effect):
        self.money += effect.money
        self.happiness += effect.happiness
        self.grades += effect.grades