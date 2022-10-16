import copy
import sys
import heapq
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


def get_king_actions(y, x, grid, row, col):
    ls = []
    right = (y, x + 1)
    ls.append(right)
    diag_right_up = (y + 1, x + 1)
    ls.append(diag_right_up)

    left = (y, x - 1)
    ls.append(left)
    diag_left_up = (y + 1, x - 1)
    ls.append(diag_left_up)

    down = (y - 1, x)
    ls.append(down)
    diag_left_down = (y - 1, x - 1)
    ls.append(diag_left_down)

    up = (y + 1, x)
    ls.append(up)
    diag_right_down = (y - 1, x + 1)
    ls.append(diag_right_down)

    pieces = ls.copy()
    for piece in ls:
        # assume a is start
        if piece[1] >= col or piece[1] < 0 or piece[0] < 0 or piece[0] >= row:
            pieces.remove(piece)

    # remove pieces in obstacles
    copy_pieces = pieces.copy()
    for piece in copy_pieces:
        obstacle = grid[piece[0]][piece[1]]
        is_obstacle = obstacle == -1
        if is_obstacle:
            pieces.remove(piece)
    pieces.append((y, x))
    return pieces


def get_queen_actions(y, x, grid, row, col):
    ls = []

    # rook like movement
    for i in range(x - 1, -1, -1):
        if grid[y][i] == -1:
            break
        piece = (y, i)
        ls.append(piece)

    for i in range(x + 1, col):
        if grid[y][i] == -1:
            break
        piece = (y, i)
        ls.append(piece)

    for i in range(y - 1, -1, -1):
        if grid[i][x] == - 1:
            break
        piece = (i, x)
        ls.append(piece)

    for i in range(y + 1, row):
        if grid[i][x] == - 1:
            break
        piece = (i, x)
        ls.append(piece)

    # bishop like movement
    counter_2 = 0
    for i in range(x - 1, - 1, -1):
        counter_2 -= 1
        if col > y + counter_2:
            if y + counter_2 < 0 or grid[y + counter_2][i] == - 1:
                break
            piece = (y + counter_2, i)
            ls.append(piece)

    counter_1 = 0
    for i in range(x + 1, col):
        counter_1 += 1
        if row > y + counter_1:
            if grid[y + counter_1][i] == - 1:
                break
            piece = (y + counter_1, i)
            ls.append(piece)

    counter_3 = 0
    for i in range(y - 1, - 1, -1):
        counter_3 += 1
        if col > x + counter_3:
            if grid[i][x + counter_3] == -1:
                break
            piece = (i, x + counter_3)
            ls.append(piece)

    counter_4 = 0
    for i in range(y + 1, row):
        counter_4 += 1
        if x - counter_4 >= 0:
            if grid[i][x - counter_4] == -1:
                break
            piece = (i, x - counter_4)
            ls.append(piece)

    ls.append((y, x))
    return ls


def get_bishop_actions(y, x, grid, row, col):
    ls = []

    counter_2 = 0
    for i in range(x - 1, - 1, -1):
        counter_2 -= 1
        if col > y + counter_2:
            if y + counter_2 < 0 or grid[y + counter_2][i] == - 1:
                break
            piece = (y + counter_2, i)
            ls.append(piece)

    counter_1 = 0
    for i in range(x + 1, col):
        counter_1 += 1
        if row > y + counter_1:
            if grid[y + counter_1][i] == - 1:
                break
            piece = (y + counter_1, i)
            ls.append(piece)

    counter_3 = 0
    for i in range(y - 1, - 1, -1):
        counter_3 += 1
        if col > x + counter_3:
            if grid[i][x + counter_3] == -1:
                break
            piece = (i, x + counter_3)
            ls.append(piece)

    counter_4 = 0
    for i in range(y + 1, row):
        counter_4 += 1
        if x - counter_4 >= 0:
            if grid[i][x - counter_4] == -1:
                break
            piece = (i, x - counter_4)
            ls.append(piece)

    ls.append((y, x))
    return ls


def get_rook_actions(y, x, grid, row, col):
    ls = []

    # rook like movement
    for i in range(x - 1, -1, -1):
        if grid[y][i] == -1:
            break
        piece = (y, i)
        ls.append(piece)

    for i in range(x + 1, col):
        if grid[y][i] == -1:
            break
        piece = (y, i)
        ls.append(piece)

    for i in range(y - 1, -1, -1):
        if grid[i][x] == - 1:
            break
        piece = (i, x)
        ls.append(piece)

    for i in range(y + 1, row):
        if grid[i][x] == - 1:
            break
        piece = (i, x)
        ls.append(piece)

    ls.append((y, x))
    return ls


def get_knight_actions(y, x, grid, row, col):
    ls = []

    top_left = (y + 2, x - 1)
    ls.append(top_left)
    top_right = (y + 2, x + 1)
    ls.append(top_right)

    bottom_left = (y - 2, x - 1)
    ls.append(bottom_left)
    bottom_right = (y - 2, x + 1)
    ls.append(bottom_right)

    left_top = (y + 1, x - 2)
    ls.append(left_top)

    left_bottom = (y - 1, x - 2)
    ls.append(left_bottom)

    right_top = (y + 1, x + 2)
    ls.append(right_top)

    right_bottom = (y - 1, x + 2)
    ls.append(right_bottom)

    pieces = ls.copy()
    for piece in ls:
        # assume a is start
        if piece[1] >= col or piece[1] < 0 or piece[0] < 0 or piece[0] >= row:
            pieces.remove(piece)

    # remove pieces in obstacles
    copy_pieces = pieces.copy()
    for piece in copy_pieces:
        obstacle = grid[piece[0]][piece[1]]
        is_obstacle = obstacle == -1
        if is_obstacle:
            pieces.remove(piece)

    pieces.append((y, x))
    return pieces


def get_frez_actions(y, x, grid, row, col):
    ls = []
    if y + 1 < row:
        if x - 1 >= 0:
            diag_left_up = (y + 1, x - 1)
            ls.append(diag_left_up)
        if x + 1 < col:
            diag_right_up = (y + 1, x + 1)
            ls.append(diag_right_up)

    if y - 1 >= 0:
        if x - 1 >= 0:
            diag_left_down = (y - 1, x - 1)
            ls.append(diag_left_down)
        if x + 1 < col:
            diag_right_down = (y - 1, x + 1)
            ls.append(diag_right_down)

    pieces = ls.copy()
    for piece in ls:
        # assume a is start
        if piece[1] >= col or piece[1] < 0 or piece[0] < 0 or piece[0] >= row:
            pieces.remove(piece)

    # remove pieces in obstacles
    copy_pieces = pieces.copy()
    for piece in copy_pieces:
        obstacle = grid[piece[0]][piece[0]]
        is_obstacle = obstacle == -1
        if is_obstacle:
            pieces.remove(piece)

    pieces.append((y, x))
    return pieces


def get_princess_actions(y, x, grid, row, col):
    ls = []

    # bishop like movement
    counter_2 = 0
    for i in range(x - 1, - 1, -1):
        counter_2 -= 1
        if col > y + counter_2:
            if y + counter_2 < 0 or grid[y + counter_2][i] == - 1:
                break
            piece = (y + counter_2, i)
            ls.append(piece)

    counter_1 = 0
    for i in range(x + 1, col):
        counter_1 += 1
        if row > y + counter_1:
            if grid[y + counter_1][i] == - 1:
                break
            piece = (y + counter_1, i)
            ls.append(piece)

    counter_3 = 0
    for i in range(y - 1, - 1, -1):
        counter_3 += 1
        if col > x + counter_3:
            if grid[i][x + counter_3] == -1:
                break
            piece = (i, x + counter_3)
            ls.append(piece)

    counter_4 = 0
    for i in range(y + 1, row):
        counter_4 += 1
        if x - counter_4 >= 0:
            if grid[i][x - counter_4] == -1:
                break
            piece = (i, x - counter_4)
            ls.append(piece)

    # knight like movement
    top_left = (y + 2, x - 1)
    ls.append(top_left)
    top_right = (y + 2, x + 1)
    ls.append(top_right)

    bottom_left = (y - 2, x - 1)
    ls.append(bottom_left)
    bottom_right = (y - 2, x + 1)
    ls.append(bottom_right)

    left_top = (y + 1, x - 2)
    ls.append(left_top)

    left_bottom = (y - 1, x - 2)
    ls.append(left_bottom)

    right_top = (y + 1, x + 2)
    ls.append(right_top)

    right_bottom = (y - 1, x + 2)
    ls.append(right_bottom)

    pieces = ls.copy()
    for piece in ls:
        # assume a is start
        if piece[1] >= col or piece[1] < 0 or piece[0] < 0 or piece[0] >= row:
            pieces.remove(piece)

    # remove pieces in obstacles
    copy_pieces = pieces.copy()
    for piece in copy_pieces:
        obstacle = grid[piece[0]][piece[1]]
        is_obstacle = obstacle == -1
        if is_obstacle:
            pieces.remove(piece)

    pieces.append((y, x))
    return pieces


def get_empress_actions(y, x, grid, row, col):
    ls = []

    # rook like movement
    for i in range(x - 1, -1, -1):
        if grid[y][i] == -1:
            break
        piece = (y, i)
        ls.append(piece)

    for i in range(x + 1, col):
        if grid[y][i] == -1:
            break
        piece = (y, i)
        ls.append(piece)

    for i in range(y - 1, -1, -1):
        if grid[i][x] == - 1:
            break
        piece = (i, x)
        ls.append(piece)

    for i in range(y + 1, row):
        if grid[i][x] == - 1:
            break
        piece = (i, x)
        ls.append(piece)

    # knight like movement
    top_left = (y + 2, x - 1)
    ls.append(top_left)
    top_right = (y + 2, x + 1)
    ls.append(top_right)

    bottom_left = (y - 2, x - 1)
    ls.append(bottom_left)
    bottom_right = (y - 2, x + 1)
    ls.append(bottom_right)

    left_top = (y + 1, x - 2)
    ls.append(left_top)

    left_bottom = (y - 1, x - 2)
    ls.append(left_bottom)

    right_top = (y + 1, x + 2)
    ls.append(right_top)

    right_bottom = (y - 1, x + 2)
    ls.append(right_bottom)

    pieces = ls.copy()
    for piece in ls:
        # assume a is start
        if piece[1] >= col or piece[1] < 0 or piece[0] < 0 or piece[0] >= row:
            pieces.remove(piece)

    # remove pieces in obstacles
    copy_pieces = pieces.copy()
    for piece in copy_pieces:
        obstacle = grid[piece[0]][piece[1]]
        is_obstacle = obstacle == -1
        if is_obstacle:
            pieces.remove(piece)

    pieces.append((y, x))
    return pieces


#############################################################################
######## Board
#############################################################################
## was never used
class Board:
    def __init__(self, board, pieces):
        self.board = board

    def get_board(self):
        return self.board


#############################################################################
######## State
#############################################################################
class State:
    def __init__(self, num_of_pieces_placed, num_of_free_tiles, free_tiles, path):
        self.num_of_pieces_placed = num_of_pieces_placed
        self.num_of_free_tiles = num_of_free_tiles
        self.free_tiles = free_tiles
        self.path = path

    def __lt__(self, other):
        return self.num_of_pieces_placed > other.num_of_pieces_placed or (
                self.num_of_pieces_placed == other.num_of_pieces_placed and self.num_of_free_tiles > other.num_of_free_tiles)

    def get_num_of_pieces_placed(self):
        return self.num_of_pieces_placed

    def get_num_of_free_tiles(self):
        return self.num_of_free_tiles

    def get_free_tiles(self):
        return self.free_tiles

    def get_path(self):
        return self.path

    def get_ans(self):
        output = {}
        for key, value in self.path.items():
            x = chr(key[1] + 97)
            y = key[0]
            output[(x, y)] = value
        return output


#############################################################################
######## Implement Search Algorithm
#############################################################################

def get_pieces(ls, no_of_pieces, string):
    for i in range(no_of_pieces):
        ls.append(string)
    return ls


def get_piece_action(piece_string, y, x, grid, row, col):
    piece = piece_string
    if piece == "Queen":
        return get_queen_actions(y, x, grid, row, col)
    elif piece == "Empress":
        return get_empress_actions(y, x, grid, row, col)
    elif piece == "Princess":
        return get_princess_actions(y, x, grid, row, col)
    elif piece == "Rook":
        return get_rook_actions(y, x, grid, row, col)
    elif piece == "Bishop":
        return get_bishop_actions(y, x, grid, row, col)
    elif piece == "Knight":
        return get_knight_actions(y, x, grid, row, col)
    elif piece == "King":
        return get_king_actions(y, x, grid, row, col)
    else:
        return get_frez_actions(y, x, grid, row, col)


def get_next_state(state, piece, actions, coord):
    # if piece is attacking another piece, break
    for key in state.get_path():
        for action in actions:
            if key == action:
                return State(-1, -1, {}, {})
    dic = {}
    curr_no_of_free_tiles = state.get_num_of_free_tiles()

    for key, value in state.get_free_tiles().items():
        dic[key] = value

    for action in actions:
        if dic[action]:
            dic[action] = False
            curr_no_of_free_tiles -= 1
    #shallow copy, need deep copy
    curr_path = {}
    for key, value in state.get_path().items():
        curr_path[key] = value
    curr_no_of_pieces = state.get_num_of_pieces_placed()
    curr_path[coord] = piece
    curr_no_of_pieces += 1

    return State(curr_no_of_pieces, curr_no_of_free_tiles, dic, curr_path)


def search(rows, cols, grid, num_pieces):
    pieces = []
    total_required_pieces = sum(num_pieces)
    no_of_king = num_pieces[0]
    no_of_queen = num_pieces[1]
    no_of_bishop = num_pieces[2]
    no_of_rook = num_pieces[3]
    no_of_knight = num_pieces[4]
    no_of_ferz = num_pieces[5]
    no_of_princess = num_pieces[6]
    no_of_empress = num_pieces[7]
    # order of adding add queen, empress, princess, rook, bishop, knight, king, ferz
    pieces = get_pieces(pieces, no_of_queen, "Queen")
    pieces = get_pieces(pieces, no_of_empress, "Empress")
    pieces = get_pieces(pieces, no_of_princess, "Princess")
    pieces = get_pieces(pieces, no_of_rook, "Rook")
    pieces = get_pieces(pieces, no_of_bishop, "Bishop")
    pieces = get_pieces(pieces, no_of_knight, "Knight")
    pieces = get_pieces(pieces, no_of_king, "King")
    pieces = get_pieces(pieces, no_of_ferz, "Ferz")

    free_tiles = {}
    num_of_free_tiles = rows * cols
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # stored in y, x format
            if grid[j][i] == -1:
                free_tiles[(j, i)] = False
                num_of_free_tiles -= 1
            else:
                free_tiles[(j, i)] = True
    pq = []

    example_state = State(0, num_of_free_tiles, free_tiles, {})
    heapq.heappush(pq, example_state)
    while not len(pq) == 0:
        curr_state = heapq.heappop(pq)
        for key, value in curr_state.get_free_tiles().items():
            if value:
                piece_string = pieces[curr_state.get_num_of_pieces_placed()]
                actions = get_piece_action(piece_string, key[0], key[1], grid, rows, cols)
                state = get_next_state(curr_state, piece_string, actions, key)
                if state.get_num_of_pieces_placed() == -1:
                    continue
                elif state.get_num_of_pieces_placed() == total_required_pieces:
                    return state.get_ans()
                heapq.heappush(pq, state)


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

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()

    piece_nums = get_par(handle.readline()).split()
    num_pieces = [int(x) for x in piece_nums]  # List in the order of King, Queen, Bishop, Rook, Knight

    return rows, cols, grid, num_pieces


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
def run_CSP():
    testcase = sys.argv[1]  # Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    return goalstate  # Format to be returned
