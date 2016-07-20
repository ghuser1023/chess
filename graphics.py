from classes import *
import pyglet
from pyglet.window import mouse

SQ_SIZE = 40
P_SIZE = 28
pieceimages = {}
abilityimages = {}

w_length = 400
w_height = 500
top_bar = 60

window = pyglet.window.Window(w_length, w_height)

cur_abils = []
states = ["working", "select_unit", "select_move", "select_attack", "select_ability"]
state = ["select_unit", None]

def loc_to_square(x, y):
    x = x // 40
    y = (y - top_bar) // 40
    if x > 0 and y > 0:
        if x < 9 and y < 9:
            return (x - 1, y - 1)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print(state)
        if state[0] == "working":
            pass
        elif state[0] == "select_unit":
            loc = loc_to_square(x, y)
            if loc != None:
                unit = board.get_unit(loc[0], loc[1])
                if unit != None:
                    unit_selected(unit)
        elif state[0] == "select_move":
            loc = loc_to_square(x, y)
            if loc != None:
                move_selected(loc)
        elif state[0] == "select_attack":
            pass
        elif state[0] == "select_ability":
            pass

def unit_selected(unit):
    state[0] = "select_move"
    state[1] = unit
    cur_abils.clear()
    for x in unit.abilities():
        cur_abils.append(x)

def move_selected(loc):
    (a, b) = board.get_loc(state[1])
    (x, y) = loc
    board.move_unit(state[1], x - a, y - b)
    state[0] = "select_unit"
    state[1] = None

@window.event
def on_draw():
    window.clear()
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ("v2i", (0,0,0,w_height,w_length,w_height,w_length,0)), ("c3B", (127, 127, 127)*4))
    draw_board()
    draw_pieces()
    draw_ability_images()

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

import_images()
import_abilities()

def draw_white_rect(x, y):
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
    ("v2i", (SQ_SIZE*x, SQ_SIZE*y + top_bar, SQ_SIZE*(x+1), SQ_SIZE*y + top_bar,
             SQ_SIZE*(x+1), SQ_SIZE*(y+1) + top_bar, SQ_SIZE*x, SQ_SIZE*(y+1) + top_bar)),
    ("c3B", (255, 255, 255)*4))

def draw_black_rect(x, y):
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
    ("v2i", (SQ_SIZE*x, SQ_SIZE*y + top_bar, SQ_SIZE*(x+1), SQ_SIZE*y + top_bar,
             SQ_SIZE*(x+1), SQ_SIZE*(y+1) + top_bar, SQ_SIZE*x, SQ_SIZE*(y+1) + top_bar)),
    ("c3B", (0, 0, 0)*4))

def draw_board():
    for x in range(1, 9, 2):
        for y in range(1, 9, 2):
            draw_black_rect(x, y)
        for y in range(2, 10, 2):
            draw_white_rect(x, y)
    for x in range(2, 10, 2):
        for y in range(1, 9, 2):
            draw_white_rect(x, y)
        for y in range(2, 10, 2):
            draw_black_rect(x, y)

def draw_pieces():
    for piece in board.get_pieces():
        side = str(piece.side)
        typ = str(piece)
        locx = board.get_loc(piece)[0]*SQ_SIZE + 46
        locy = board.get_loc(piece)[1]*SQ_SIZE + 106
        pieceimages[side + typ].blit(locx, locy)

def draw_ability_images():
    if len(cur_abils) > 0:
        abilityimages[cur_abils[0]].blit(286, 36)
    if len(cur_abils) > 1:
        abilityimages[cur_abils[1]].blit(326, 36)


pyglet.app.run()

        
