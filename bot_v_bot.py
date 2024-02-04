# tag::bot_vs_bot[]
import dlgo.goboard as goboard
from dlgo.utils import print_board, print_move
import time
import enum
import random
from dlgo.agent.helpers import is_point_an_eye
from dlgo.agent.base import Agent
from collections import namedtuple
class Player(enum.Enum) :
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

class Point(namedtuple('Point','row col')):
    def neighbors(self):
        return [
            Point(self.row -1, self.col),
            Point(self.row +1, self.col),
            Point(self.row, self.col -1),
            Point(self.row, self.col +1)]

class Move():
    def _init_(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.play is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

        @classmethod
        def play(cls, point):
            return Move(point = point)
        @classmethod
        def pass_turn(cls):
            return Move(is_pass = True)
        @classmethod
        def resign(cls):
            return Move(is_resign = True)

__all__ = ['RandomBot']

# tag::random_bot[]
class RandomBot(Agent):
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and \
                        not is_point_an_eye(game_state.board,
                                            candidate,
                                            game_state.next_player):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots = {
        Player.black: RandomBot(),
        Player.white: RandomBot(),
    }
    while not game.is_over():
        time.sleep(0.3)  # <1>

        #clear_screen()   # <2>
        print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)


if __name__ == '__main__':
    main()

# <1> We set a sleep timer to 0.3 seconds so that bot moves aren't printed too fast to observe
# <2> Before each move we clear the screen. This way the board is always printed to the same position on the command line.
# end::bot_vs_bot[]
