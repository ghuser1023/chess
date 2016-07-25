# This file contains other important classes.

from subpieces import *

def initialize_board():
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
        self.side1 = side1
        self.side2 = side2

    def add_unit(self, unit, x, y):
        self.board[x][y] = unit
        self.units[unit] = (x, y)

    def get_unit(self, x, y):
        return self.board[x][y]

    def get_loc(self, unit):
        return self.units[unit]

    def remove_unit(self, unit):
        (x, y) = self.units[unit]
        self.board[x][y] = None
        self.units.pop(unit)

    def move_unit(self, unit, x, y):
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
        (a, b) = self.units[attacker]
        defender = self.board[x][y]
        if (attacker.get_side() == white and attacker.check_attack(x - a, y - b)) or (
                        attacker.get_side() == black and attacker.check_attack(x - a, b - y)):
            defender.deal_damage(attacker.effective_strength())
            print("An attack occured!")
            print("Defender's HP:", defender.get_hp())
            if defender.isDead():
                self.remove_unit(defender)
            return True
        else:
            return False

    def valid(self, x, y):
        if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
            return True
        return False

    def valid_path(self, unit, x, y):
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
        for x in self.units.keys():
            if x.isDead():
                x.side.add_morale(-1 * x.get_value())
                x.side.other.add_morale(0.5 * x.get_value())
                x.side.remove_unit(x)
                self.remove_unit(x)
            else:
                x.tick()

    def get_pieces(self):
        return list(self.units.keys())


class Side(object):
    def __init__(self, name):
        self.units = []
        self.morale = 100
        self.other = None
        self.name = name

    def add_opponent(self, other):
        self.other = other

    def get_opponent(self):
        return self.other

    def get_name(self):
        return self.name

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.pop(unit)

    def add_morale(self, morale):
        self.morale += morale
        if self.morale > 100:
            self.morale = 100
        if self.morale < 0:
            self.morale = 0

    def get_obdedience(self, morale):
        if morale >= 50:
            return 1
        else:
            return 0.02 * morale

    def get_num_abilities(self, morale):
        num = 0
        if morale >= 15:
            num += 1
        if morale >= 40:
            num += 1
        if morale >= 80:
            num += 1
        return num

    def __str__(self):
        return self.name.lower()


board = Board()
white = Side("White")
black = Side("Black")
initialize_board()
