# This file contains the other drawing classes and the pyglet application loop.

from pyglet.window import mouse
from drawing import *

window = pyglet.window.Window(w_length, w_height)
window.set_caption("Chess 2")

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
                pass  # AI
            elif dist > y > dist - sq_size:
                pass  # Help
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


class Depict(object):
    """
    Handles graphics for the non-gray screens.
    """
    @staticmethod
    def draw_background():
        """
        Draws a checkerboard pattern on the title screen.
        :return: None
        """
        for x in range(0, 13):
            for y in range(0, 12):
                if (x + y) % 2 == 0:
                    color = (240, 240, 240)
                else:
                    color = (220, 220, 220)
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
        dist_from_top = 100
        label1 = pyglet.text.Label("Chess II", font_name='Courier New', font_size=32, bold=True,
                                   x=w_length // 2, y=w_height - dist_from_top,
                                   anchor_x='center', anchor_y='center', color=(0, 0, 0, 255))
        label2 = pyglet.text.Label('"What if pieces had feelings?"', font_name='Courier New', font_size=16, bold=True,
                                   x=w_length // 2, y=w_height - dist_from_top - 40,
                                   anchor_x='center', anchor_y='center', color=(0, 0, 255, 255))
        label1.draw()
        label2.draw()

    @staticmethod
    def draw_options():
        """
        Draws the Player v. Player, Player v. AI, and Instructions buttons.
        :return: None
        """
        dist = 163
        Draw.draw_button(w_length // 2 - (4*sq_size) // 2, dist + sq_size, "2 Players", (255, 125, 125),
                         4*sq_size, sq_size - 6, (0, 0, 0), 14)
        Draw.draw_button(w_length // 2 - (4*sq_size) // 2, dist, "Player vs. AI", (255, 125, 125),
                         4*sq_size, sq_size - 6, (0, 0, 0), 14)
        Draw.draw_button(w_length // 2 - (4*sq_size) // 2, dist - sq_size, "Instructions", (255, 125, 125),
                         4*sq_size, sq_size - 6, (0, 0, 0), 14)

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
        pass

