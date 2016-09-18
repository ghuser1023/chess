# This file contains other important classes.

from subpieces import *


def initialize_board():
    """
    Initializes board conditions.
    :return: None
    """
    white.other = black
    black.other = white
    board.set_sides(white, black)
    for x in range(8):
        wp = Pawn()
        bp = Pawn()
        wp.set_board(board)
        wp.set_side(white)
        bp.set_board(board)
        bp.set_side(black)
        board.add_unit(wp, x, 1)
        board.add_unit(bp, x, 6)
        white.add_unit(wp)
        black.add_unit(bp)
    row_0 = [Fort(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Fort()]
    row_7 = [Fort(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Fort()]
    column = 0
    for piece in row_0:
        piece.set_board(board)
        piece.set_side(white)
        board.add_unit(piece, column, 0)
        white.add_unit(piece)
        column += 1
    column = 0
    for piece in row_7:
        piece.set_board(board)
        piece.set_side(black)
        board.add_unit(piece, column, 7)
        black.add_unit(piece)
        column += 1


class Board(object):
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
        return self.board[x][y]

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

    def qualify_move(self, unit, loc):
        """
        Alters the delta-x and delta-y of a unit to correct for black/white discrepancies.
        :param unit: the unit to be moved/attacked
        :param loc: the delta-(x, y) of the move/attack
        :return: (x, y) if white; (x, -y) if black
        """
        if unit.get_side() == black:
            return (loc[0], -loc[1])
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
        if (unit.get_side() == white and unit.check_move(x,y)) or (unit.get_side() == black and unit.check_move(x,-y)):
            if self.valid(loc[0] + x, loc[1] + y) and self.valid_path(unit, loc[0] + x, loc[1] + y):
                self.board[loc[0] + x][loc[1] + y] = unit
                self.board[loc[0]][loc[1]] = None
                self.units[unit] = (loc[0] + x, loc[1] + y)
                return True
        else:
            return False

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
        if (attacker.get_side() == white and attacker.check_attack(x - a, y - b)) or (
                        attacker.get_side() == black and attacker.check_attack(x - a, b - y)):
            defender.deal_damage(attacker.effective_strength())
            if defender.isDead():
                self.remove_unit(defender)
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
            if x.isDead():
                x.side.add_morale(-1 * x.get_value())
                x.side.other.add_morale(0.5 * x.get_value())
                x.side.remove_unit(x)
                self.remove_unit(x)
            else:
                x.tick()

    def get_pieces(self):
        """
        :return: a list of the pieces on the board.
        """
        return list(self.units.keys())


class Side(object):
    def __init__(self, name):
        self.units = []
        self.morale = 100
        self.other = None
        self.name = name

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

    def remove_unit(self, unit):
        """
        Removes a unit from this side.
        :param unit: the unit to be removed
        :return: None
        """
        self.units.pop(unit)

    def add_morale(self, morale):
        """
        Adds morale to this side
        :param morale: the morale to be added
        :return: None
        """
        self.morale += morale
        if self.morale > 100:
            self.morale = 100
        if self.morale < 0:
            self.morale = 0

    def get_obdedience(self):
        """
        :return: a value dictating the possibility of a unit's loyalty.
        """
        if self.morale >= 50:
            return 1
        else:
            return 0.02 * self.morale

    def get_num_abilities(self):
        """
        :return: the number of abilities that can be used on any given turn.
        """
        num = 0
        if self.morale >= 15:
            num += 1
        if self.morale >= 40:
            num += 1
        if self.morale >= 80:
            num += 1
        return num

    def __str__(self):
        """
        Note: this method is used by graphics. Change with caution.
        :return: a string representation of this side.
        """
        return self.name.lower()


board = Board()
white = Side("White")
black = Side("Black")
initialize_board()
