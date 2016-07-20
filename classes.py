import math

class Unit(object):
    def __init__(self, strength, hp, xp_drop, xp_threshold, moves, value):
        self.base_str = strength
        self.base_hp = hp
        self.buffs = [[],[]]
        self.hp = hp
        self.xp = 0
        self.xp_drop = xp_drop
        self.xp_threshold = xp_threshold
        self.level_multiplier = 1.1
        self.level = 1
        self.moves = moves
        self.board = None
        self.side = None
        self.cooldowns = [0, 0]
        self.value = value

    def set_board(self, board):
        self.board = board

    def get_side(self):
        return self.side

    def get_value(self):
        return self.value

    def set_side(self, side):
        self.side = side

    def level_up(self):
        if self.level < 3:
            self.base_str *= self.level_multiplier
            self.hp *= self.level_multiplier
            self.base_hp *= self.level_multiplier
            self.level += 1
            self.level_multiplier = 1.25 / 1.1

    def effective_strength(self):
        buff = 0
        for x in self.buffs[0]:
            buff *= x[0]
        return self.base_str * buff

    def deal_damage(self, damage):
        buff = 1
        for x in self.buffs[1]:
            buff *= x[0]
            self.hp -= (damage / buff)
        if self.hp < 0:
            self.hp = 0

    def heal_damage(self, health):
        self.hp += health
        if self.hp > self.base_hp:
            self.hp = self.base_hp

    def buff_attack(self, buff, duration):
        self.buffs[0].append((buff, duration))

    def buff_health(self, buff, duration):
        self.buffs[1].append((buff, duration))

    def gain_xp(self, xp):
        self.xp += xp
        if self.xp >= self.xp_threshold:
            self.xp -= self.xp_threshold
            self.levelup()

    def check_move(self, x, y):
        if (x, y) in self.moves:
            return True
        return False

    def tick(self):
        buffs = []
        for buff in self.buffs[0]:
            if buff[1] > 1:
                buffs.append((buff[0], buff[1] - 1))
                self.buffs[0] = buffs
                if self.cooldowns[0] > 0:
                    self.cooldowns -= 1
                if self.cooldowns[1] > 0:
                    self.cooldowns -= 1

    def isDead(self):
        return (self.hp <= 0)


class Side(object):
    def __init__(self, name):
        self.units = []
        self.morale = 100
        self.other = None
        self.name = name

    def add_opponent(self, other):
        self.other = other

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.pop(unit)

    def add_morale(self, morale):
        self.morale += morale
        if self.morale > 100:
            self.morale = 100
        if self.morale < 0:
            self.morale = 0

    def get_obdedience(self, morale):
        if morale >= 50:
            return 1
        else:
            return 0.02 * morale

    def get_num_abilities(self, morale):
        num = 0
        if morale >= 15:
            num += 1
        if morale >= 40:
            num += 1
        if morale >= 80:
            num += 1
        return num

    def __str__(self):
        return self.name


def initialize_board():
    white.other = black
    black.other = white
    board.set_sides(white, black)
    for x in range(8):
        wp = Pawn()
        bp = Pawn()
        wp.set_board(board)
        wp.set_side(white)
        bp.set_board(board)
        bp.set_side(black)
        board.add_unit(wp, x, 1)
        board.add_unit(bp, x, 6)
        white.add_unit(wp)
        black.add_unit(bp)
    row_0 = [Fort(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Fort()]
    row_7 = [Fort(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Fort()]
    column = 0
    for piece in row_0:
        piece.set_board(board)
        piece.set_side(white)
        board.add_unit(piece, column, 0)
        white.add_unit(piece)
        column += 1
    column = 0
    for piece in row_7:
        piece.set_board(board)
        piece.set_side(black)
        board.add_unit(piece, column, 7)
        black.add_unit(piece)
        column += 1


class Pawn(Unit):
    def __init__(self):
        moves = [(0, 1)]
        Unit.__init__(self, 3, 10, 1, 2, moves, 3)

    def arrowstorm(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 2 or yDifference <= 2:
                target.deal_damage(math.ceil(.75 * self.effective_str()))
                self.cooldown[0] = 4


    def deal_damage(self, damage):
        local_unit_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc(self)[1] + j)
                if checked_unit == None or checked_unit.side == self.side:
                    local_unit_list.append(checked_unit)
        buff = len(local_unit_list) * 0.3 + 1
        Unit.deal_damage(self, damage / buff)

    def effective_strength(self):
        local_unit_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                checked_unit = self.board.get_unit(self.board.get_loc(self)[0] + i, self.board.get_loc[1] + j)
                if checked_unit.side == self.side:
                    local_unit_list.append(checked_unit)
        buff = len(local_unit_list) * 0.3 + 1
        return (buff * self.base_str)

    def abilities(self):
        return ["arrowstorm"]

    def __str__(self):
        return 'p'+ str(self.level)


class Fort(Unit):
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            moves.append((0, i))
            moves.append((i, 0))
        Unit.__init__(self, 7, 75, 3, 3, moves, 10)

    def aerial_defense(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 2 or yDifference <= 2:
                target.deal_damage(math.ceil(.75 * self.effective_str()))
                self.cooldown[0] = 4

    def abilities(self):
        return ["aerial_defense"]

    def __str__(self):
        return 'r'+ str(self.level)


class Knight(Unit):
    def __init__(self):
        moves = [(-1, -2), (-1, 2), (-2, -1), (-2, 1), (1, -2), (1, 2), (2, -1), (2, 1)]
        Unit.__init__(self, 10, 50, 5, 4, moves, 10)
        self.chivalrous = (False, 0)

    def charge(self, moveLoc):
        if self.cooldown[0] == 0:
            self.buff_attack(1.25, 1)
            self.board.move_unit(moveLoc[0], moveLoc[1])
            self.cooldown[0] = 10

    def chivalry(self):
        if self.cooldown[1] == 0:
            self.buff_health(1.2, 2)
            self.chivalrous = (True, 2)
            self.cooldown[1] = 10

    def abilities(self):
        return ["charge", "chivalry"]

    def __str__(self):
        return 'n'+ str(self.level)


class Bishop(Unit):
    def __init__(self):
        moves = []
        for i in range(-8, 9):
            moves.append((i, i))
        Unit.__init__(self, 5, 20, 4, 3, moves, 15)

    def regeneration(self, target):
        if self.cooldown[0] == 0:
            target.heal_damage(1000)
            self.cooldown[0] = 16

    def piety(self):
        if self.cooldown[1] == 0:
            local_unit_list = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    checked_unit = self.board.get_unit(self.board.get_loc(aelf)[0] + i, self.board.get_loc[1] + j)
                    if checked_unit.side == self.side:
                        local_unit_list.append(checked_unit)
            for unit in local_unit_list:
                unit.boost_health(1.2, 3)
                unit.boost_attack(1.1, 3)
            self.cooldown[1] = 12

    def abilities(self):
        return ["regeneration", "piety"]

    def __str__(self):
        return 'b'+ str(self.level)


class King(Unit):
    def __init__(self):
        self.rally_amt = 30
        moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        Unit.__init__(self, 7, 40, 0, 3, moves, 100)

    def call_to_arms(self, x1, y1, x2, y2):
        if self.cooldown[0] == 0:
            mercenary1 = Pawn()
            mercenary2 = Pawn()
            self.board.add_unit(mercenary1, x1, y1)
            self.board.add_unit(mercenary2, x2, y2)
            self.side.add_unit(mercenary1)
            self.side.add_unit(mercenary2)
            self.cooldown[0] = 20

    def rally(self):
        if self.cooldown[1] == 0:
            self.side.add_morale(self.rally_amt)
            self.rally_amt = (self.rally_amt + 1) // 2
            self.cooldown = 12

    def abilities(self):
        return ["call_to_arms", "rally"]

    def __str__(self):
        return 'k'+ str(self.level)


class Queen(Unit):
    def __init__(self):
        self.influence_active = False
        moves = []
        for i in range(-8, 9):
            for j in range(-8, 9):
                moves.append((i, j))
        Unit.__init__(self, 7, 35, 0, 3, moves, 25)

    def subterfuge(self, target):
        if self.cooldown[0] == 0:
            xDifference = abs(self.board.get_loc(self)[0] - target.board.get_loc(self)[0])
            yDifference = abs(self.board.get_loc(self)[1] - target.board.get_loc(self)[1])
            if xDifference <= 5 or yDifference <= 5:
                target.buff_attack(.75, 3)
                target.deal_damage(math.ceil(.8 * self.effective_strength()))
                self.cooldown[0] = 16
    
    def influence(self):
        if self.cooldown[1] == 0:
            self.influence_active = True
            self.cooldown[0] = 26

    def abilities(self):
        return ["subterfuge", "influence"]

    def __str__(self):
        return 'q' + str(self.level)


class Board(object):
    def __init__(self):
        self.board = []
        self.units = {}
        self.side1 = None
        self.side2 = None
        self.error = ""
        for x in range(8):
            row = []
            for y in range(8):
                row.append(None)
            self.board.append(row)

    def set_sides(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def add_unit(self, unit, x, y):
        self.board[x][y] = unit
        self.units[unit] = (x, y)

    def get_unit(self, x, y):
        return self.board[x][y]

    def get_loc(self, unit):
        return self.units[unit]

    def remove_unit(self, unit, x, y):
        self.board[x][y] = None
        self.units.pop(unit)

    def move_unit(self, unit, x, y):
        loc = self.units[unit]
        if self.valid(loc[0] + x, loc[1] + y) and unit.check_move(x, y):
            if self.board[loc[0] + x][loc[1] + y] == None:
                self.board[loc[0] + x][loc[1] + y] = unit
                self.board[loc[0]][loc[1]] = None
                self.units[unit] = (loc[0] + x, loc[1] + y)
            else:
                square = self.closest_square(loc[0], loc[1], loc[0] + x, loc[1] + y)
                self.move_unit(unit, square[0], square[1])
                self.attack_unit(unit, self.board[loc[0] + x][loc[1] + y])
        else:
            self.error = "That move is invalid."

    def valid(self, x, y):
        if (x >= 0) and (x <= 7) and (y >= 0) and (y <= 7):
            return True
        return False

    def closest_square(self, a, b, x, y):
        squares = []
        for m in range(3):
            for n in range(3):
                squares.append((x + m - 1, y + m - 1))
        squares.remove((x, y))
        for square in squares:
            if not self.valid(square[0], square[1]):
                squares.remove(square)
            if self.board[square[0]][square[1]] != None:
                squares.remove(square)
        piece = None
        min = 100
        for square in squares:
            dist = (square[0] - a) * (square[0] - a) + (square[1] - b) * (square[1] - b)
            if dist < min:
                min = dist
                piece = square
        if min == 100:
            return None
        else:
            return piece

    def attack_unit(self, attacker, defender):
        defender.deal_damage(attacker.effective_strength())

    def end_turn(self):
        for x in self.units.keys():
            if x.isDead():
                x.side.add_morale(-1 * x.get_value())
                x.side.other.add_morale(0.5 * x.get_value())
                x.side.remove_unit(x)
                self.remove_unit(x)
            else:
                x.tick()

    def get_pieces(self):
        return list(self.units.keys())


board = Board()
white = Side("w")
black = Side("b")
initialize_board()
