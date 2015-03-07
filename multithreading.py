from webcontent import WebContent
from PyQt4.QtCore import QObject, pyqtSignal
from time import sleep
import urllib
from filemanager import FileManager
import json

class HeroLoader(WebContent, QObject):

	data_loaded = pyqtSignal('QString', 'QString', 'QString')
	job_done = pyqtSignal()

	def __init__(self, view, pool, conn, what, interval=3, parent=None):
		WebContent.__init__(self, conn)
		QObject.__init__(self, parent)

		self.view = view
		self.pool = pool
		self.interval = interval
		self.what = what

		self.fetch_what = {'images' : self.fetch_image, 'related_to' : self.fetch_related_to}[what]

	def load_hero_data(self):
		self.view.updated.connect(self.disconnect_view_from_hero)
		for hero in sorted(self.pool.heroes.values(), key=lambda x: x.name):
			self.data_loaded.connect({'images' : hero.catch_image, 'related_to' : hero.catch_related_to}[self.what])
			hero.data_received.connect(self.disconnect_hero)
			hero.data_received.connect(self.view.update)

			self.fetch_what(hero.name)

			sleep(self.interval)

		self.view.updated.disconnect(self.disconnect_view_from_hero)

		self.job_done.emit()

	def disconnect_hero(self, name, slot):
		name = str(name)
		slot = str(slot)

		self.data_loaded.disconnect(self.pool.heroes[name].__getattribute__(slot))
		self.pool.heroes[name].data_received.disconnect(self.disconnect_hero)

	def disconnect_view_from_hero(self, name):
		name = str(name)
		
		self.pool.heroes[name].data_received.disconnect(self.view.update)

	def fetch_related_to(self, name):
		# print "Fetching versus data for {0} ...".format(name)

		hero_name = name

		name = HeroLoader.prepare_name_for_url(name)
		url = '/heroes/' + name + '/_versus'

		related_to = {}

		html = self.__get_html__(url)

		rows = html.replace('</tr>', '<tr>').split('<tr>')
		rows = [row for row in rows if '<img' in row]

		for row in rows:
			name_index = row.index('title=')
			name = row[name_index+7 : len(row)].split('"')[0]
			name = HeroLoader.prepare_name_from_html(name)

			cols = row.replace('</td>', '<td>').split('<td>')

			advantage = float(cols[4].split('%')[0])

			related_to[name] = advantage

		# print "Loaded related_to for {0}. Sleeping for 3 seconds now.".format(hero_name)

		self.data_loaded.emit('related_to', hero_name, json.dumps(related_to))

	def fetch_image(self, name):
		"""
		Fetches the image for the hero from the website.
		"""

		# print "Fetching image for {0} ...".format(name)

		hero_name = name

		name = HeroLoader.prepare_name_for_url(name)
		url = '/heroes/' + name

		html = self.__get_html__(url)

		html_name = HeroLoader.prepare_name_for_html(hero_name)

		tokens = html.replace('<img', '/>').split('/>')  # split at the image tag <img and the closing tag /> to get the image tag contents
		imtag = [tok for tok in tokens if 'title="{0}"'.format(html_name) in tok and 'src=' in tok][0]  # grab the image which contains the hero data

		src_index = imtag.find('src=')  # grab the image source ...
		img_url = imtag[src_index+5:imtag.find('"', src_index+5)]  # ... which is confined by ""

		new_img_name = 'images/' + FileManager.prepare_name(hero_name) + '.' + img_url.split('.')[-1]
		urllib.urlretrieve(img_url, new_img_name)

		# print "Saved image as {0}. Sleeping for 3 seconds now.".format(new_img_name)

		self.data_loaded.emit('image', hero_name, new_img_name)

	@staticmethod
	def prepare_name_for_url(name):
		return name.replace("'", "").replace(" ", "-").lower()

	@staticmethod
	def prepare_name_for_html(name):
		return name.replace("'", "&#39;")

	@staticmethod
	def prepare_name_from_html(name):
		return name.replace("&#39;", "'")