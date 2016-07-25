# This file contains graphics, utilities, and constants.

from classes import *
import pyglet

sq_size = 40
p_size = 28
pieceimages = {}
abilityimages = {}

w_length = 400
w_height = 460
top_bar = 60

piece_calib = 46
abil_bot_dist = 6
abil_width_dist = 50
abil_init_width = 276
msg_height = w_height - 20

bar_len = 150
bar_width = 15
bar_height = 50
name_height = 80

exp_init_width = 234
exp_init_height = 50

cur_abils = []
cur_side = white
states = ["working", "select_unit", "unit_selected"]
state = ["select_unit", None]


class Utils:
    @staticmethod
    def loc_to_square(x, y):
        x //= sq_size
        y = (y - top_bar) // sq_size
        if x > 0 and y > 0:
            if x < 9 and y < 9:
                return (x - 1, y - 1)

    @staticmethod
    def loc_to_ability(x, y):
        pass


class Selections:
    error = ""

    @staticmethod
    def select_unit(x, y):
        loc = Utils.loc_to_square(x, y)
        if loc != None:
            unit = board.get_unit(loc[0], loc[1])
            if unit != None:
                state[0] = "unit_selected"
                state[1] = unit
                cur_abils.clear()
                for x in unit.abilities():
                    cur_abils.append(x)

    @staticmethod
    def select_general(method, x, y, error):
        global cur_side
        if state[1].get_side() == cur_side:
            worked = method(state[1], x, y)
            if worked:
                cur_side = cur_side.get_opponent()
                state[0] = "select_unit"
                state[1] = None
                cur_abils.clear()
                Selections.error = ""
            else:
                Selections.error = "That " + error + " is invalid."
        else:
            Selections.error = "It is " + cur_side.get_name() + " to move."

    @staticmethod
    def select_move(loc):
        (a, b) = board.get_loc(state[1])
        (x, y) = loc
        Selections.select_general(board.move_unit, x - a, y - b, "move")

    @staticmethod
    def select_attack(loc):
        if board.get_unit(loc[0], loc[1]).get_side() == state[1].get_side():
            Selections.error = "No friendly fire."
        else:
            Selections.select_general(board.attack_unit, loc[0], loc[1], "attack")

    @staticmethod
    def select_ability(loc):
        pass

class FileHandling():
    @staticmethod
    def import_abilities():
        abilityimages["arrowstorm"] = pyglet.resource.image('abilities/Arrows.png')
        abilityimages["aerial_defense"] = pyglet.resource.image('abilities/Arrows.png')
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