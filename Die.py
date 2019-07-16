from random import randint


class Die():
    def __init__(self, sides):
        self.sides = sides

    def roll_die(self, sides):
        self.sides = randint(1, sides)
        return self.sides


if __name__ == '__main__':
    sides = 20
    die = Die(sides)
    for i in range(1, 11):
        print(die.roll_die(sides))
