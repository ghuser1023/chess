# This file contains the general unit class.


class Unit(object):
    def __init__(self, strength, hp, xp_drop, xp_threshold, moves, value, name, abils, mabils):
        """
        :param strength: the default attack stat of this unit.
        :param hp: the maximum health value of this unit.
        :param xp_drop: the amount of xp this unit will drop if killed.
        :param xp_threshold: the amount of xp this unit needs to level up.
        :param moves: the moveset of this unit.
        :param value: the "value" of this piece.
        :param name: the type of this piece. IMPORTANT: not to be confused with the return of get_name,
                     which returns a string used by graphics.
        :param abils: the list of abilities this unit has.
        :param mabils: the list of ability methods this unit has.
        """
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
        self.abils = abils
        self.mabils = mabils
        self.protected = [None, 2]

    def get_protected(self):
        """
        :return: whether or not this unit is protected by chivalry.
        """
        return self.protected[0] is not None

    def add_protected(self, unit):
        """
        Causes this unit to become protected by the Knight's chivalrous ability.
        :param unit: the knight in question
        :return: None
        """
        self.protected[0] = unit
        self.protected[1] = 2

    def get_xp_drop(self):
        """
        :return: the xp received by the unit that destroys this unit.
        """
        return self.xp_drop

    def set_board(self, board):
        """
        :param board: the board to assign this unit to.
        :return: None
        """
        self.board = board

    def get_name(self):
        """
        Note: this method is used by graphics as a display on the HUD.
        :return: the name of this unit.
        """
        return self.side.get_name() + " " + self.name + " [" + str(self.level) + "]"

    def get_side(self):
        """
        :return: the side this unit is on.
        """
        return self.side

    def get_cd_1(self):
        """
        :return: the remaining cooldown time of this unit's first ability.
        """
        return self.cooldown[0]

    def get_cd_2(self):
        """
        :return: the remaining cooldown time of this unit's second ability.
        """
        return self.cooldown[1]

    def get_cur_xp(self):
        """
        :return: the current amount of xp this unit has.
        """
        return self.xp

    def get_max_xp(self):
        """
        :return: the amount of xp required for this unit to level up.
        """
        return self.xp_threshold

    def get_value(self):
        """
        Note: this method should NOT be used for determining xp drops. Use get_xp_drop instead.
        :return: the "value" of this piece.
        """
        return self.value

    def set_side(self, side):
        """
        :param side: the side this unit should be assigned to.
        :return: None
        """
        self.side = side

    def level_up(self):
        """
        Levels up the unit; resets the unit's xp counter.
        :return: None
        """
        if self.level < 3:
            self.base_str *= self.level_multiplier
            self.hp *= self.level_multiplier
            self.base_hp *= self.level_multiplier
            self.level += 1
            self.level_multiplier = 1.25 / 1.1

    def str_buff(self):
        """
        :return: the buff given to this unit's strength.
        """
        buff = 1
        for x in self.buffs[0]:
            buff *= x[0]
        return buff

    def def_buff(self):
        """
        :return: the buff given to this unit's defense.
        """
        buff = 1
        for x in self.buffs[1]:
            buff *= x[0]
        return buff

    def effective_strength(self):
        """
        :return: the effective attack strength of this unit.
        """
        return self.base_str * self.str_buff()

    def deal_damage(self, damage):
        """
        :param damage: the damage to be dealt to this unit.
        :return: None
        """
        if self.protected[0] is not None:
            self.protected[0].deal_damage(damage)
        else:
            buff = self.def_buff()
            self.hp -= (damage / buff)
            if self.hp < 0:
                self.hp = 0
                self.board.remove_unit(self)
                self.side.remove_unit(self)

    def heal_damage(self, health):
        """
        :param health: the amount of damage that will be healed from this unit
        :return: None
        """
        self.hp += health
        if self.hp > self.base_hp:
            self.hp = self.base_hp

    def buff_attack(self, buff, duration):
        """
        :param buff: a multiplier that will be applied to the unit's effective strength
        :param duration: how long that buff will last
        :return: None
        """
        self.buffs[0].append((buff, duration))

    def buff_health(self, buff, duration):
        """
        :param buff: a multiplier that will be applied to damage dealt to this unit
        :param duration: how long that buff will last
        :return: None
        """
        self.buffs[1].append((buff, duration))

    def gain_xp(self, xp):
        """
        :param xp: the xp that this unit will receive
        :return: None
        """
        self.xp += xp
        while self.xp >= self.xp_threshold and self.level <= 3:
            self.xp -= self.xp_threshold
            self.level_up()

    def check_move(self, x, y):
        """
        :param x: the delta-x of the move to be checked.
        :param y: the delta-y of the move to be checked.
        :return: whether or not that move is part of this unit's moveset.
        """
        if (x, y) in self.moves:
            return True
        return False

    def check_attack(self, x, y):
        """
        Note: currently, this method uses the unit's moveset as its attackset.
        :param x: the delta-x of the attack to be checked.
        :param y: the delta-y of the attack to be checked.
        :return: whether or not that attack is valid for this unit.
        """
        return self.check_move(x, y)

    def tick(self):
        """
        Causes this unit to "wait" one move. Should be called for all units at the end of each turn.
        Currently, updates buffs and ability cooldowns.
        :return: None
        """
        buffs = []
        for buff in self.buffs[0]:
            if buff[1] > 1:
                buffs.append((buff[0], buff[1] - 1))
        self.buffs[0] = buffs
        buffs = []
        for buff in self.buffs[1]:
            if buff[1] > 1:
                buffs.append((buff[0], buff[1] - 1))
        self.buffs[1] = buffs
        if self.cooldown[0] > 0:
            self.cooldown[0] -= 1
        if self.cooldown[1] > 0:
            self.cooldown[1] -= 1
        if self.protected[1] > 1:
            self.protected[1] -= 1
        else:
            self.protected = [None, 0]

    def get_hp(self):
        """
        :return: the current amount of health this unit has.
        """
        return self.hp

    def get_perhp(self):
        """
        :return: the percentage of the total health this unit has. Used by graphics.
        """
        return self.hp / float(self.base_hp)

    def get_maxhp(self):
        """
        :return: the maximum amount of health this unit has.
        """
        return self.base_hp

    def isDead(self):
        """
        :return: whether or not this unit is still alive.
        """
        return self.hp <= 0

    def get_level(self):
        """
        :return: the current level of the unit.
        """
        return self.level

    def num_abils(self):
        """
        :return: the number of abilities this unit has.
        """
        return len(self.abils)

    def abilities(self):
        """
        :return: a copy of this unit's abilities.
        """
        return self.abils[:]

    def abil_methods(self):
        """
        :return: a copy of this unit's ability methods.
        """
        return self.mabils[:]

    def get_num_input(self, abil):
        """
        This method should be overriden in every piece class.
        :param abil: the number of the ability (0 or 1).
        :return: the number of input squares necessary.
        """
        pass

    def __str__(self):
        """
        Note: this method is used by graphics to assign unit thumbnails, so do not change naively.
        :return: a string representation of this unit.
        """
        if self.name == "Knight":
            return "n" + str(self.level)
        if self.name == "Fort":
            return "r" + str(self.level)
        return self.name[0].lower() + str(self.level)

