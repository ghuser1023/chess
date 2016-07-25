# This file contains the drawing class and the pyglet application loop.

from pyglet.window import mouse
from graphics import *

window = pyglet.window.Window(w_length, w_height)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print(state)
        if state[0] == "working":
            pass
        elif state[0] == "select_unit":
            Selections.select_unit(x, y)
        elif state[0] == "unit_selected":
            loc = Utils.loc_to_square(x, y)
            if loc != None:
                if board.get_unit(loc[0], loc[1]) == None:
                    Selections.select_move(loc)
                elif board.get_unit(loc[0], loc[1]) == state[1]:
                    state[0] = "select_unit"
                    state[1] = None
                else:
                    Selections.select_attack(loc)
            else:
                abil = Utils.loc_to_ability(x, y)
                if (abil != None):
                    Selections.select_ability(loc)


class Draw:
    @staticmethod
    def draw_white_rect(x, y):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ("v2i", (sq_size*x, sq_size*y + top_bar, sq_size*(x+1), sq_size*y + top_bar,
                 sq_size*(x+1), sq_size*(y+1) + top_bar, sq_size*x, sq_size*(y+1) + top_bar)),
            ("c3B", (255, 255, 255)*4))

    @staticmethod
    def draw_black_rect(x, y):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ("v2i", (sq_size*x, sq_size*y + top_bar, sq_size*(x+1), sq_size*y + top_bar,
                 sq_size*(x+1), sq_size*(y+1) + top_bar, sq_size*x, sq_size*(y+1) + top_bar)),
            ("c3B", (0, 0, 0)*4))

    @staticmethod
    def draw_board():
        for x in range(1, 9, 2):
            for y in range(1, 9, 2):
                Draw.draw_black_rect(x, y)
            for y in range(2, 10, 2):
                Draw.draw_white_rect(x, y)
        for x in range(2, 10, 2):
            for y in range(1, 9, 2):
                Draw.draw_white_rect(x, y)
            for y in range(2, 10, 2):
                Draw.draw_black_rect(x, y)

    @staticmethod
    def draw_pieces():
        for piece in board.get_pieces():
            side = str(piece.side)[0]
            typ = str(piece)
            locx = board.get_loc(piece)[0]*sq_size + piece_calib
            locy = board.get_loc(piece)[1]*sq_size + top_bar + piece_calib
            if piece == state[1]:
                label = pyglet.text.Label(piece.get_name(), font_name='Courier New', font_size=14, bold = True,
                                          x = sq_size, y = name_height, anchor_x='left', anchor_y='center')
                label.draw()
                Draw.draw_bar(piece.get_perhp(), (0, 255, 0), bar_height)
                pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                     ("v2i", (locx - 2, locy - 2, locx - 2, locy + p_size + 2,
                            locx + p_size + 2, locy + p_size + 2, locx + p_size + 2, locy - 2)),
                     ("c3B", (0, 255, 0) * 4))
            pieceimages[side + typ].blit(locx, locy)

    @staticmethod
    def draw_ability_images():
        if len(cur_abils) > 0:
            abilityimages[cur_abils[0]].blit(abil_init_width, top_bar - abil_bot_dist)
        if len(cur_abils) > 1:
            abilityimages[cur_abils[1]].blit(abil_init_width + abil_width_dist, top_bar - abil_bot_dist)

    @staticmethod
    def draw_message():
        if Selections.error != "":
            label = pyglet.text.Label(Selections.error, font_name = 'Courier New', font_size = 11, bold = True,
                                      x = w_length // 2, y = msg_height, anchor_x = 'center', anchor_y = 'center')
            label.draw()

    @staticmethod
    def draw_bar(percent, color, height):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
             ("v2i", (sq_size, height, sq_size, height + bar_width,
                      sq_size + bar_len, height + bar_width, sq_size + bar_len, height)),
             ("c3B", (0, 0, 0) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
             ("v2i", (sq_size + 1, height + 1, sq_size + 1, height + bar_width - 1,
                      sq_size - 1 + bar_len, height + bar_width - 1, sq_size - 1 + bar_len, height + 1)),
             ("c3B", (255, 0, 0) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
             ("v2i", (sq_size + 1, height + 1, sq_size + 1, height + bar_width - 1,
                      sq_size-1+int(bar_len*percent), height+bar_width-1, sq_size-1+int(bar_len*percent), height+1)),
             ("c3B", color * 4))

@window.event
def on_draw():
    window.clear()
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ("v2i", (0,0,0,w_height,w_length,w_height,w_length,0)), ("c3B", (127, 127, 127)*4))
    Draw.draw_board()
    Draw.draw_pieces()
    Draw.draw_ability_images()
    Draw.draw_message()


pyglet.app.run()