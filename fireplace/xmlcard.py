import os
from xml.etree import ElementTree


_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, "data", "TextAsset")


class XMLCard(object):
	_tags = {
		"type": "CardType",
		"health": "Health",
		"durability": "Durability",
		"atk": "Atk",
		"cost": "Cost",
		"race": "Race",
		"charge": "Charge",
		"taunt": "Taunt",
		"divineShield": "Divine Shield",
		"oneTurnEffect": "OneTurnEffect",
		"hasAura": "Aura",
	}

	@classmethod
	def get(cls, id):
		from . import carddata
		if not hasattr(carddata, id):
			return cls(id)
		return getattr(carddata, id)(id)

	def __init__(self, id):
		self.file = os.path.join(_path, "%s.xml" % (id))
		self.xml = ElementTree.parse(self.file)

	def __getattribute__(self, name):
		parent = super()
		if name != "_tags" and name in self._tags:
			if hasattr(parent.__self_class__, name):
				return parent.__getattribute__(name)
			return self.getTag(self._tags[name])
		return parent.__getattribute__(name)

	def getTag(self, name):
		tag = self.xml.findall('./Tag[@name="%s"]' % (name))
		if not tag:
			return 0
		tag = tag[0]
		value, type = tag.attrib["value"], tag.attrib["type"]
		if type == "Bool":
			return bool(int(value))
		return int(value)

	@property
	def name(self):
		return self.xml.findall("./Tag[@name='CardName']/enUS")[0].text


