#import platform
#import subprocess

#import numpy as np

# tag::print_utils[]
import enum
class Player(enum.Enum) :
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

from collections import namedtuple

class Point(namedtuple('Point','row col')):
    def neighbors(self):
        return [
            Point(self.row -1, self.col),
            Point(self.row +1, self.col),
            Point(self.row, self.col -1),
            Point(self.row, self.col +1)]

COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: ' . ',
    Player.black: ' x ',
    Player.white: ' o ',
}


def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % (COLS[move.point.col - 1], move.point.row)
    print('%s %s' % (player, move_str))


def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' % (bump, row, ''.join(line)))
    print('    ' + '  '.join(COLS[:board.num_cols]))
# end::print_utils[]

'''

# tag::human_coordinates[]
def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)
# end::human_coordinates[]


def coords_from_point(point):
    return '%s%d' % (
        COLS[point.col - 1],
        point.row
    )

def clear_screen():
    # see https://stackoverflow.com/a/23075152/323316
    if platform.system() == "Windows":
        subprocess.Popen("cls", shell=True).communicate()
    else:  # Linux and Mac
        # the link uses print("\033c", end=""), but this is the original sequence given in the book.
        print(chr(27) + "[2J")

# NOTE: MoveAge is only used in chapter 13, and doesn't make it to the main text.
# This feature will only be implemented in goboard_fast.py so as not to confuse
# readers in early chapters.
class MoveAge():
    def __init__(self, board):
        self.move_ages = - np.ones((board.num_rows, board.num_cols))

    def get(self, row, col):
        return self.move_ages[row, col]

    def reset_age(self, point):
        self.move_ages[point.row - 1, point.col - 1] = -1

    def add(self, point):
        self.move_ages[point.row - 1, point.col - 1] = 0

    def increment_all(self):
        self.move_ages[self.move_ages > -1] += 1

'''