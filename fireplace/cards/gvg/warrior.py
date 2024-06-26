from ..utils import *


##
# Minions


class GVG_051:
    """Warbot"""

    enrage = Refresh(SELF, buff="GVG_051e")


GVG_051e = buff(atk=1)


class GVG_053:
    """Shieldmaiden"""

    play = GainArmor(FRIENDLY_HERO, 5)


class GVG_055:
    """Screwjank Clunker"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
    }
    powered_up = Find(FRIENDLY_MINIONS + MECH)
    play = Buff(TARGET, "GVG_055e")


GVG_055e = buff(+2, +2)


class GVG_056:
    """Iron Juggernaut"""

    play = Shuffle(OPPONENT, "GVG_056t")


class GVG_056t:
    """Burrowing Mine"""

    play = Hit(FRIENDLY_HERO, 10)
    draw = CAST_WHEN_DRAWN


class GVG_086:
    """Siege Engine"""

    events = GainArmor(FRIENDLY_HERO).on(Buff(SELF, "GVG_086e"))


GVG_086e = buff(atk=1)


##
# Spells


class GVG_050:
    """Bouncing Blade"""

    requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1}
    play = Hit(RANDOM(ALL_MINIONS - IMMUNE - (CURRENT_HEALTH == MIN_HEALTH)), 1).then(
        Dead(Hit.TARGET) | CastSpell("GVG_050")
    )


class GVG_052:
    """Crush"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET)
    cost_mod = Find(FRIENDLY_MINIONS + DAMAGED) & -4


##
# Weapons


class GVG_054:
    """Ogre Warmaul"""

    events = FORGETFUL
