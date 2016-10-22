# Contains the specific piece classes.

from pieces import *
import math

file = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

class Pawn(Unit):
    """
    Represents a pawn. Weak, but useful on the front line.
    """
    def __init__(self):
        moves = [(0, 1)]
        Unit.__init__(self, 3, 10, 1, 2, moves, 3, "Pawn", ["arrowstorm"], [self.arrowstorm], True)

    @staticmethod
    def get_key_stats():
        """
        Returns the key stats of the unit for display in the help screens.
        :return: a tuple containing strength, hp, xp drops, and level up xp.
        """
        return 3, 10, 1, 2

    def get_num_input(self, abil):
        """
        :param abil: the number of the ability
        :return: the number of inputs necessary
        """
        return 1

    def arrowstorm(self, squares):
        """
        An ability that deals ranged damage to another unit.
        :param squares: should contain all the data necessary for the following parameters:
            target: the enemy unit to be targeted by this ability.
        :return: the relevant error message.
        """
        target = self.board.get_unit(squares[0][0], squares[0][1])
        if self.cooldown[0] == 0:
            if not self.side == target.get_side():
                if target is not None:
                    xDifference = abs(self.board.get_loc(self)[0] - self.board.get_loc(target)[0])
                    yDifference = abs(self.board.get_loc(self)[1] - self.board.get_loc(target)[1])
                    if xDifference <= 2 and yDifference <= 2:
                        target.deal_damage(math.ceil(.75 * self.effective_strength()))
                        self.cooldown[0] = 4
                        (a, b) = self.board.get_loc(self)
                        return self.name + " on " + file[a]+str(b+1) + " casted arrowstorm."
                    else:
                        return "Target not in range."
                else:
                    return "Target does not exist."
            else:
                return "No friendly fire."
        else:
            return "Ability not sufficiently cooled down."

    def str_buff(self):
        """
        Overrides Unit's str_buff to match the Pawn's solidarity ability.
        :return: the buff given to this unit's strength.
        """
        num_local = -1
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc(self)[1] + j)
                if checked_unit is not None and checked_unit.side == self.side and type(checked_unit) == type(self):
                    num_local += 1
        buff = num_local * 0.2 + 1
        buff *= Unit.str_buff(self)
        return buff

    def def_buff(self):
        """
        Overrides Unit's def_buff to match the Pawn's solidarity ability.
        :return: the buff given to this unit's defense.
        """
        num_local = -1
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc(self)[1] + j)
                if checked_unit is not None and checked_unit.side == self.side and type(checked_unit) == type(self):
                    num_local += 1
        buff = num_local * 0.2 + 1
        buff *= Unit.def_buff(self)
        return buff


class Fort(Unit):
    """
    Represents a Fort. Useful defensively, but limited offensive capabilities.
    """
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            moves.append((0, i))
            moves.append((i, 0))
        Unit.__init__(self, 7, 75, 3, 3, moves, 10, "Fort", ["aerial_defense"], [self.aerial_defense], False)

    @staticmethod
    def get_key_stats():
        """
        Returns the key stats of the unit for display in the help screens.
        :return: a tuple containing strength, hp, xp drops, and level up xp.
        """
        return 7, 75, 3, 3

    def get_num_input(self, abil):
        """
        :param abil: the number of the ability
        :return: the number of inputs necessary
        """
        return 1

    def aerial_defense(self, squares):
        """
        Works exactly the same way as the Pawn's arrowstorm ability.
        :param squares: should contain all the data necessary for the following parameters:
            target: the target to be fired upon.
        :return: the relevant error message.
        """
        target = self.board.get_unit(squares[0][0], squares[0][1])
        if self.cooldown[0] == 0:
            if not self.side == target.get_side():
                if target is not None:
                    xDifference = abs(self.board.get_loc(self)[0] - self.board.get_loc(target)[0])
                    yDifference = abs(self.board.get_loc(self)[1] - self.board.get_loc(target)[1])
                    if xDifference <= 2 and yDifference <= 2:
                        target.deal_damage(math.ceil(.75 * self.effective_strength()))
                        self.cooldown[0] = 4
                        (a, b) = self.board.get_loc(self)
                        return self.name + " on " + file[a] + str(b + 1) + " casted aerial defense."
                    else:
                        return "Target not in range."
                else:
                    return "Target does not exist."
            else:
                return "No friendly fire."
        else:
            return "Ability not sufficiently cooled down."


class Knight(Unit):
    """
    Represents a knight. Offensive unit with some potential for mobility.
    """
    def __init__(self):
        moves = [(-1, -2), (-1, 2), (-2, -1), (-2, 1), (1, -2), (1, 2), (2, -1), (2, 1)]
        Unit.__init__(self, 10, 50, 5, 4, moves, 10, "Knight", ["charge", "chivalry"], [self.charge, self.chivalry], True)

    @staticmethod
    def get_key_stats():
        """
        Returns the key stats of the unit for display in the help screens.
        :return: a tuple containing strength, hp, xp drops, and level up xp.
        """
        return 10, 50, 5, 4

    def get_num_input(self, abil):
        """
        :param abil: the number of the ability
        :return: the number of inputs necessary
        """
        if abil == 0:
            return 1
        else:
            return 1

    def charge(self, squares):
        """
        Buffs the knight's attack for one turn, then moves the knight to the chosen square.
        This move does not count as a turn action; therefore the knight can then be used to attack or move again;
        alternatively, another unit may be moved.
        :param squares: should contain all the data necessary for the following parameters:
            the place where the knight is to be moved initially.
        :return: the relevant error message.
        """
        moveLoc = squares[0]
        pos = self.board.get_loc(self)
        delta = self.board.qualify_move(self, (moveLoc[0] - pos[0], moveLoc[1] - pos[1]))
        if self.cooldown[0] == 0:
            if self.check_move(delta[0], delta[1]):
                if self.board.get_unit(moveLoc[0], moveLoc[1]) is None:
                    self.buff_attack(2, 1)
                    self.board.move_unit(self, moveLoc[0] - pos[0], moveLoc[1] - pos[1])
                    self.cooldown[0] = 10
                    (a, b) = self.board.get_loc(self)
                    return self.name + " on " + file[a] + str(b + 1) + " casted charge."
                else:
                    return "Cannot move into another unit."
            else:
                return "That move is invalid."
        else:
            return "Ability not sufficiently cooled down."

    def chivalry(self, squares):
        """
        Buffs the knight's defense, then allows it to take a hit for a friendly unit.
        Note: this is not implemented (must alter deal_damage in the Piece class)
        :param squares: should contain all the data necessary for the following parameters:
            target: the target that should be protected.
        :return: the relevant error message.
        """
        target = self.board.get_unit(squares[0][0], squares[0][1])
        if self.cooldown[1] == 0:
            if self.side == target.get_side():
                if target is not None:
                    xDifference = abs(self.board.get_loc(self)[0] - self.board.get_loc(target)[0])
                    yDifference = abs(self.board.get_loc(self)[1] - self.board.get_loc(target)[1])
                    if xDifference <= 2 and yDifference <= 2 and xDifference != 0 and yDifference != 0:
                        target.add_protected(self)
                        self.buff_health(1.5, 2)
                        self.cooldown[1] = 10
                        (a, b) = self.board.get_loc(self)
                        return self.name + " on " + file[a] + str(b + 1) + " casted chivalry."
                    else:
                        return "Target not in range."
                else:
                    return "Target does not exist."
            else:
                return "Cannot protect enemy unit."
        else:
            return "Ability not sufficiently cooled down."


class Bishop(Unit):
    """
    Represents a bishop. Support unit for the army.
    """
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            moves.append((i, i))
            moves.append((-i, i))
        Unit.__init__(self, 5, 20, 4, 3, moves, 15, "Bishop", ["regeneration", "piety"], [self.regeneration, self.piety], False)

    @staticmethod
    def get_key_stats():
        """
        Returns the key stats of the unit for display in the help screens.
        :return: a tuple containing strength, hp, xp drops, and level up xp.
        """
        return 5, 20, 4, 3

    def get_num_input(self, abil):
        """
        :param abil: the number of the ability
        :return: the number of inputs necessary
        """
        if abil == 0:
            return 1
        else:
            return 0

    def regeneration(self, squares):
        """
        Heals a friendly target.
        :param squares: should contain all the data necessary for the following parameters:
            target: the unit to be healed.
        :return: the relevant error message.
        """
        target = self.board.get_unit(squares[0][0], squares[0][1])
        if self.cooldown[0] == 0:
            if self.side == target.get_side():
                if target is not None:
                    target.heal_damage(1000)
                    self.cooldown[0] = 16
                    (a, b) = self.board.get_loc(self)
                    return self.name + " on " + file[a] + str(b + 1) + " casted regeneration."
                else:
                    return "Target does not exist."
            else:
                return "Cannot heal enemy unit."
        else:
            return "Ability not sufficiently cooled down."

    def piety(self, squares):
        """
        Passively buffs the health of every unit in a short radius.
        :param squares: should contain all the data necessary for the following parameters: [None]
        :return: the relevant error message.
        """
        squares.clear()
        if self.cooldown[1] == 0:
            local_unit_list = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc(self)[1] + j)
                    if checked_unit is not None and checked_unit.side == self.side:
                        local_unit_list.append(checked_unit)
            for unit in local_unit_list:
                unit.buff_health(1.2, 3)
                unit.buff_attack(1.1, 3)
            self.cooldown[1] = 12
            (a, b) = self.board.get_loc(self)
            return self.name + " on " + file[a] + str(b + 1) + " casted piety."
        else:
            return "Ability not sufficiently cooled down."


class King(Unit):
    """
    Represents a king. Flagship piece of the army, weak physically but important emotionally.
    """
    def __init__(self):
        self.rally_amt = 30
        moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        Unit.__init__(self, 7, 40, 10, 3, moves, 100, "King", ["call_to_arms", "rally"], [self.call_to_arms, self.rally], True)

    @staticmethod
    def get_key_stats():
        """
        Returns the key stats of the unit for display in the help screens.
        :return: a tuple containing strength, hp, xp drops, and level up xp.
        """
        return 7, 40, 10, 3

    def get_num_input(self, abil):
        """
        :param abil: the number of the ability
        :return: the number of inputs necessary
        """
        if abil == 0:
            return 2
        else:
            return 0

    def call_to_arms(self, squares):
        """
        Adds two mercenary pawns to the board.
        :param squares: should contain all the data necessary for the following parameters:
            x1: the x-location of the first pawn.
            y1: the y-location of the first pawn.
            x2: the x-location of the second pawn.
            y2: the y-location of the second pawn.
        :return: the relevant error message.
        """
        (x1, y1) = squares[0]
        (x2, y2) = squares[1]
        if self.cooldown[0] == 0:
            if self.board.get_unit(x1, y1) is None and self.board.get_unit(x2, y2) is None:
                mercenary1 = Pawn()
                mercenary2 = Pawn()
                mercenary1.set_board(self.board)
                mercenary1.set_side(self.side)
                mercenary2.set_board(self.board)
                mercenary2.set_side(self.side)
                self.board.add_unit(mercenary1, x1, y1)
                self.board.add_unit(mercenary2, x2, y2)
                self.side.add_unit(mercenary1)
                self.side.add_unit(mercenary2)
                self.cooldown[0] = 20
                (a, b) = self.board.get_loc(self)
                return self.name + " on " + file[a] + str(b + 1) + " casted call to arms."
            else:
                return "Cannot spawn mercenaries on top of units."
        else:
            return "Ability not sufficiently cooled down."


    def rally(self, squares):
        """
        Increases the morale of this unit's side for a few turns.
        :param squares: should contain all the data necessary for the following parameters: [None]
        :return: the relevant error message.
        """
        squares.clear()
        if self.cooldown[1] == 0:
            self.side.rally()
            self.cooldown[1] = 20
            (a, b) = self.board.get_loc(self)
            return self.name + " on " + file[a] + str(b + 1) + " casted rally."
        else:
            return "Ability not sufficiently cooled down."


class Queen(Unit):
    """
    Represents a queen. Capable of covert operations and significant mobility.
    """
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            for j in range(-8, 9):
                moves.append((i, j))
        Unit.__init__(self, 7, 35, 5, 3, moves, 25, "Queen", ["subterfuge", "influence"], [self.subterfuge, self.influence], False)

    @staticmethod
    def get_key_stats():
        """
        Returns the key stats of the unit for display in the help screens.
        :return: a tuple containing strength, hp, xp drops, and level up xp.
        """
        return 7, 35, 5, 3

    def get_num_input(self, abil):
        """
        :param abil: the number of the ability
        :return: the number of inputs necessary
        """
        if abil == 0:
            return 1
        else:
            return 0

    def subterfuge(self, squares):
        """
        Debuffs and deals damage to target unit.
        :param squares: should contain all the data necessary for the following parameters:
            target: the targeted unit.
        :return: the relevant error message.
        """
        target = self.board.get_unit(squares[0][0], squares[0][1])
        if self.cooldown[0] == 0:
            if not self.side == target.get_side():
                if target is not None:
                    xDifference = abs(self.board.get_loc(self)[0] - self.board.get_loc(target)[0])
                    yDifference = abs(self.board.get_loc(self)[1] - self.board.get_loc(target)[1])
                    if xDifference <= 5 and yDifference <= 5:
                        target.buff_attack(.5, 3)
                        target.deal_damage(math.ceil(.5 * self.effective_strength()))
                        self.cooldown[0] = 16
                        (a, b) = self.board.get_loc(self)
                        return self.name + " on " + file[a] + str(b + 1) + " casted subterfuge."
                    else:
                        return "Target not in range."
                else:
                    return "Target does not exist."
            else:
                return "No friendly fire."
        else:
            return "Ability not sufficiently cooled down."

    def influence(self, squares):
        """
        Suppresses mutiny on the board for 1 turn.
        Note: this is not implemented (fix needed in Board class)
        :param squares: should contain all the data necessary for the following parameters: [None]
        :return: the relevant error message.
        """
        squares.clear()
        if self.cooldown[1] == 0:
            self.side.influence()
            self.cooldown[1] = 26
            (a, b) = self.board.get_loc(self)
            return self.name + " on " + file[a] + str(b + 1) + " casted influence."
        else:
            return "Ability not sufficiently cooled down."

Unit.add_fort(Fort)
unit_dict = {"Pawn":Pawn, "Fort":Fort, "Knight":Knight, "Bishop":Bishop, "King":King, "Queen":Queen}