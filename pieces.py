# This file contains all of the piece classes.

import math


class Unit(object):
    def __init__(self, strength, hp, xp_drop, xp_threshold, moves, value):
        self.base_str = strength
        self.base_hp = hp
        self.buffs = [[],[]]
        self.hp = hp
        self.xp = 0
        self.xp_drop = xp_drop
        self.xp_threshold = xp_threshold
        self.level_multiplier = 1.1
        self.level = 1
        self.moves = moves
        self.board = None
        self.side = None
        self.cooldowns = [0, 0]
        self.value = value

    def set_board(self, board):
        self.board = board

    def get_side(self):
        return self.side

    def get_value(self):
        return self.value

    def set_side(self, side):
        self.side = side

    def level_up(self):
        if self.level < 3:
            self.base_str *= self.level_multiplier
            self.hp *= self.level_multiplier
            self.base_hp *= self.level_multiplier
            self.level += 1
            self.level_multiplier = 1.25 / 1.1

    def effective_strength(self):
        buff = 0
        for x in self.buffs[0]:
            buff *= x[0]
        return self.base_str * buff

    def deal_damage(self, damage):
        buff = 1
        for x in self.buffs[1]:
            buff *= x[0]
            self.hp -= (damage / buff)
        if self.hp < 0:
            self.hp = 0

    def heal_damage(self, health):
        self.hp += health
        if self.hp > self.base_hp:
            self.hp = self.base_hp

    def buff_attack(self, buff, duration):
        self.buffs[0].append((buff, duration))

    def buff_health(self, buff, duration):
        self.buffs[1].append((buff, duration))

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= self.xp_threshold:
            self.xp -= self.xp_threshold
            self.levelup()

    def check_move(self, x, y):
        if (self.side == white and (x, y) in self.moves) or (self.side == black and (x, -y) in self.moves):
            return True
        return False

    def tick(self):
        buffs = []
        for buff in self.buffs[0]:
            if buff[1] > 1:
                buffs.append((buff[0], buff[1] - 1))
                self.buffs[0] = buffs
                if self.cooldowns[0] > 0:
                    self.cooldowns -= 1
                if self.cooldowns[1] > 0:
                    self.cooldowns -= 1

    def isDead(self):
        return (self.hp <= 0)


class Pawn(Unit):
    def __init__(self):
        moves = [(0, 1)]
        Unit.__init__(self, 3, 10, 1, 2, moves, 3)

    def arrowstorm(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 2 or yDifference <= 2:
                target.deal_damage(math.ceil(.75 * self.effective_str()))
                self.cooldown[0] = 4

    def deal_damage(self, damage):
        local_unit_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc(self)[1] + j)
                if checked_unit == None or checked_unit.side == self.side:
                    local_unit_list.append(checked_unit)
        buff = len(local_unit_list) * 0.3 + 1
        Unit.deal_damage(self, damage / buff)

    def effective_strength(self):
        local_unit_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc[1] + j)
                if checked_unit.side == self.side:
                    local_unit_list.append(checked_unit)
        buff = len(local_unit_list) * 0.3 + 1
        return (buff * self.base_str)

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
        Unit.__init__(self, 7, 75, 3, 3, moves, 10)

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
        Unit.__init__(self, 10, 50, 5, 4, moves, 10)
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
        Unit.__init__(self, 5, 20, 4, 3, moves, 15)

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
        Unit.__init__(self, 7, 40, 0, 3, moves, 100)

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
        Unit.__init__(self, 7, 35, 0, 3, moves, 25)

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

