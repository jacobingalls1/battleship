

class Armor:
    def __init__(self, belt=0, beltMaterial=.5, deck=0, deckMaterial=.1):
        self.belt = belt#inches
        self.beltMaterial = beltMaterial #ton per foot
        self.deck = deck#inches
        self.deckMaterial = deckMaterial  # ton per foot

    def weight(self):
        return self.belt*self.beltMaterial + self.deck*self.deckMaterial