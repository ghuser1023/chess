# Contains the specific piece classes.

from pieces import *
import math


class Pawn(Unit):
    def __init__(self):
        moves = [(0, 1)]
        Unit.__init__(self, 3, 10, 1, 2, moves, 3, "Pawn")

    def arrowstorm(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 2 or yDifference <= 2:
                target.deal_damage(math.ceil(.75 * self.effective_str()))
                self.cooldown[0] = 4

    def deal_damage(self, damage):
        local_unit_list = []
        for i in range(self.board.get_loc(self)[0] - 1, self.board.get_loc(self)[0] + 2):
            for j in range(self.board.get_loc(self)[1] - 1, self.board.get_loc(self)[1] + 2):
                if i >= 0 and i < 8 and j >= 0 and j < 8:
                    checked_unit = self.board.get_unit(i, j)
                    if checked_unit is None or checked_unit.side == self.side:
                        local_unit_list.append(checked_unit)
        buff = len(local_unit_list) * 0.3 + 1
        Unit.deal_damage(self, damage / buff)

    def effective_strength(self):
        num_local = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc(self)[1] + j)
                if checked_unit is not None and checked_unit.side == self.side:
                    num_local += 1
        buff = num_local * 0.3 + 1
        return buff * self.base_str

    def abilities(self):
        return ["arrowstorm"]

    def __str__(self):
        return 'p' + str(self.level)


class Fort(Unit):
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            moves.append((0, i))
            moves.append((i, 0))
        Unit.__init__(self, 7, 75, 3, 3, moves, 10, "Fort")

    def aerial_defense(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 2 or yDifference <= 2:
                target.deal_damage(math.ceil(.75 * self.effective_str()))
                self.cooldown[0] = 4

    def abilities(self):
        return ["aerial_defense"]

    def __str__(self):
        return 'r' + str(self.level)


class Knight(Unit):
    def __init__(self):
        moves = [(-1, -2), (-1, 2), (-2, -1), (-2, 1), (1, -2), (1, 2), (2, -1), (2, 1)]
        Unit.__init__(self, 10, 50, 5, 4, moves, 10, "Knight")
        self.chivalrous = (False, 0)

    def charge(self, moveLoc):
        if self.cooldown[0] == 0:
            self.buff_attack(1.25, 1)
            self.board.move_unit(moveLoc[0], moveLoc[1])
            self.cooldown[0] = 10

    def chivalry(self):
        if self.cooldown[1] == 0:
            self.buff_health(1.2, 2)
            self.chivalrous = (True, 2)
            self.cooldown[1] = 10

    def abilities(self):
        return ["charge", "chivalry"]

    def __str__(self):
        return 'n' + str(self.level)


class Bishop(Unit):
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            moves.append((i, i))
            moves.append((-i, i))
        Unit.__init__(self, 5, 20, 4, 3, moves, 15, "Bishop")

    def regeneration(self, target):
        if self.cooldown[0] == 0:
            target.heal_damage(1000)
            self.cooldown[0] = 16

    def piety(self):
        if self.cooldown[1] == 0:
            local_unit_list = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc[1] + j)
                    if checked_unit.side == self.side:
                        local_unit_list.append(checked_unit)
            for unit in local_unit_list:
                unit.boost_health(1.2, 3)
                unit.boost_attack(1.1, 3)
            self.cooldown[1] = 12

    def abilities(self):
        return ["regeneration", "piety"]

    def __str__(self):
        return 'b' + str(self.level)


class King(Unit):
    def __init__(self):
        self.rally_amt = 30
        moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        Unit.__init__(self, 7, 40, 10, 3, moves, 100, "King")

    def call_to_arms(self, x1, y1, x2, y2):
        if self.cooldown[0] == 0:
            mercenary1 = Pawn()
            mercenary2 = Pawn()
            self.board.add_unit(mercenary1, x1, y1)
            self.board.add_unit(mercenary2, x2, y2)
            self.side.add_unit(mercenary1)
            self.side.add_unit(mercenary2)
            self.cooldown[0] = 20

    def rally(self):
        if self.cooldown[1] == 0:
            self.side.add_morale(self.rally_amt)
            self.rally_amt = (self.rally_amt + 1) // 2
            self.cooldown = 12

    def abilities(self):
        return ["call_to_arms", "rally"]

    def __str__(self):
        return 'k' + str(self.level)


class Queen(Unit):
    def __init__(self):
        self.influence_active = False
        moves = []
        for i in range(-8, 9):
            for j in range(-8, 9):
                moves.append((i, j))
        Unit.__init__(self, 7, 35, 5, 3, moves, 25, "Queen")

    def subterfuge(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 5 or yDifference <= 5:
                target.buff_attack(.75, 3)
                target.deal_damage(math.ceil(.8 * self.effective_strength()))
                self.cooldown[0] = 16

    def influence(self):
        if self.cooldown[1] == 0:
            self.influence_active = True
            self.cooldown[0] = 26

    def abilities(self):
        return ["subterfuge", "influence"]

    def __str__(self):
        return 'q' + str(self.level)

