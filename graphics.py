# This file contains utilities and constants.

from classes import *
import pyglet

sq_size = 40  # the size of each square on the board
p_size = 28  # the size of each piece thumbnail
pieceimages = {}
abilityimages = {}

w_length = 520  # the length of the window
w_height = 480  # the height of the window
top_bar = 80  # the distance from the bottom of the window to the board
hud_cal = 65  # used to calibrate the HUD

piece_calib = 46  # used to calibrate the drawing of pieces on the board
abil_bot_dist = 6  # the vertical downwards distance of the abilities from the top of the HUD
abil_width_dist = 50  # the distance between the two ability thumbnails (left edge to left edge)
abil_init_width = 276  # the distance to the left edge of the first ability
msg_height = w_height - 20  # the height at which messages are drawn at

bar_len = 150  # the length of the health bar
bar_width = 15  # the width of the health bar
bar_height = 50  # the height of the health bar
mbar_height = 30 # the height of the morale bar
name_height = 80  # the height of the displayed name of the piece

exp_init_width = 234  # the distance of the experience point statistic from the left edge
exp_init_height = 50  # the height of the experience point statistic

buff_height = top_bar - hud_cal - 0  # the height of the buff indicators
buff_size = 18  # the size of the buff indicator square
buff_dist = 90  # the distance between the buff indicators

label_calib = sq_size * 23 // 2
side_label_color = (0, 0, 0, 255)  # the default color of the side labels

button_width = 85  # the default width of each button
button_height = 25  # the default height of each button
flip_height = 285  # the height of the board flipping button
b_heights = (250, 375, 405, 450)  # the "big" button heights

title_button_dist = 163  # distance of the title buttons from the bottom of the screen
title_dist = 100  # distance the title is displayed from the top of the screen

thumb_side_dist = 80  # distance the thumbnails are from the sides of the screen
thumb_height = 60  # height of the piece thumbnail buttons
thumb_width = 60  # width of the piece thumbnail buttons
thumb_heights = (370, 300, 230, 160, 90, 20)  # the heights of the piece thumbnails

back_offset = 15  # the height at which the back button is displayed
back_height = 26  # the vertical width of the back button

par_x_offset = 15  # the left margin on the help screen
col_2_offset = 230  # the left margin for the second help column
help_title_y = 20  # the height at which the title is displayed
help_abil_y = 60  # the height at which the ability names are displayed


screens = ("game", "help", "title")  # all possible screens
states = ("working", "select_unit", "unit_selected", "select_squares")  # all possible states


class Utils(object):
    """
    Contains methods that convert screen coordinates (in pixels) to board coordinates/buttons.
    """
    @staticmethod
    def loc_to_square(x, y):
        """
        Converts window pixels to board coordinates.
        :param x: the x-location (in terms of window pixels)
        :param y: the y-location (in terms of window pixels)
        :return: the location (in terms of board coordinates)
        """
        x //= sq_size
        y = (y - top_bar) // sq_size
        if 0 < x < 9 and 0 < y < 9:
            if not game.get_flipped() or game.get_cur_side() == game.get_white():
                return x-1, y-1
            else:
                return x-1, 8-y

    @staticmethod
    def loc_to_ability(x, y):
        """
        Converts window pixels to abilities.
        :param x: the x-location (in terms of window pixels)
        :param y: the y-location (in terms of window pixels)
        :return: the number of the ability selected
        """
        x -= abil_init_width
        y -= top_bar - abil_bot_dist
        if x >= 0 and y >= 0 and x < p_size and y < p_size:
            return 0
        x -= abil_width_dist
        if x >= 0 and y >= 0 and x < p_size and y < p_size and game.edit_state()[1].num_abils() > 1:
            return 1

    @staticmethod
    def loc_to_button(x, y):
        """
        Converts window pixels to buttons.
        :param x: the x-location (in terms of window pixels)
        :param y: the y-location (in terms of window pixels)
        :return: the method that should be called
        """
        y = w_height - y
        if (label_calib - button_width // 2) < x < (label_calib + button_width // 2):
            if b_heights[0] > y > (b_heights[0] - button_height):
                game.switch_side()
                return game.get_board().end_turn
            elif flip_height > y > (flip_height - button_height):
                return Utils.flip_board
            elif b_heights[1] > y > (b_heights[1] - button_height):
                return FileHandling.save
            elif b_heights[2] > y > (b_heights[2] - button_height):
                game.set_state(["select_unit", None, 0, [], -1])
                return FileHandling.load
            elif b_heights[3] > y > (b_heights[3] - button_height):
                game.set_state(["select_unit", None, 0, [], -1])
                return game.new_game
        print("no button clicked")
        return None

    @staticmethod
    def flip_board():
        """
        Changes the board_flipped statistic.
        :return: None
        """
        game.flip()


class Selections(object):
    """
    Contains methods that process and act upon mouse actions.
    """
    error = ""

    @staticmethod
    def select_unit(x, y):
        """
        Selects a unit on the screen.
        :param x: the x-location (in terms of window pixels)
        :param y: the y-location (in terms of window pixels)
        :return: None
        """
        loc = Utils.loc_to_square(x, y)
        if loc is not None:
            unit = game.get_board().get_unit(loc[0], loc[1])
            if unit is not None:
                game.edit_state()[0] = "unit_selected"
                game.edit_state()[1] = unit
                game.edit_cur_abils().clear()
                for x in unit.abilities():
                    game.edit_cur_abils().append(x)

    @staticmethod
    def select_general(method, x, y, error, success):
        """
        A general selection method that calls a method (move or attack).
        :param method: the method to be called (move or attack)
        :param x: the board x-location
        :param y: the board y-location
        :param error: the method name string (used for the error message to be displayed upon failure)
        :return: None
        """
        if game.edit_state()[1].get_side() == game.get_cur_side():
            worked = method(game.edit_state()[1], x, y)
            if worked:
                game.switch_side()
                game.get_board().end_turn()
                game.edit_state()[0] = "select_unit"
                game.edit_state()[1] = None
                game.edit_cur_abils().clear()
                Selections.error = success
            else:
                Selections.error = "That " + error + " is invalid."
        else:
            Selections.error = "It is " + game.get_cur_side().get_name() + " to move."

    @staticmethod
    def select_move(loc):
        """
        Selects a certain move.
        :param loc: the board location of the move destination
        :return: None
        """
        (a, b) = game.get_board().get_loc(game.edit_state()[1])
        (x, y) = loc
        success = game.edit_state()[1].get_type() + " moved from " + file[a]+str(b+1) + " to " + file[x]+str(y+1) + "."
        Selections.select_general(game.get_board().move_unit, x - a, y - b, "move", success)

    @staticmethod
    def select_attack(loc):
        """
        Selects a certain attack.
        :param loc: the board location of the attack target
        :return: None
        """
        if game.get_board().get_unit(loc[0], loc[1]).get_side() == game.edit_state()[1].get_side():
            Selections.error = "No friendly fire."
        else:
            (a, b) = game.get_board().get_loc(game.edit_state()[1])
            (x, y) = loc
            success = game.edit_state()[1].get_type() + " on " + file[a]+str(b+1) + " attacked " + file[x]+str(y+1) + "."
            Selections.select_general(game.get_board().attack_unit, loc[0], loc[1], "attack", success)

    @staticmethod
    def select_ability():
        """
        Selects a certain ability.
        :return: None
        """
        abil = game.edit_state()[4]
        ability = game.edit_state()[1].abil_methods()[abil]
        squares = game.edit_state()[3]
        if game.edit_state()[1].get_side() == game.get_cur_side():
            error = ability(squares)
            if error == "":
                game.edit_state()[0] = "unit_selected"
                game.edit_state()[2] = 0
                game.edit_state()[4] = -1
                game.edit_state()[3].clear()
            else:
                Selections.error = error
                game.edit_state()[2] = game.edit_state()[1].get_num_input(game.edit_state()[4])
                game.edit_state()[3].clear()
        else:
            Selections.error = "It is " + game.get_cur_side().get_name() + " to move."

    @staticmethod
    def select_button(x, y):
        """
        Attempts to select a certain menu button.
        :param x: the x-coordinate (window)
        :param y: the y-coordinate (window)
        :return: whether or not the attempt was successful
        """
        button = Utils.loc_to_button(x, y)
        if button is None:
            return False
        else:
            button()


class FileHandling():
    """
    Contains methods that use external files (image loading and load/save systems).
    """
    @staticmethod
    def save():
        """
        Saves the game.
        :return: None
        """
        try:
            f = open("save.txt", 'w')
            f.write(str(game.get_num_turns()) + "\n")
            f.write(str(game.get_cur_side().get_name() + "\n"))
            pieces = game.get_board().get_pieces()
            for piece in pieces:
                f.write(piece.get_save_data())
            f.write("End of file.\n")
        except IOError:
            pass

    @staticmethod
    def load():
        """
        Loads the game.
        :return: whether or not a save file was found.
        """
        try:
            f = open("save.txt", 'r')
            num_turns = int(f.readline()[:-1])
            cur_side = f.readline()[:-1]
            game.reset(num_turns, cur_side)
            typ = f.readline()[:-1]

            while typ != "End of file.":
                piece = unit_dict[typ]()
                side = f.readline()[:-1]
                if side == 'White':
                    side = game.get_white()
                elif side == 'Black':
                    side = game.get_black()
                loc = f.readline()[:-1]
                loc = (loc[0:1], loc[2:3])
                game.get_board().add_unit(piece, int(loc[0]), int(loc[1]))
                side.add_unit(piece)
                piece.set_board(game.get_board())
                piece.set_side(side)

                buff0 = f.readline()[:-1]
                while buff0 != "":
                    buff0 = buff0.split()
                    piece.buff_attack(float(buff0[0]), int(buff0[1]))
                    buff0 = f.readline()[:-1]
                buff1 = f.readline()[:-1]
                while buff1 != "":
                    buff1 = buff1.split()
                    piece.buff_health(float(buff1[0]), int(buff1[1]))
                    buff1 = f.readline()[:-1]

                hp = float(f.readline()[:-1])
                xp = int(f.readline()[:-1])
                level_mult = float(f.readline()[:-1])
                level = int(f.readline()[:-1])
                cooldown = f.readline()[:-1]
                cooldown = cooldown.split()
                cooldown = [int(cooldown[0]), int(cooldown[1])]
                protect = f.readline()[:-1]
                if protect == '':
                    protected = (None, 0)
                    p_loc = (-1, -1)
                else:
                    protect = protect.split()
                    protected = (True, int(protect[2]))
                    p_loc = (int(protect[0]), int(protect[1]))
                piece.load_save_data(hp, xp, level_mult, level, cooldown, protected, p_loc)

                typ = f.readline()[:-1]
            return True
        except IOError:
            return False

    @staticmethod
    def import_abilities():
        """
        Imports all of the ability thumbnails. The names are important.
        :return: None
        """
        abilityimages["arrowstorm"] = pyglet.resource.image('abilities/Arrows.png')
        abilityimages["solidarity"] = pyglet.resource.image('abilities/RedSquare.png')
        abilityimages["aerial_defense"] = pyglet.resource.image('abilities/Arrows.png')
        abilityimages["fortify"] = pyglet.resource.image('abilities/RedSquare.png')
        abilityimages["call_to_arms"] = pyglet.resource.image('abilities/Call to Arms.png')
        abilityimages["charge"] = pyglet.resource.image('abilities/Charge.png')
        abilityimages["chivalry"] = pyglet.resource.image('abilities/Chivalry.png')
        abilityimages["influence"] = pyglet.resource.image('abilities/Influence.png')
        abilityimages["piety"] = pyglet.resource.image('abilities/Piety.png')
        abilityimages["rally"] = pyglet.resource.image('abilities/Rally.png')
        abilityimages["regeneration"] = pyglet.resource.image('abilities/Regen.png')
        abilityimages["subterfuge"] = pyglet.resource.image('abilities/Subterfuge.png')

    @staticmethod
    def import_images():
        """
        Imports all of the piece thumbnails. The names are important.
        :return: None
        """
        pieceimages["wr1"] = pyglet.resource.image('sprites/WFort1.png')
        pieceimages["wn1"] = pyglet.resource.image('sprites/WKnight1.png')
        pieceimages["wb1"] = pyglet.resource.image('sprites/WBishop1.png')
        pieceimages["wq1"] = pyglet.resource.image('sprites/WQueen1.png')
        pieceimages["wk1"] = pyglet.resource.image('sprites/WKing1.png')
        pieceimages["wp1"] = pyglet.resource.image('sprites/WPawn1.png')

        pieceimages["wr2"] = pyglet.resource.image('sprites/WFort2.png')
        pieceimages["wn2"] = pyglet.resource.image('sprites/WKnight2.png')
        pieceimages["wb2"] = pyglet.resource.image('sprites/WBishop2.png')
        pieceimages["wq2"] = pyglet.resource.image('sprites/WQueen2.png')
        pieceimages["wk2"] = pyglet.resource.image('sprites/WKing2.png')
        pieceimages["wp2"] = pyglet.resource.image('sprites/WPawn2.png')

        pieceimages["wr3"] = pyglet.resource.image('sprites/WFort3.png')
        pieceimages["wn3"] = pyglet.resource.image('sprites/WKnight3.png')
        pieceimages["wb3"] = pyglet.resource.image('sprites/WBishop3.png')
        pieceimages["wq3"] = pyglet.resource.image('sprites/WQueen3.png')
        pieceimages["wk3"] = pyglet.resource.image('sprites/WKing3.png')
        pieceimages["wp3"] = pyglet.resource.image('sprites/WPawn3.png')

        pieceimages["br1"] = pyglet.resource.image('sprites/BFort1.png')
        pieceimages["bn1"] = pyglet.resource.image('sprites/BKnight1.png')
        pieceimages["bb1"] = pyglet.resource.image('sprites/BBishop1.png')
        pieceimages["bq1"] = pyglet.resource.image('sprites/BQueen1.png')
        pieceimages["bk1"] = pyglet.resource.image('sprites/BKing1.png')
        pieceimages["bp1"] = pyglet.resource.image('sprites/BPawn1.png')

        pieceimages["br2"] = pyglet.resource.image('sprites/BFort2.png')
        pieceimages["bn2"] = pyglet.resource.image('sprites/BKnight2.png')
        pieceimages["bb2"] = pyglet.resource.image('sprites/BBishop2.png')
        pieceimages["bq2"] = pyglet.resource.image('sprites/BQueen2.png')
        pieceimages["bk2"] = pyglet.resource.image('sprites/BKing2.png')
        pieceimages["bp2"] = pyglet.resource.image('sprites/BPawn2.png')

        pieceimages["br3"] = pyglet.resource.image('sprites/BFort3.png')
        pieceimages["bn3"] = pyglet.resource.image('sprites/BKnight3.png')
        pieceimages["bb3"] = pyglet.resource.image('sprites/BBishop3.png')
        pieceimages["bq3"] = pyglet.resource.image('sprites/BQueen3.png')
        pieceimages["bk3"] = pyglet.resource.image('sprites/BKing3.png')
        pieceimages["bp3"] = pyglet.resource.image('sprites/BPawn3.png')

FileHandling.import_images()
FileHandling.import_abilities()