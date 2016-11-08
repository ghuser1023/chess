# This file contains other important classes.

from subpieces import *


class Board(object):
    """
    Represents the game board.
    """
    def __init__(self):
        self.board = []
        self.units = {}
        self.side1 = None
        self.side2 = None
        for x in range(8):
            row = []
            for y in range(8):
                row.append(None)
            self.board.append(row)

    def set_sides(self, side1, side2):
        """
        Adds the two side objects (Black, White) to this board.
        :param side1: the first side
        :param side2: the second side
        :return: None
        """
        self.side1 = side1
        self.side2 = side2

    def add_unit(self, unit, x, y):
        """
        Adds a unit to this board.
        :param unit: the unit to be added
        :param x: the x-location of the unit
        :param y: the y-location of the unit
        :return: None
        """
        self.board[x][y] = unit
        self.units[unit] = (x, y)

    def get_unit(self, x, y):
        """
        Gets a unit from the board.
        :param x: the x-location to be searched
        :param y: the y-location to be searched
        :return: the unit at target location
        """
        if self.valid(x, y):
            return self.board[x][y]
        else:
            return None

    def get_loc(self, unit):
        """
        Returns the location of a unit on the board.
        :param unit: the unit to be located
        :return: the location (x, y) where the unit exists
        """
        return self.units[unit]

    def remove_unit(self, unit):
        """
        Removes a unit from the board.
        :param unit: the unit to be removed
        :return: None
        """
        (x, y) = self.units[unit]
        self.board[x][y] = None
        self.units.pop(unit)
        unit.get_side().remove_unit(unit)

    def qualify_move(self, unit, loc):
        """
        Alters the delta-x and delta-y of a unit to correct for black/white discrepancies.
        :param unit: the unit to be moved/attacked
        :param loc: the delta-(x, y) of the move/attack
        :return: (x, y) if white; (x, -y) if black
        """
        if unit.get_side() == self.side2:
            return loc[0], -loc[1]
        else:
            return loc

    def move_unit(self, unit, x, y):
        """
        Moves a unit on the board.
        :param unit: the unit to be moved
        :param x: the delta-x of the move
        :param y: the delta-y of the move
        :return: whether or not the move was successful
        """
        loc = self.units[unit]
        if (unit.get_side() == self.side1 and unit.check_move(x,y)) \
                or (unit.get_side() == self.side2 and unit.check_move(x,-y)):
            if self.valid(loc[0] + x, loc[1] + y) and self.valid_path(unit, loc[0] + x, loc[1] + y):
                self.board[loc[0] + x][loc[1] + y] = unit
                self.board[loc[0]][loc[1]] = None
                self.units[unit] = (loc[0] + x, loc[1] + y)
                if type(unit) == Pawn and (loc[1] + y == 0 or loc[1] + y == 7):
                    self.promote(unit)
                return True
        else:
            return False

    def promote(self, pawn):
        """
        Promotes a pawn which has advanced to the 8th rank to a knight.
        :param pawn: the pawn to be promoted.
        :return: None
        """
        x, y = self.units[pawn]
        pawn.get_side().remove_unit(pawn)
        self.remove_unit(pawn)
        knight = Knight()
        while knight.get_level() < pawn.get_level():
            knight.level_up()
        damage = int((1-pawn.get_perhp())*knight.get_key_stats()[1])
        knight.deal_damage(damage)
        pawn.get_side().add_unit(knight)
        self.add_unit(knight, x, y)

    def attack_unit(self, attacker, x, y):
        """
        Invokes an attack from one unit onto another.
        :param attacker: the unit doing the attacking.
        :param x: the x-location of the attack
        :param y: the y-location of the attack
        :return: whether or not the attack was successful.
        """
        (a, b) = self.units[attacker]
        defender = self.board[x][y]
        if (attacker.get_side() == self.side1 and attacker.check_attack(x - a, y - b)) or (
                        attacker.get_side() == self.side2 and attacker.check_attack(x - a, b - y)):
            defender.deal_damage(attacker.effective_strength())
            if defender.isDead():
                attacker.gain_xp(defender.get_xp_drop())
            return True
        else:
            return False

    def valid(self, x, y):
        """
        Determines whether or not a square is on the board.
        :param x: the x-location
        :param y: the y-location
        :return: whether or not (x, y) is a valid square
        """
        if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
            return True
        return False

    def valid_path(self, unit, x, y):
        """
        Determines whether or not the path of a unit moving to (x, y) is clear.
        :param unit: the unit in question
        :param x: the x-location of the destination
        :param y: the y-location of the destination
        :return: None
        """
        (a, b) = self.units[unit]
        if abs(x - a) <= 1 and abs(y - b) <= 1:
            return True
        elif type(unit) is Knight:
            return True
        else:
            if x == a:
                c = 0
            else:
                c = (x - a) // abs(x - a)
            if y == b:
                d = 0
            else:
                d = (y - b) // abs(y - b)
            while a != x or b != y:
                a += c
                b += d
                if self.board[a][b] != None:
                    return False
            return True

    def end_turn(self):
        """
        Ends a turn; updates morale, removes dead units, and updates units.
        :return: None
        """
        for x in self.units.keys():
            x.tick()
        self.side1.tick()
        self.side2.tick()

    def get_pieces(self):
        """
        :return: a list of the pieces on the board.
        """
        return self.units.keys()

    def get_morale(self, unit):
        """
        Calculates the morale of a certain unit based on adjacent pieces, piece health, and the king.
        :param unit: the unit whose morale will be calculated.
        :return: the morale of that unit as a percentage.
        """
        health = unit.get_perhp()
        num_local = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.valid(self.get_loc(unit)[0] + i, self.get_loc(unit)[1] + j):
                    checked_unit = self.get_unit(self.get_loc(unit)[0] + i, self.get_loc(unit)[1] + j)
                    if checked_unit is not None:
                        if checked_unit.get_side() == unit.get_side():
                            num_local += 1
                        if checked_unit.get_side() != unit.get_side():
                            num_local -= 1
        num_local *= 0.05
        morale = 0.5 + (health - 0.5)/2 + num_local
        if not unit.get_side().king_alive():
            morale -= 0.25
        if unit.get_side().get_rallied():
            morale += 0.25
        if morale > 1 or unit.get_side().get_influenced():
            morale = 1
        if morale < 0:
            morale = 0
        return morale
    
    def determine_value(self, side):
        """
        Used by the AI method. Determines a bs valuation of the position of a side.
        Currently uses the sum of (piece health * piece value) across all pieces of a side.
            Needs to be updated for current purposes; rn will return the same number for all AI move choices
        :param side: the side which will have its value determined.
        :return: None
        """
        value = 0
        for unit in self.units.keys():
            if unit.get_side() == side:
                value += unit.get_perhp()*unit.get_value()
        return value


class Side(object):
    """
    Represents an individual side/army (typically white and black).
    """
    def __init__(self, name):
        self.units = []
        self.other = None
        self.name = name
        self.has_king = False
        self.rallied = 0
        self.influenced = False

    def rally(self):
        """
        Rallies this side.
        :return: None
        """
        self.rallied = 5

    def get_rallied(self):
        """
        :return: whether or not this side is rallied.
        """
        return self.rallied > 0

    def influence(self):
        """
        Influences this side.
        :return: None
        """
        self.influenced = True

    def get_influenced(self):
        """
        :return: whether or not this side is influenced.
        """
        return self.influenced

    def king_alive(self):
        """
        :return: whether or not the king is still alive.
        """
        return self.has_king

    def get_num_units(self):
        """
        :return: the total number of units still alive.
        """
        return len(self.units)

    def add_opponent(self, other):
        """
        :param other: the opposing side
        :return: None
        """
        self.other = other

    def get_opponent(self):
        """
        :return: the opposing side
        """
        return self.other

    def get_name(self):
        """
        Note: this method is used by graphics. Change with caution.
        :return: this side's name
        """
        return self.name

    def add_unit(self, unit):
        """
        Adds a unit to this side.
        :param unit: the unit to be added to this side
        :return: None
        """
        self.units.append(unit)
        if type(unit) == King:
            self.has_king = True

    def remove_unit(self, unit):
        """
        Removes a unit from this side.
        :param unit: the unit to be removed
        :return: None
        """
        self.units.remove(unit)
        if type(unit) == King:
            self.has_king = False

    def tick(self):
        """
        Decreases the remaining time left on the rally method.
        :return: None
        """
        if self.rallied > 0:
            self.rallied -= 1
        self.influenced = False

    def __str__(self):
        """
        Note: this method is used by graphics. Change with caution.
        :return: a string representation of this side.
        """
        return self.name.lower()

