"""Some tools for drawing games"""

from functools import lru_cache
from itertools import cycle
from dataclasses import dataclass
from typing import Union, List

import random

import lexis


def is_singular_and_drawable(word):
    return lexis.is_drawable(word) and lexis.get_singular(word) == word


@lru_cache(maxsize=1)
def drawable_word_counts():
    wc = idiom.word_count_df()
    drawables = list(filter(is_singular_and_drawable, wc.index))
    return wc.loc[drawables]


def random_drawable_word(max_rank=1000):
    return drawable_word_counts().iloc[:max_rank].sample(1).index[0]


@dataclass
class FakeArtist:
    """A game of 'fake artist goes to new-york'.

    A video explaining the game: https://www.youtube.com/watch?v=916s7Tb01W8

    A pdf of the rules: https://tesera.ru/images/items/744225/rule_fakeartist_e.pdf

    The problem I wanted to solve: We're three in our family, so we can't really play
    because someone needs to decide on a drawable word and distribute the cards,
    so that person can't play, and since only two are left... each know who the other
    person is.

    With this, everyone can play!

    To play:

    .. code-block:: python

        game = FakeArtist(players=['Alice', 'Bob', 'Charlie'])
        game.deal_new_cards()
        # and then do this in a loop (only one loop is necessary usually)
        game.next_cycle_item()
        # This will either tell you who the next player is, or tell you the card of
        # that next player.

    """

    players: Union[int, List[str]] = 3
    max_rank: int = 1000

    current_cards = None
    view_cycle = None
    current_cycle_idx = None

    def __post_init__(self):
        if isinstance(self.players, int):
            self.players = list(range(self.players))
        self.n_players = len(self.players)

    def deal_new_cards(self):
        word = random_drawable_word(self.max_rank)
        cards = [word] * self.n_players
        # randomly select one of the cards to be the fake artist's one
        fake_artist_idx = random.randint(0, self.n_players - 1)
        cards[fake_artist_idx] = 'X'
        self.current_cards = cards
        self._mk_view_cycle()

    def _mk_view_cycle(self):
        def gen():
            for player_idx, card in enumerate(self.current_cards):
                yield f'Next player is:    {self.players[player_idx]}'
                yield f'For {self.players[player_idx]}, the card is........... {card}'

        self.view_cycle = cycle(list(gen()))

    def next_cycle_item(self):
        if self.view_cycle is None:
            print(f'You need to deal some cards first (using `deal_new_cards`)')
        return next(self.view_cycle)
