import random

from hearthstone.enums import *

import fireplace.cards
from fireplace.brawls import *
from fireplace.game import BaseGame, CoinRules, Game
from fireplace.logging import log
from fireplace.player import Player
from fireplace.utils import random_draft


# Token minions
ANIMATED_STATUE = "LOEA04_27"
GOLDSHIRE_FOOTMAN = "CS1_042"
TARGET_DUMMY = "GVG_093"
KOBOLD_GEOMANCER = "CS2_142"
SPELLBENDERT = "tt_010a"
CHICKEN = "GVG_092t"
IMP = "EX1_598"
MURLOC = "PRO_001at"
WISP = "CS2_231"
WHELP = "ds1_whelptoken"
MECH = "BOT_309"
ELEMENTAL = "UNG_809t1"

# Token spells
INNERVATE = "VAN_EX1_169"
MOONFIRE = "CS2_008"
FIREBALL = "CS2_029"
PYROBLAST = "EX1_279"
CIRCLE_OF_HEALING = "EX1_621"
DREAM = "DREAM_04"
SILENCE = "EX1_332"
THE_COIN = "GAME_005"
HAND_OF_PROTECTION = "EX1_371"
MIND_CONTROL = "CS1_113"
TIME_REWINDER = "PART_002"
SOULFIRE = "EX1_308"
UNSTABLE_PORTAL = "GVG_003"
HOLY_LIGHT = "CS2_089"

# Token weapon
LIGHTS_JUSTICE = "CS2_091"

# Fandral Staghelm
FANDRAL_STAGHELM = "OG_044"

# Collectible cards excluded from random drafts
BLACKLIST = (
    "GVG_007",  # Flame Leviathan
    "AT_022",  # Fist of Jaraxxus
    "AT_130",  # Sea Reaver
    "KAR_096",  # Prince Malchezaar
    "CFM_637",  # Patches the Pirate
    "KAR_205",  # Silverware Golem
    "UNG_836",  # Clutchmother Zavas
    "TRL_252",  # High Priestess Jeklik
    "DRG_056",  # Parachute Brigand
    "DAL_185",  # Aranasi Broodmother
    "OG_123",  # Shifter Zerus
    "UNG_929",  # Molten Blade
    "LOOT_104",  #  Shifting Scroll
    "DRG_096",  # Bandersmosh
)

_draftcache = {}


def _draft(card_class, exclude, include):
    # random_draft() is fairly slow, this caches the drafts
    if (card_class, exclude, include) not in _draftcache:
        _draftcache[(card_class, exclude, include)] = random_draft(
            card_class, exclude + BLACKLIST, include
        )
    return _draftcache[(card_class, exclude, include)], card_class.default_hero


_heroes = fireplace.cards.filter(collectible=True, type=CardType.HERO)


class BaseTestGame(CoinRules, BaseGame):
    def start(self):
        super().start()
        self.player1.max_mana = 10
        self.player2.max_mana = 10


def _random_class():
    return CardClass(random.randint(2, 10))


def _empty_mulligan(game: BaseGame):
    for player in game.players:
        if player.choice:
            player.choice.choose()


def init_game(
    class1=None, class2=None, exclude=(), include=(), game_class=BaseTestGame
):
    log.info("Initializing a new game")
    if class1 is None:
        class1 = _random_class()
    if class2 is None:
        class2 = _random_class()
    player1 = Player("Player1", *_draft(class1, exclude, include))
    player2 = Player("Player2", *_draft(class2, exclude, include))
    game = game_class(players=(player1, player2))
    return game


def prepare_game(*args, **kwargs):
    game = init_game(*args, **kwargs)
    game.start()
    _empty_mulligan(game)

    return game


def prepare_empty_game(class1=None, class2=None, game_class=BaseTestGame):
    log.info("Initializing a new game with empty decks")
    if class1 is None:
        class1 = _random_class()
    if class2 is None:
        class2 = _random_class()
    player1 = Player("Player1", [], class1.default_hero)
    player1.cant_fatigue = True
    player2 = Player("Player2", [], class2.default_hero)
    player2.cant_fatigue = True
    game = game_class(players=(player1, player2))
    game.start()
    _empty_mulligan(game)

    return game
