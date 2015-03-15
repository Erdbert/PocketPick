from hero import Hero
from webinterface import WebInterface
from filemanager import FileManager
from custom_exceptions import DataFileError, MissingAttributesError
from PyQt4 import QtGui
import info

class HeroPool(WebInterface):
	"""
	Manages the heroes and their data.
	"""
	def __init__(self, file_path, base_url):
		WebInterface.__init__(self, base_url)

		self.file_path = file_path

	def load_heroes(self):
		try:
			heroes_data = FileManager.load_json(self.file_path)
		except IOError:
			heroes_data = {name : None for name in info.heroes_names}
			raise DataFileError('It seems that there is no data file available.')
		finally:
			fm = FileManager('images')

			heroes = {}
			attributes = ['img_name', 'related_to']

			for hero_name in heroes_data.keys():
				data = {}
				for att in attributes:
					try:
						data[att] = heroes_data[hero_name][att]
					except TypeError, AttributeError:
						data[att] = None

				heroes[hero_name] = Hero(hero_name, data['img_name'], data['related_to'])

			self.heroes = heroes

	def check_heroes(self):
		missing_attributes = {}
		for hero in self.heroes.values():
			missing = []
			if hero.img_name == 'images/nopic.png':
				missing.append('img_name')
			if not hero.related_to:
				missing.append('related_to')
			missing_attributes[hero.name] = missing

		return missing_attributes

	def add_heroes(self, heroes):
		for hero_name in heroes:
			self.heroes[hero_name] = Hero(hero_name, None, None)

	def save_heroes(self):
		heroes = {}
		for hero in self.heroes.keys():
			heroes[hero] = self.heroes[hero].to_json()

		FileManager.save_json(heroes, self.file_path)