# tag::randombotimports[]
import random
from .helpers import is_point_an_eye
from .base import Agent
# end::randombotimports[]
from collections import namedtuple

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
# end::random_bot[]
