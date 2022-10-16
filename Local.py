import copy
import sys
from random import shuffle


# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    def __init__(self, piece_type, x, y, max_x, max_y, grid, points):
        self.piece_type = piece_type
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.grid = grid
        self.points = points

    def __repr__(self):
        return "{piece_type} : [{x}, {y}]".format(piece_type=self.piece_type, x=self.x, y=self.y)

    def __lt__(self, other):
        return self.points > other.points

    def get_coord(self):
        return chr(self.x + 97), self.y

    def get_coord_swapped(self):
        return chr(self.y + 97), self.x

    def get_numeric_coord(self):
        return self.y, self.x

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def get_grid(self):
        return self.grid

    def get_piece_type(self):
        return self.piece_type

    def get_points(self):
        return self.points


class King(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('King', x, y, max_x, max_y, grid, 2)

    def get_actions(self):
        ls = []
        right = (self.get_y(), self.get_x() + 1)
        ls.append(right)
        diag_right_up = (self.get_y() + 1, self.get_x() + 1)
        ls.append(diag_right_up)

        left = (self.get_y(), self.get_x() - 1)
        ls.append(left)
        diag_left_up = (self.get_y() + 1, self.get_x() - 1)
        ls.append(diag_left_up)

        down = (self.get_y() - 1, self.get_x())
        ls.append(down)
        diag_left_down = (self.get_y() - 1, self.get_x() - 1)
        ls.append(diag_left_down)

        up = (self.get_y() + 1, self.get_x())
        ls.append(up)
        diag_right_down = (self.get_y() - 1, self.get_x() + 1)
        ls.append(diag_right_down)

        pieces = ls.copy()
        for piece in ls:
            # assume a is start
            if piece[1] >= self.get_max_x() or piece[1] < 0 or piece[0] < 0 or piece[0] >= self.get_max_y():
                pieces.remove(piece)

        # remove pieces in obstacles
        copy_pieces = pieces.copy()
        for piece in copy_pieces:
            obstacle = self.grid[piece[0]][piece[1]]
            is_obstacle = obstacle == -1
            if is_obstacle:
                pieces.remove(piece)

        return pieces


class Rook(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('Rook', x, y, max_x, max_y, grid, 5)

    def get_actions(self):
        ls = []

        for i in range(self.get_x() - 1, -1, -1):
            if self.grid[self.get_y()][i] == -1:
                break
            piece = (self.get_y(), i)
            ls.append(piece)

        for i in range(self.get_x() + 1, self.get_max_x()):
            if self.grid[self.get_y()][i] == -1:
                break
            piece = (self.get_y(), i)
            ls.append(piece)

        for i in range(self.get_y() - 1, -1, -1):
            if self.grid[i][self.get_x()] == - 1:
                break
            piece = (i, self.get_x())
            ls.append(piece)

        for i in range(self.get_y() + 1, self.get_max_y()):
            if self.grid[i][self.get_x()] == - 1:
                break
            piece = (i, self.get_x())
            ls.append(piece)

        return ls


class Bishop(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('Bishop', x, y, max_x, max_y, grid, 4)

    def get_actions(self):
        ls = []

        counter_2 = 0
        for i in range(self.x - 1, - 1, -1):
            counter_2 -= 1
            if len(self.grid) > self.y + counter_2:
                if self.y + counter_2 < 0 or self.grid[self.y + counter_2][i] == - 1:
                    break
                piece = (self.get_y() + counter_2, i)
                ls.append(piece)

        counter_1 = 0
        for i in range(self.x + 1, self.get_max_x()):
            counter_1 += 1
            if len(self.grid) > self.y + counter_1:
                if self.grid[self.y + counter_1][i] == - 1:
                    break
                piece = (self.get_y() + counter_1, i)
                ls.append(piece)

        counter_3 = 0
        for i in range(self.y - 1, - 1, -1):
            counter_3 += 1
            if len(self.grid[0]) > self.x + counter_3:
                if self.grid[i][self.x + counter_3] == -1:
                    break
                piece = (i, self.get_x() + counter_3)
                ls.append(piece)

        counter_4 = 0
        for i in range(self.y + 1, self.get_max_y()):
            counter_4 += 1
            if self.x - counter_4 >= 0:
                if self.grid[i][self.x - counter_4] == -1:
                    break
                piece = (i, self.x - counter_4)
                ls.append(piece)

        return ls


class Queen(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__("Queen", x, y, max_x, max_y, grid, 8)
        self.grid = grid

    def get_actions(self):
        ls = []

        # rook like movement
        for i in range(self.get_x() - 1, -1, -1):
            if self.grid[self.get_y()][i] == -1:
                break
            piece = (self.get_y(), i)
            ls.append(piece)

        for i in range(self.get_x() + 1, self.get_max_x()):
            if self.grid[self.get_y()][i] == -1:
                break
            piece = (self.get_y(), i)
            ls.append(piece)

        for i in range(self.get_y() - 1, -1, -1):
            if self.grid[i][self.get_x()] == - 1:
                break
            piece = (i, self.get_x())
            ls.append(piece)

        for i in range(self.get_y() + 1, self.get_max_y()):
            if self.grid[i][self.get_x()] == - 1:
                break
            piece = (i, self.get_x())
            ls.append(piece)

        # bishop like movement
        counter_2 = 0
        for i in range(self.x - 1, - 1, -1):
            counter_2 -= 1
            if len(self.grid) > self.y + counter_2:
                if self.y + counter_2 < 0 or self.grid[self.y + counter_2][i] == - 1:
                    break
                piece = (self.get_y() + counter_2, i)
                ls.append(piece)

        counter_1 = 0
        for i in range(self.x + 1, self.get_max_x()):
            counter_1 += 1
            if len(self.grid) > self.y + counter_1:
                if self.grid[self.y + counter_1][i] == - 1:
                    break
                piece = (self.get_y() + counter_1, i)
                ls.append(piece)

        counter_3 = 0
        for i in range(self.y - 1, - 1, -1):
            counter_3 += 1
            if len(self.grid[0]) > self.x + counter_3:
                if self.grid[i][self.x + counter_3] == -1:
                    break
                piece = (i, self.get_x() + counter_3)
                ls.append(piece)

        counter_4 = 0
        for i in range(self.y + 1, self.get_max_y()):
            counter_4 += 1
            if self.x - counter_4 >= 0:
                if self.grid[i][self.x - counter_4] == -1:
                    break
                piece = (i, self.x - counter_4)
                ls.append(piece)

        return ls


class Knight(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('Knight', x, y, max_x, max_y, grid, 3)

    def get_actions(self):
        ls = []

        top_left = (self.get_y() + 2, self.get_x() - 1)
        ls.append(top_left)
        top_right = (self.get_y() + 2, self.get_x() + 1)
        ls.append(top_right)

        bottom_left = (self.get_y() - 2, self.get_x() - 1)
        ls.append(bottom_left)
        bottom_right = (self.get_y() - 2, self.get_x() + 1)
        ls.append(bottom_right)

        left_top = (self.get_y() + 1, self.get_x() - 2)
        ls.append(left_top)

        left_bottom = (self.get_y() - 1, self.get_x() - 2)
        ls.append(left_bottom)

        right_top = (self.get_y() + 1, self.get_x() + 2)
        ls.append(right_top)

        right_bottom = (self.get_y() - 1, self.get_x() + 2)
        ls.append(right_bottom)

        pieces = ls.copy()
        for piece in ls:
            # assume a is start
            if piece[1] >= self.max_x or piece[1] < 0 or piece[0] < 0 or piece[0] >= self.max_y:
                pieces.remove(piece)

        # remove pieces in obstacles
        copy_pieces = pieces.copy()
        for piece in copy_pieces:
            obstacle = self.grid[piece[0]][piece[1]]
            is_obstacle = obstacle == -1
            if is_obstacle:
                pieces.remove(piece)

        return pieces


class Ferz(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('Ferz', x, y, max_x, max_y, grid, 1)

    def get_actions(self):
        ls = []
        if self.get_y() + 1 < self.get_max_y():
            if self.get_x() - 1 >= 0:
                diag_left_up = (self.get_y() + 1, self.get_x() - 1)
                ls.append(diag_left_up)
            if self.get_x() + 1 < self.get_max_x():
                diag_right_up = (self.get_y() + 1, self.get_x() + 1)
                ls.append(diag_right_up)

        if self.get_y() - 1 >= 0:
            if self.get_x() - 1 >= 0:
                diag_left_down = (self.get_y() - 1, self.get_x() - 1)
                ls.append(diag_left_down)
            if self.get_x() + 1 < self.get_max_x():
                diag_right_down = (self.get_y() - 1, self.get_x() + 1)
                ls.append(diag_right_down)

        pieces = ls.copy()
        for piece in ls:
            # assume a is start
            if piece[1] >= self.max_x or piece[1] < 0 or piece[0] < 0 or piece[0] >= self.max_y:
                pieces.remove(piece)

        # remove pieces in obstacles
        copy_pieces = pieces.copy()
        for piece in copy_pieces:
            obstacle = self.grid[piece[0]][piece[0]]
            is_obstacle = obstacle == -1
            if is_obstacle:
                pieces.remove(piece)

        return pieces


class Princess(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('Princess', x, y, max_x, max_y, grid, 6)

    def get_actions(self):
        ls = []
        # Bishop like movement
        counter_2 = 0
        for i in range(self.x - 1, - 1, -1):
            counter_2 -= 1
            if len(self.grid) > self.y + counter_2:
                if self.grid[self.y + counter_2][i] == - 1:
                    break
                piece = (self.get_y() + counter_2, i)
                ls.append(piece)

        counter_1 = 0
        for i in range(self.x + 1, self.get_max_x()):
            counter_1 += 1
            if len(self.grid) > self.y + counter_1:
                if self.grid[self.y + counter_1][i] == - 1:
                    break
                piece = (self.get_y() + counter_1, i)
                ls.append(piece)

        counter_3 = 0
        for i in range(self.y - 1, - 1, -1):
            counter_3 += 1
            if len(self.grid[0]) > self.x + counter_3:
                if self.grid[i][self.x + counter_3] == -1:
                    break
                piece = (i, self.get_x() + counter_3)
                ls.append(piece)

        counter_4 = 0
        for i in range(self.y + 1, self.get_max_y()):
            counter_4 += 1
            if self.x - counter_4 >= 0:
                if self.grid[i][self.x - counter_4] == -1:
                    break
                piece = (i, self.x - counter_4)
                ls.append(piece)

        # Knight-like movements
        top_left = (self.get_y() + 2, self.get_x() - 1)
        ls.append(top_left)
        top_right = (self.get_y() + 2, self.get_x() + 1)
        ls.append(top_right)

        bottom_left = (self.get_y() - 2, self.get_x() - 1)
        ls.append(bottom_left)
        bottom_right = (self.get_y() - 2, self.get_x() + 1)
        ls.append(bottom_right)

        left_top = (self.get_y() + 1, self.get_x() - 2)
        ls.append(left_top)

        left_bottom = (self.get_y() - 1, self.get_x() - 2)
        ls.append(left_bottom)

        right_top = (self.get_y() + 1, self.get_x() + 2)
        ls.append(right_top)

        right_bottom = (self.get_y() - 1, self.get_x() + 2)
        ls.append(right_bottom)

        pieces = ls.copy()
        for piece in ls:
            # assume a is start
            if piece[1] >= self.max_x or piece[1] < 0 or piece[0] < 0 or piece[0] >= self.max_y:
                pieces.remove(piece)

        # remove pieces in obstacles
        copy_pieces = pieces.copy()
        for piece in copy_pieces:
            obstacle = self.grid[piece[0]][piece[1]]
            is_obstacle = obstacle == -1
            if is_obstacle:
                pieces.remove(piece)

        return pieces


class Empress(Piece):
    def __init__(self, x, y, max_x, max_y, grid):
        super().__init__('Empress', x, y, max_x, max_y, grid, 7)

    def get_actions(self):
        ls = []
        # rook like movement
        for i in range(self.get_x() - 1, -1, -1):
            if self.grid[self.get_y()][i] == -1:
                break
            piece = (self.get_y(), i)
            ls.append(piece)

        for i in range(self.get_x() + 1, self.get_max_x()):
            if self.grid[self.get_y()][i] == -1:
                break
            piece = (self.get_y(), i)
            ls.append(piece)

        for i in range(self.get_y() - 1, -1, -1):
            if self.grid[i][self.get_x()] == - 1:
                break
            piece = (i, self.get_x())
            ls.append(piece)

        for i in range(self.get_y() + 1, self.get_max_y()):
            if self.grid[i][self.get_x()] == - 1:
                break
            piece = (i, self.get_x())
            ls.append(piece)

        # Knight like movement
        top_left = (self.get_y() + 2, self.get_x() - 1)
        ls.append(top_left)
        top_right = (self.get_y() + 2, self.get_x() + 1)
        ls.append(top_right)

        bottom_left = (self.get_y() - 2, self.get_x() - 1)
        ls.append(bottom_left)
        bottom_right = (self.get_y() - 2, self.get_x() + 1)
        ls.append(bottom_right)

        left_top = (self.get_y() + 1, self.get_x() - 2)
        ls.append(left_top)

        left_bottom = (self.get_y() - 1, self.get_x() - 2)
        ls.append(left_bottom)

        right_top = (self.get_y() + 1, self.get_x() + 2)
        ls.append(right_top)

        right_bottom = (self.get_y() - 1, self.get_x() + 2)
        ls.append(right_bottom)

        pieces = ls.copy()
        for piece in ls:
            # assume a is start
            if piece[1] >= self.max_x or piece[1] < 0 or piece[0] < 0 or piece[0] >= self.max_y:
                pieces.remove(piece)

        # remove pieces in obstacles
        copy_pieces = pieces.copy()
        for piece in copy_pieces:
            obstacle = self.grid[piece[0]][piece[1]]
            is_obstacle = obstacle == -1
            if is_obstacle:
                pieces.remove(piece)

        return pieces


#############################################################################
######## Board
#############################################################################
class Board:
    pass


#############################################################################
######## State
#############################################################################
class State:
    def __init__(self, pieces, value):
        self.pieces = pieces
        self.value = value

    def get_answer(self):
        answer = {}
        for piece in self.get_pieces():
            answer[piece.get_coord()] = piece.get_piece_type()
        return answer

    def get_value(self):
        return self.value

    def get_pieces(self):
        return self.pieces

    def get_no_of_pieces_left(self):
        return len(self.pieces)


#############################################################################
######## Implement Search Algorithm
#############################################################################

def get_neighbour(pieces, index):
    value = 0
    piece_to_remove_coord = pieces[index].get_numeric_coord()
    remaining_pieces = []
    for piece in pieces:
        if not piece.get_numeric_coord() == piece_to_remove_coord:
            remaining_pieces.append(piece)
    attacking = {}

    for piece in remaining_pieces:
        attacking[piece.get_numeric_coord()] = piece.get_actions()

    for tiles_to_attack in attacking.values():
        for curr_attack in tiles_to_attack:
            if curr_attack in attacking.keys():
                value += 1

    return State(remaining_pieces, value)


def best_neighbour(state):
    best_state = state

    for i in range(state.get_no_of_pieces_left()):
        curr_state = get_neighbour(state.get_pieces(), i)
        if best_state.get_value() >= curr_state.get_value():
            best_state = curr_state

    return best_state


def search(rows, cols, grid, pieces, k):
    pieces_list = []

    for index in pieces:
        enemy = pieces[index]
        if enemy == "King":
            piece = King(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Rook":
            piece = Rook(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Bishop":
            piece = Bishop(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Queen":
            piece = Queen(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Knight":
            piece = Knight(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Ferz":
            piece = Ferz(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Princess":
            piece = Princess(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)
        if enemy == "Empress":
            piece = Empress(index[1], index[0], cols, rows, grid)
            pieces_list.append(piece)

    iterations = []

    for i in range(len(pieces_list)):
        state = get_neighbour(pieces_list, i)
        iterations.append(state)
    shuffle(iterations)

    for i in range(len(iterations)):
        state = iterations[i]

        while state.get_no_of_pieces_left() > int(k):
            state = best_neighbour(state)
            if state.get_value() == 0:
                return state.get_answer()

    # in (y, x) format


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()

    k = handle.readline().split(":")[1].strip()  # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece

    return rows, cols, grid, pieces, k


def add_piece(comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r, c), piece]


# Returns row and col index in integers respectively
def from_chess_coord(ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    testcase = sys.argv[1]  # Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    return goalstate  # Format to be returned
