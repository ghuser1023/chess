# This file contains other important classes.

from subpieces import *


class Board(object):
    """
    Represents the game board.
    """
    def __init__(self, game):
        self.game = game
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
        if unit.get_side() == game.get_black():
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
        if (unit.get_side() == game.get_white() and unit.check_move(x,y)) \
                or (unit.get_side() == game.get_black() and unit.check_move(x,-y)):
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
        if (attacker.get_side() == game.get_white() and attacker.check_attack(x - a, y - b)) or (
                        attacker.get_side() == game.get_black() and attacker.check_attack(x - a, b - y)):
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
        self.game.get_white().tick()
        self.game.get_black().tick()
        self.game.next_turn()
        if self.game.get_cur_side().get_num_units() == 0:
            game.set_screen("victory")

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


class Game(object):
    """
    Represents the game itself.
    """
    def __init__(self):
        self.board = Board(self)
        self.white = Side("White")
        self.black = Side("Black")
        self.num_turns = 1
        self.cur_side = self.white
        self.initialize_board()
        self.cur_abils = []  # the abilities that are currently displayed
        self.state = ["select_unit", None, 0, [], -1]  # the current state
        self.previous = "title"  # the previous screen
        self.screen = "title"  # the current screen
        self.board_flipped = False  # whether or not the board should be flipped

    def get_previous_screen(self):
        """
        :return: the previous screen.
        """
        return self.previous

    def get_cur_screen(self):
        """
        :return: the current screen.
        """
        return self.screen

    def set_screen(self, screen):
        """
        Changes the current screen.
        :return: None
        """
        self.previous = self.screen
        self.screen = screen

    def edit_cur_abils(self):
        """
        :return: the current abilities.
        """
        return self.cur_abils

    def set_cur_abils(self, abils):
        """
        :param abils: the current abilities to be set.
        :return: None
        """
        self.cur_abils = abils

    def edit_state(self):
        """
        :return: the current game state.
        """
        return self.state

    def set_state(self, state):
        """
        :param state: the state that will be set to the current state.
        :return: None
        """
        self.state = state

    def get_flipped(self):
        """
        :return: whether or not the board should be flipped.
        """
        return self.board_flipped

    def flip(self):
        """
        Toggles the board_flipped state.
        :return: None
        """
        self.board_flipped = not self.board_flipped

    def reset(self, num_turns, cur_side):
        """
        Resets the game board in anticipation of a load.
        :return:
        """
        self.board = Board(self)
        self.white = Side("White")
        self.black = Side("Black")
        self.white.add_opponent(self.black)
        self.black.add_opponent(self.white)
        self.board.set_sides(self.white, self.black)
        if cur_side == 'White':
            self.cur_side = self.white
        elif cur_side == 'Black':
            self.cur_side = self.black
        self.num_turns = num_turns

    def get_cur_side(self):
        """
        :return: the current owner of the move.
        """
        return self.cur_side

    def get_num_turns(self):
        """
        :return: the amount of turns elapsed.
        """
        return self.num_turns

    def switch_side(self):
        """
        Switches the current side moving (called at end of turn).
        :return: None
        """
        self.cur_side = self.cur_side.get_opponent()

    def next_turn(self):
        """
        Increments the number of turns.
        :return: None
        """
        self.num_turns += 1

    def get_board(self):
        """
        :return: the board object
        """
        return self.board

    def get_white(self):
        """
        :return: the white side
        """
        return self.white

    def get_black(self):
        """
        :return: the black side
        """
        return self.black

    def initialize_board(self):
        """
        Initializes self.board conditions.
        :return: None
        """
        self.white.add_opponent(self.black)
        self.black.add_opponent(self.white)
        self.board.set_sides(self.white, self.black)
        for x in range(8):
            wp = Pawn()
            bp = Pawn()
            wp.set_board(self.board)
            wp.set_side(self.white)
            bp.set_board(self.board)
            bp.set_side(self.black)
            self.board.add_unit(wp, x, 1)
            self.board.add_unit(bp, x, 6)
            self.white.add_unit(wp)
            self.black.add_unit(bp)
        row_0 = [Fort(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Fort()]
        row_7 = [Fort(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Fort()]
        column = 0
        for piece in row_0:
            piece.set_board(self.board)
            piece.set_side(self.white)
            self.board.add_unit(piece, column, 0)
            self.white.add_unit(piece)
            column += 1
        column = 0
        for piece in row_7:
            piece.set_board(self.board)
            piece.set_side(self.black)
            self.board.add_unit(piece, column, 7)
            self.black.add_unit(piece)
            column += 1

    def new_game(self):
        """
        Creates a new game.
        :return: None
        """
        self.__init__()
        self.screen = "game"

    def do_nothing(self):
        """
        Does nothing.
        :return: None
        """
        pass

game = Game()
