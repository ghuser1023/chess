# This file contains everything necessary for making AI decisions.

from classes import *


class Game(object):
    """
    Represents the game itself.
    """
    def __init__(self):
        self.board = Board()
        self.white = Side("White")
        self.black = Side("Black")
        self.num_turns = 1
        self.cur_side = self.white
        self.initialize_board()
        self.cur_abils = []  # the abilities that are currently displayed
        self.state = ["select_unit", None, 0, [], -1]  # the current state
        self.previous = "title"  # the previous screen
        self.screen = "title"  # the current screen
        self.board_flipped = False
        self.ai_side = None
        self.ai = None

    def make_ai_game(self, side):
        """
        Makes the game an AI game.
        :param side: what side the AI is playing
        :return: None
        """
        self.ai_side = side
        self.ai = AI(side, self)

    def get_ai_side(self):
        """
        :return: the side the AI is playing.
        """
        return self.ai_side

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
        self.board = Board()
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
        self.board.end_turn()
        if self.get_cur_side().get_num_units() == 0:
            self.set_screen("victory")
        if self.get_cur_side() == self.ai_side:
            self.ai.choose_decision()
            self.next_turn()

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


class AI(object):
    """
    Represents an extremely dumb chess AI.
    """
    def __init__(self, side, game_repr):
        self.side = side
        self.game = game_repr
        self.board_copy = None
        self.white_copy = None
        self.black_copy = None

    def copy_board(self):
        """
        Copies the current game board to the temporary copy held by the AI.
        :return: None
        """
        board = self.game.get_board()
        self.board_copy = Board()
        self.white_copy = Side("C_White")
        self.black_copy = Side("C_Black")
        for piece in board.get_pieces():
            new_piece = type(piece)()
            new_piece.load_save_data(piece.get_save_data_raw())
            self.board_copy.add_unit(new_piece, board.get_loc(piece)[0], board.get_loc(piece)[1])
            new_piece.set_board(self.board_copy)
            if piece.get_side() == self.game.get_white():
                self.white_copy.add_unit(new_piece)
                new_piece.set_side(self.white_copy)
            else:
                self.black_copy.add_unit(new_piece)
                new_piece.set_side(self.black_copy)

    def choose_decision(self):
        """
        Executes the "best" move found.
        Current AI "strategy":
            Casts all abilities that have a chance of working.
                Requires calculating a "perceived benefit" for several abilities; use threshold
            Makes all attacks that are valid.
            Moves a high-valued piece out of a calculated danger zone or threatens an enemy high-valued piece.
                Requires optimizing across all possible moves -- hence copy_board and determine_value
        :return: None
        """
        pass


game = Game()
