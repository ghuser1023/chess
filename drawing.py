# This file contains the drawing methods for the game screen.

from graphics import *
import pyglet

class Draw:
    """
    Contains graphical methods; responsible for actual displays.
    """
    @staticmethod
    def draw_white_rect(x, y):
        """
        Draws a white square for the board coordinates (x, y).
        :param x: the board x-location.
        :param y: the board y-location.
        :return: None
        """
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ("v2i", (sq_size*x, sq_size*y + top_bar, sq_size*(x+1), sq_size*y + top_bar,
                 sq_size*(x+1), sq_size*(y+1) + top_bar, sq_size*x, sq_size*(y+1) + top_bar)),
            ("c3B", (255, 220, 185)*4))

    @staticmethod
    def draw_black_rect(x, y):
        """
        Draws a black square for the board coordinates (x, y).
        :param x: the board x-location.
        :param y: the board y-location.
        :return: None
        """
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ("v2i", (sq_size*x, sq_size*y + top_bar, sq_size*(x+1), sq_size*y + top_bar,
                 sq_size*(x+1), sq_size*(y+1) + top_bar, sq_size*x, sq_size*(y+1) + top_bar)),
            ("c3B", (90, 60, 30)*4))

    @staticmethod
    def draw_board():
        """
        Draws the board itself.
        :return: None
        """
        th = 1
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ("v2i", (sq_size - th, sq_size + top_bar - th, sq_size - th, top_bar + sq_size * 9 + th,
                                      sq_size*9+th, sq_size*9+top_bar+th, sq_size*9+th, sq_size+top_bar-th)),
                             ("c3B", (0, 0, 0) * 4))
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
        """
        Draws all the pieces and calls the relevant HUD method.
        :return: None
        """
        for piece in game.get_board().get_pieces():
            side = str(piece.side)[0]
            typ = str(piece)[:1]
            lvl = piece.get_level()
            locx = game.get_board().get_loc(piece)[0] * sq_size + piece_calib
            if not game.get_flipped() or game.get_cur_side() == game.get_white():
                locy = game.get_board().get_loc(piece)[1] * sq_size + top_bar + piece_calib
            else:
                locy = (7 - game.get_board().get_loc(piece)[1]) * sq_size + top_bar + piece_calib
            # Drawing the "piece activated by chivalry" indicator (yellow)
            if piece.get_protected():
                pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                                     ("v2i", (locx - 2, locy - 2, locx - 2, locy + p_size + 2,
                                              locx + p_size + 2, locy + p_size + 2, locx + p_size + 2, locy - 2)),
                                     ("c3B", (255, 255, 0) * 4))
            if piece == game.edit_state()[1] and piece is not None:
                Draw.draw_active(piece, locx, locy)
            pieceimages[side + typ + str(lvl)].blit(locx, locy)
        if game.edit_state()[1] is None:
            Draw.draw_passive()

    @staticmethod
    def draw_active(piece, locx, locy):
        """
        Draws the active HUD.
        :param piece: the piece selected.
        :param locx: the x-location of the piece.
        :param locy: the y-location of the piece.
        :return: None
        """
        # Drawing the name of the piece
        label = pyglet.text.Label(piece.get_name(), font_name='Courier New', font_size=14, bold=True,
                                  x=sq_size, y=top_bar + name_height - hud_cal, anchor_x='left',
                                  anchor_y='center')
        label.draw()
        # Drawing the health bar
        Draw.draw_bar(piece.get_perhp(), (0, 255, 0), bar_height)
        text = str("{:.1f}".format(piece.get_hp())) + "/" + str("{:.1f}".format(piece.get_maxhp()))
        label = pyglet.text.Label(text, font_name='Courier New', font_size=10, bold=False,
                                  x=sq_size + bar_len // 2, y=top_bar + bar_height + bar_width // 2 - hud_cal,
                                  anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        label.draw()
        # Drawing the morale bar
        Draw.draw_bar(game.get_board().get_morale(piece), (125, 125, 255), mbar_height)
        text = str(int(game.get_board().get_morale(piece) * 100)) + "/100"
        label = pyglet.text.Label(text, font_name='Courier New', font_size=10, bold=False,
                                  x=sq_size + bar_len // 2, y=top_bar + mbar_height + bar_width // 2 - hud_cal,
                                  anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        label.draw()
        # Drawing the buff indicators
        Draw.draw_buffs(piece.str_buff(), (255, 200, 125), sq_size)
        Draw.draw_buffs(piece.def_buff(), (200, 200, 255), sq_size + buff_dist)
        # Drawing the experience
        Draw.draw_exp(piece.get_cur_xp(), piece.get_max_xp())
        # Drawing the "piece selected" indicator (green)
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ("v2i", (locx - 2, locy - 2, locx - 2, locy + p_size + 2,
                                      locx + p_size + 2, locy + p_size + 2, locx + p_size + 2, locy - 2)),
                             ("c3B", (0, 255, 0) * 4))

    @staticmethod
    def draw_ability_images():
        """
        Draws the ability images.
        :return: None
        """
        if game.edit_state()[4] != -1:
            x = abil_init_width + abil_width_dist * game.edit_state()[4]
            y = top_bar - abil_bot_dist
            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                                 ("v2i", (x - 2, y - 2, x - 2, y + p_size + 2,
                                          x + p_size + 2, y + p_size + 2, x + p_size + 2, y - 2)),
                                 ("c3B", (255, 127, 63) * 4))
        if len(game.edit_cur_abils()) > 0:
            abilityimages[game.edit_cur_abils()[0]].blit(abil_init_width, top_bar - abil_bot_dist)
            label = pyglet.text.Label(str(game.edit_state()[1].get_cd_1()), font_name='Courier New', font_size=16, bold=True,
                                      x=abil_init_width + p_size//2, y=top_bar - abil_bot_dist - sq_size//2,
                                      anchor_x='center', anchor_y='center')
            label.draw()
        if len(game.edit_cur_abils()) > 1:
            abilityimages[game.edit_cur_abils()[1]].blit(abil_init_width + abil_width_dist, top_bar - abil_bot_dist)
            label = pyglet.text.Label(str(game.edit_state()[1].get_cd_2()), font_name='Courier New', font_size=16, bold=True,
                                      x=abil_init_width + abil_width_dist + p_size//2, y=top_bar - abil_bot_dist - sq_size//2,
                                      anchor_x='center', anchor_y='center')
            label.draw()


    @staticmethod
    def draw_message():
        """
        Draws the user-friendly error message.
        :return: None
        """
        if Selections.error != "":
            label = pyglet.text.Label(Selections.error, font_name = 'Courier New', font_size = 11, bold = True,
                                      x = 10*sq_size // 2, y = msg_height, anchor_x = 'center', anchor_y = 'center')
            label.draw()

    @staticmethod
    def draw_exp(cur, max):
        """
        Draws the experience statistics in the HUD.
        :param cur: the current experience of the unit.
        :param max: the maximum experience of the unit.
        :return: None
        """
        label = pyglet.text.Label(str(cur), font_name='Courier New', font_size=18, bold=True,
                                  x = exp_init_width, y=top_bar + exp_init_height - hud_cal, anchor_x='center',
                                  anchor_y='bottom')
        label.draw()
        label = pyglet.text.Label("\\" + str(max), font_name='Courier New', font_size=12, bold=True,
                                  x = exp_init_width, y=top_bar + exp_init_height - hud_cal, anchor_x='center',
                                  anchor_y='top')
        label.draw()

    @staticmethod
    def draw_bar(percent, color, height):
        """
        Draws a (health/morale) bar.
        :param percent: the percentage that the bar is filled to.
        :param color: the color of the bar.
        :param height: the height of the bar.
        :return: None
        """
        height += top_bar - hud_cal
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

    @staticmethod
    def draw_buffs(multiplier, color, offset):
        """
        Draws a (strength/defense) buff indicator.
        :param multiplier: the current buff multiplier.
        :param color: the color of the buff indicator.
        :param offset: the x-offset of the buff.
        :return: None
        """
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
             ("v2i", (offset, buff_height, offset, buff_height + buff_size,
                      offset + buff_size, buff_height + buff_size, offset + buff_size, buff_height)),
             ("c3B", color * 4))
        mult = str("x{:.2f}".format(multiplier))
        label = pyglet.text.Label(mult, font_name='Courier New', font_size=11, bold=True,
                                  x=offset + buff_size*3 // 2, y=buff_height + buff_size // 2, anchor_x='left',
                                  anchor_y='center')
        label.draw()

    @staticmethod
    def draw_passive():
        """
        Draws a "no unit selected" empty HUD.
        :return: None
        """
        off = 3
        width1 = sq_size + off
        width2 = sq_size * 9 - off
        height1 = buff_height + 10 + off
        height2 = name_height + 20 - off
        th = 3
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                 ("v2i", (width1, height1, width1, height2, width2, height2, width2, height1)),
                 ("c3B", (255, 255, 255) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                 ("v2i", (width1 + th, height1 + th, width1 + th, height2 - th,
                          width2 - th, height2 - th, width2 - th, height1 + th)),
                 ("c3B", (127, 127, 127) * 4))
        label = pyglet.text.Label("No unit selected.", font_name='Courier New', font_size=12, bold=True,
                                  x=(width1 + width2) // 2, y=(height1 + height2) // 2, anchor_x='center',
                                  anchor_y='center')
        label.draw()

    @staticmethod
    def draw_side_bar():
        """
        Draws the bar that separates the board from the side display.
        :return: None
        """
        width1 = 10 * sq_size
        height1 = w_height  # w_height - sq_size//2
        height2 = 0  # sq_size//2
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ("v2i", (width1, height1, width1, height2,
                                      width1 + 2, height2, width1 + 2, height1)),
                             ("c3B", (0, 0, 0) * 4))

    @staticmethod
    def draw_side_div(height):
        """
        Draws a side division bar.
        :param height: the height at which the bar will be drawn.
        :return: None
        """
        width1 = 10 * sq_size
        height = w_height - height
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ("v2i", (width1, height, width1, height + 2,
                                      w_length, height + 2, w_length, height)),
                             ("c3B", (0, 0, 0) * 4))

    @staticmethod
    def draw_button(width, height, text, color, w=button_width, h=button_height, secondary=(0, 0, 0), size=11, offset=0):
        """
        Draws a button on the side.
        :param width: the width at which the button will be drawn (this is the left width)
        :param height: the height at which the button will be drawn (this is the lower height)
        :param text: the label for the button
        :param color: the color of the button
        :param w: the horizontal width (length) of the button
        :param h: the vertical width (height) of the button
        :param secondary: the border color of the button
        :param size: the font size of the label
        :param offset: used to calibrate the position of the label within the button
        :return: None
        """
        th = 2
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ("v2i", (width, height, width, height + h, width + w, height + h, width + w, height)),
                             ("c3B", secondary * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                         ("v2i", (width + th, height + th, width + th, height + h - th,
                                  width - th + w, height + h - th, width - th + w, height + th)),
                         ("c3B", color * 4))
        label = pyglet.text.Label(text, font_name='Courier New', font_size=size, bold=True,
                                  x=width + w // 2, y=height + h // 2 - offset,
                                  anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        label.draw()

    @staticmethod
    def draw_hud_button(height, text, color, w=button_width, h=button_height, secondary=(0, 0, 0)):
        """
        Specialized button method for the Draw class.
        :param height: the height at which the button will be drawn (this is the lower height)
        :param text: the label for the button
        :param color: the color of the button
        :param w: the horizontal width (length) of the button
        :param h: the vertical width (height) of the button
        :param secondary: the border color of the button
        :return: None
        """
        Draw.draw_button(label_calib - (w // 2), height, text, color, w, h, secondary)

    @staticmethod
    def draw_name():
        """
        Draws the name of the game. [Legacy code]
        :return: None
        """
        dist_from_top = 35
        label1 = pyglet.text.Label("Chess", font_name='Courier New', font_size=16, bold=True,
                                  x=label_calib, y=w_height - dist_from_top,
                                  anchor_x='center', anchor_y='center', color=side_label_color)
        label2 = pyglet.text.Label("II", font_name='Courier New', font_size=16, bold=True,
                                  x=label_calib, y=w_height - dist_from_top - 20,
                                  anchor_x='center', anchor_y='center', color=side_label_color)
        label1.draw()
        label2.draw()

    @staticmethod
    def draw_move_owner():
        """
        Draws whose turn it is.
        :return: None
        """
        dist_from_top = 115
        if game.get_cur_side() == game.get_white():
            color = (255, 255, 255)
            name = "White"
        else:
            color = (0, 0, 0)
            name = "Black"
        Draw.draw_hud_button(w_height - dist_from_top, "", color, p_size, p_size, (127, 127, 255))
        label1 = pyglet.text.Label(name, font_name='Courier New', font_size=11, bold=True,
                                   x=label_calib, y=w_height - dist_from_top - 10,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label2 = pyglet.text.Label("to move", font_name='Courier New', font_size=11, bold=True,
                                   x=label_calib, y=w_height - dist_from_top - 20,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label1.draw()
        label2.draw()

    @staticmethod
    def draw_turn_number():
        """
        Draws what turn it is.
        :return:
        """
        dist_from_top = 170
        label1 = pyglet.text.Label("Turn", font_name='Courier New', font_size=11, bold=True,
                                   x=label_calib, y=w_height - dist_from_top,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label2 = pyglet.text.Label(str(game.get_num_turns()), font_name='Courier New', font_size=18,
                                   bold=True, x=label_calib, y=w_height - dist_from_top - 22,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label1.draw()
        label2.draw()

    @staticmethod
    def draw_board_flipping():
        dist_from_top = flip_height
        if game.get_flipped():
            color = (127, 255, 127)
        else:
            color = (255, 127, 127)
        Draw.draw_hud_button(w_height - dist_from_top, "", color, p_size, p_size)
        label1 = pyglet.text.Label("Toggle", font_name='Courier New', font_size=10, bold=True,
                                   x=label_calib, y=w_height - dist_from_top - 10,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label2 = pyglet.text.Label("board", font_name='Courier New', font_size=10, bold=True,
                                   x=label_calib, y=w_height - dist_from_top - 22,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label3 = pyglet.text.Label("flipping", font_name='Courier New', font_size=10, bold=True,
                                   x=label_calib, y=w_height - dist_from_top - 34,
                                   anchor_x='center', anchor_y='center', color=side_label_color)
        label1.draw()
        label2.draw()
        label3.draw()

    @staticmethod
    def draw_side_display():
        """
        Draws the sidebar displays (that appear to the right of the board).
        :return: None
        """
        Draw.draw_side_bar()
        Draw.draw_hud_button(w_height - b_heights[4], "Back", (255, 255, 255))
        Draw.draw_hud_button(w_height - b_heights[5], "Help", (255, 255, 191))
        Draw.draw_side_div(80)
        Draw.draw_move_owner()
        Draw.draw_side_div(155)
        Draw.draw_turn_number()
        Draw.draw_side_div(215)
        Draw.draw_hud_button(w_height - b_heights[0], "End Turn", (255, 255, 191))
        Draw.draw_board_flipping()
        Draw.draw_side_div(340)
        Draw.draw_hud_button(w_height - b_heights[1], "Save", (255, 255, 191))
        Draw.draw_hud_button(w_height - b_heights[2], "Load", (255, 255, 191))
        Draw.draw_side_div(415)
        Draw.draw_hud_button(w_height - b_heights[3], "New Game", (255, 255, 191))