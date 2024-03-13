from ..utils import *


##
# Minions

class DAL_060:
	"""Clockwork Goblin"""
	# [x]<b>Battlecry:</b> Shuffle a Bomb into your opponent's deck. When drawn, it
	# explodes for 5 damage.
	play = Shuffle(OPPONENT, "BOT_511t")


class DAL_064:
	"""Blastmaster Boom"""
	# [x]<b>Battlecry:</b> Summon two 1/1 Boom Bots for each Bomb in your opponent's deck.
	play = Summon(CONTROLLER, "GVG_110t") * (Count(FRIENDLY_DECK + ID("BOT_511t")) * 2)


class DAL_070:
	"""The Boom Reaver"""
	# <b>Battlecry:</b> Summon a copy of a minion in your deck. Give it <b>Rush</b>.
	play = Summon(CONTROLLER, Copy(FRIENDLY_DECK + MINION)).then(
		Buff(Summon.CARD, "DAL_070e")
	)


DAL_070e = buff(rush=True)


class DAL_759:
	"""Vicious Scraphound"""
	# Whenever this minion deals damage, gain that much Armor.
	events = Damage(CHARACTER, None, SELF).on(
		GainArmor(FRIENDLY_HERO, Damage.AMOUNT)
	)


class DAL_770:
	"""Omega Devastator"""
	# [x]<b>Battlecry:</b> If you have 10 Mana Crystals, deal 10 damage to a minion.
	play = Hit(TARGET, 10)


##
# Spells

class DAL_008:
	"""Dr. Boom's Scheme"""
	# Gain @ Armor. <i>(Upgrades each turn!)</i>
	class Hand:
		events = OWN_TURN_BEGIN.on(AddProgress(SELF, SELF))

	play = GainArmor(FRIENDLY_HERO, Attr(SELF, GameTag.QUEST_PROGRESS) + Number(1))


class DAL_059:
	"""Dimensional Ripper"""
	# Summon 2 copies of a minion in your deck.
	play = (
		SetAttribute(SELF, "_card", RANDOM(FRIENDLY_DECK + MINION)),
		Summon(CONTROLLER, GetAttribute(SELF, "_card")) * 2,
		DelAttribute(SELF, "_card"),
	)


class DAL_062:
	"""Sweeping Strikes"""
	# Give a minion "Also damages minions next to whomever this attacks."
	play = Buff(TARGET, "DAL_062e")


class DAL_062e:
	events = Attack(OWNER).on(Hit(ADJACENT(Attack.DEFENDER), ATK(OWNER)))


class DAL_769:
	"""Improve Morale"""
	# [x]Deal $1 damage to a minion. If it survives, add a <b>Lackey</b> to your hand.
	play = Hit(TARGET, 1), Dead(TARGET) | Give(CONTROLLER, RandomLackey())


##
# Weapons

class DAL_063:
	"""Wrenchcalibur"""
	# After your hero attacks, shuffle a Bomb into your [x]opponent's deck.
	events = Attack(FRIENDLY_HERO).after(Shuffle(OPPONENT, "BOT_511t"))
