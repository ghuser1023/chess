# This file contains the other drawing classes and the pyglet application loop.

from pyglet.window import mouse
from drawing import *

window = pyglet.window.Window(w_length, w_height)
window.set_caption("Chess 2")

thisAlgorithmBecomingSkynetCost = 999999999

@window.event
def on_mouse_press(x, y, button, modifiers):
    """
    Processes a mouse press (Pyglet method)
    :param x: the window pixel x-location
    :param y: the window pixel y-location
    :param button: the mouse button
    :param modifiers: some Pyglet thing???
    :return: None
    """
    if button == mouse.LEFT:
        print(game.edit_state())
        if game.get_cur_screen() == "game":
            Press.press_game(x, y)
        elif game.get_cur_screen() == "title":
            Press.press_title(x, y)
        elif game.get_cur_screen() == "help":
            Press.press_help(x, y)


class Press(object):
    """
    Contains methods to avoid putting all of the mouse press methods in the one Pyglet method.
    """
    @staticmethod
    def press_game(x, y):
        """
        Handles mouse presses for the game screen.
        :param x: the window pixel x-location
        :param y: the window pixel y-location
        :return: None
        """
        if game.edit_state()[0] == "working":
            pass
        elif not Selections.select_button(x, y):
            if game.edit_state()[0] == "select_unit":
                Selections.select_unit(x, y)
            elif game.edit_state()[0] == "unit_selected":
                loc = Utils.loc_to_square(x, y)
                if loc is not None:
                    unit = game.get_board().get_unit(loc[0], loc[1])
                    if unit is None:
                        Selections.select_move(loc)
                    elif unit == game.edit_state()[1]:
                        game.edit_state()[0] = "select_unit"
                        game.edit_state()[1] = None
                        game.edit_cur_abils().clear()
                    elif unit.get_side() == game.edit_state()[1].get_side():
                        Selections.select_unit(x, y)
                    else:
                        Selections.select_attack(loc)
                else:
                    abil = Utils.loc_to_ability(x, y)
                    if abil is not None:
                        if game.edit_state()[1].get_num_input(abil) == 0:
                            Selections.select_ability()
                        else:
                            game.edit_state()[0] = "select_squares"
                            game.edit_state()[2] = game.edit_state()[1].get_num_input(abil)
                            game.edit_state()[4] = abil
            elif game.edit_state()[0] == "select_squares":
                abil = Utils.loc_to_ability(x, y)
                if abil is not None:
                    game.edit_state()[0] = "unit_selected"
                    game.edit_state()[2] = 0
                    game.edit_state()[4] = -1
                    game.edit_state()[3].clear()
                else:
                    loc = Utils.loc_to_square(x, y)
                    if loc is not None:
                        game.edit_state()[3].append(loc)
                    if len(game.edit_state()[3]) == game.edit_state()[2]:
                        Selections.select_ability()

    @staticmethod
    def press_title(x, y):
        """
        Handles mouse presses for the title screen.
        :param x: the window pixel x-location
        :param y: the window pixel y-location
        :return:
        """
        dist = 163
        if (w_length//2 - 2*sq_size) < x < (w_length//2 + 2*sq_size):
            if dist + 2*sq_size > y > dist + sq_size:
                game.set_screen("game")
            elif dist + sq_size > y > dist:
                # praise be our lord and savior, xkcd.com
                global thisAlgorithmBecomingSkynetCost
                thisAlgorithmBecomingSkynetCost = 999999999
                pass  # AI
            elif dist > y > dist - sq_size:
                Depict.cur_help_state = 'basic'
                game.set_screen("help")
        print("no button pressed")
        return None

    @staticmethod
    def press_help(x, y):
        """
        Handles mouse presses for the title screen.
        :param x: the window pixel x-location
        :param y: the window pixel y-location
        :return:
        """
        if w_length - thumb_side_dist < x < w_length - thumb_side_dist + thumb_width:
            if w_height - back_offset - back_height < y < w_height - back_offset:
                if game.get_cur_screen() == 'help' and Depict.cur_help_state != 'basic':
                    Depict.cur_help_state = 'basic'
                else:
                    game.set_screen(game.get_previous_screen())
            for x in range(6):
                if thumb_heights[x] + thumb_height > y > thumb_heights[x]:
                    Depict.cur_help_state = x

class Depict(object):
    """
    Handles graphics for the non-gray screens.
    """
    cur_help_state = 'basic'
    names = ("Pawn", "Fort", "Knight", "Bishop", "King", "Queen")
    types = ('p', 'r', 'n', 'b', 'k', 'q')

    @staticmethod
    def draw_background(color1 = (240, 240, 240), color2 = (220, 220, 220)):
        """
        Draws a checkerboard pattern on the title screen.
        :return: None
        """
        for x in range(0, 13):
            for y in range(0, 12):
                if (x + y) % 2 == 0:
                    color = color1
                else:
                    color = color2
                pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                     ("v2i", (x * sq_size, y * sq_size, (x + 1) * sq_size, y * sq_size,
                              (x + 1) * sq_size, (y + 1) * sq_size, x * sq_size, (y + 1) * sq_size)),
                     ("c3B", color * 4))

    @staticmethod
    def draw_title():
        """
        Draws the title of the game.
        :return: None
        """
        label1 = pyglet.text.Label("Chess II", font_name='Courier New', font_size=32, bold=True,
                                   x=w_length // 2, y=w_height - title_dist,
                                   anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        label2 = pyglet.text.Label('"What if pieces had feelings?"', font_name='Courier New', font_size=16, bold=True,
                                   x=w_length // 2, y=w_height - title_dist - 40,
                                   anchor_x='center', anchor_y='center', color=(0, 0, 255, 255))
        label1.draw()
        label2.draw()

    @staticmethod
    def draw_options():
        """
        Draws the Player v. Player, Player v. AI, and Instructions buttons.
        :return: None
        """
        Draw.draw_button(w_length // 2 - (4*sq_size) // 2, title_button_dist + sq_size, "2 Players", (255, 125, 125),
                         4*sq_size, sq_size - 6, (0, 0, 0), 14)
        Draw.draw_button(w_length // 2 - (4*sq_size) // 2, title_button_dist, "Player vs. AI", (255, 125, 125),
                         4*sq_size, sq_size - 6, (0, 0, 0), 14)
        Draw.draw_button(w_length // 2 - (4*sq_size) // 2, title_button_dist - sq_size, "Instructions", (255, 125, 125),
                         4*sq_size, sq_size - 6, (0, 0, 0), 14)

    @staticmethod
    def draw_back_button():
        """
        Draws the back button.
        :return: None
        """
        width = w_length - thumb_side_dist
        Draw.draw_button(width, w_height - back_offset - back_height, "Back", (255, 255, 255),
                         thumb_width, back_height, (0, 0, 0), 14)

    @staticmethod
    def draw_piece_thumbnails():
        """
        Draws the piece thumbnails as pressable buttons.
        :return: None
        """
        width = w_length - thumb_side_dist
        for x in range(6):
            Draw.draw_button(width, thumb_heights[x], Depict.names[x], (255, 220, 125),
                             thumb_width, thumb_height, (0, 0, 0), 10, 15)
            pieceimages['w' + Depict.types[x] + '1'].blit(width + thumb_width//4, thumb_heights[x] + thumb_height//4 + 10)

    @staticmethod
    def draw_instructions():
        """
        Draws the correct instructions based on the current state.
        :return: None
        """
        if Depict.cur_help_state == 'basic':
            Depict.draw_basic_instructions()
        else:
            Depict.draw_piece_instructions(Depict.cur_help_state)

    @staticmethod
    def draw_basic_instructions():
        """
        Draws the basic changes from normal chess on the screen.
        :return: None
        """
        pass

    @staticmethod
    def draw_piece_instructions(piece):
        """
        Draws the piece instructions for a certain piece.
        :param piece: that piece (a number, corresponding to the traditional order).
        :return: None
        """
        abils = (("arrowstorm", "solidarity"), ("aerial_defense", "fortify"), ("charge", "chivalry"),
                 ("piety", "regeneration"), ("call_to_arms", "rally"), ("subterfuge", "influence"))
        width = w_length - thumb_side_dist
        Draw.draw_button(width, thumb_heights[piece], Depict.names[piece], (125, 220, 255),
                         thumb_width, thumb_height, (0, 0, 0), 10, 15)
        pieceimages['w' + Depict.types[piece] + '1'].blit(width + thumb_width // 4,
                                                          thumb_heights[piece] + thumb_height // 4 + 10)
        label = pyglet.text.Label(Depict.names[piece], font_name='Courier New', font_size=20, bold=True,
                                   x=par_x_offset, y=w_height - help_title_y,
                                   anchor_x='left', anchor_y='center', color=(0, 0, 0, 255))
        label.draw()
        Draw.draw_button(par_x_offset + sq_size - p_size//2 + 2, w_height - help_abil_y - p_size//2 - 1,
                         abils[piece][0][0].upper() + abils[piece][0][1:], (255, 255, 255),
                         col_2_offset - par_x_offset - 2*p_size, p_size, (0, 0, 0), 13)
        abilityimages[abils[piece][0]].blit(par_x_offset, w_height - help_abil_y - 15)
        Draw.draw_button(col_2_offset + sq_size - p_size//2 + 2, w_height - help_abil_y - p_size//2 - 1,
                         abils[piece][1][0].upper() + abils[piece][1][1:], (255, 255, 255),
                         col_2_offset - par_x_offset - 2*p_size, p_size, (0, 0, 0), 13)
        abilityimages[abils[piece][1]].blit(col_2_offset, w_height - help_abil_y - 15)


@window.event
def on_draw():
    """
    Draws the window (Pyglet method).
    :return: None
    """
    window.clear()
    if game.get_cur_screen() == "game":
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ("v2i", (0,0,0,w_height,w_length,w_height,w_length,0)),
                             ("c3B", (127, 127, 127) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ("v2i", (10*sq_size + 2, 0, 10*sq_size + 2, w_height, w_length, w_height, w_length, 0)),
                             ("c3B", (240, 240, 240) * 4))
        Draw.draw_board()
        Draw.draw_pieces()
        Draw.draw_ability_images()
        Draw.draw_message()
        Draw.draw_side_display()
    elif game.get_cur_screen() == "title":
        Depict.draw_background()
        Depict.draw_title()
        Depict.draw_options()
    elif game.get_cur_screen() == "help":
        Depict.draw_background((240, 240, 255), (220, 220, 255))
        Depict.draw_back_button()
        Depict.draw_piece_thumbnails()
        Depict.draw_instructions()


