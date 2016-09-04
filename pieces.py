# This file contains the general unit class.

class Unit(object):
    def __init__(self, strength, hp, xp_drop, xp_threshold, moves, value, name):
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
        self.cooldown = [0, 0]
        self.value = value
        self.name = name

    def get_xp_drop(self):
        return self.xp_drop

    def set_board(self, board):
        self.board = board

    def get_name(self):
        return self.side.get_name() + " " + self.name + " [" + str(self.level) + "]"

    def get_side(self):
        return self.side

    def get_cd_1(self):
        return self.cooldown[0]

    def get_cd_2(self):
        return self.cooldown[1]

    def get_cur_xp(self):
        return self.xp

    def get_max_xp(self):
        return self.xp_threshold

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
        buff = 1
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
        while self.xp >= self.xp_threshold and self.level <= 3:
            self.xp -= self.xp_threshold
            self.level_up()

    def check_move(self, x, y):
        if (x, y) in self.moves:
            return True
        return False

    def check_attack(self, x, y):
        return self.check_move(x, y)

    def tick(self):
        buffs = []
        for buff in self.buffs[0]:
            if buff[1] > 1:
                buffs.append((buff[0], buff[1] - 1))
                self.buffs[0] = buffs
                if self.cooldown[0] > 0:
                    self.cooldown -= 1
                if self.cooldown[1] > 0:
                    self.cooldown -= 1

    def get_hp(self):
        return self.hp

    def get_perhp(self):
        return self.hp / float(self.base_hp)

    def isDead(self):
        return self.hp <= 0

    def get_level(self):
        return self.level

