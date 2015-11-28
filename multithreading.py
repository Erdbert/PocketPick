from webcontent import WebContent
from PyQt4.QtCore import QObject, pyqtSignal
from time import sleep
import urllib
import urllib2
from filemanager import FileManager
import json
from os import path

class HeroLoader(WebContent, QObject):

	data_loaded = pyqtSignal('QString', 'QString', 'QString')
	job_done = pyqtSignal()

	def __init__(self, view, pool, conn, interval=3, parent=None):
		WebContent.__init__(self, conn)
		QObject.__init__(self, parent)

		self.view = view
		self.pool = pool
		self.interval = interval

	def load_hero_data(self):
		self.view.updated.connect(self.disconnect_view_from_hero)
		for hero in sorted(self.pool.heroes.values(), key=lambda x: x.name):
			self.data_loaded.connect(hero.catch_data)
			hero.data_received.connect(self.disconnect_hero)
			hero.data_received.connect(self.view.update)

			self.fetch_hero_data(hero.name)

			sleep(self.interval)

		self.view.updated.disconnect(self.disconnect_view_from_hero)

		self.job_done.emit()

	def disconnect_hero(self, name):
		name = str(name)

		self.data_loaded.disconnect(self.pool.heroes[name].catch_data)
		self.pool.heroes[name].data_received.disconnect(self.disconnect_hero)

	def disconnect_view_from_hero(self, name):
		name = str(name)
		
		self.pool.heroes[name].data_received.disconnect(self.view.update)

	def fetch_hero_data(self, name):
		hero_name = name

		name = HeroLoader.prepare_name_for_url(name)
		url = '/heroes/' + name

		html = self.__get_html__(url)

		related_to = self.fetch_related_to(html)
		img_name = self.fetch_image(hero_name, html)

		self.data_loaded.emit(hero_name, img_name, json.dumps(related_to))

	def fetch_related_to(self, html):
		related_to = {}

		tables = html.replace('</table>', '<table').split('<table')
		for ii in range(len(tables)):
			if 'best versus' in tables[ii].lower():
				best_versus = tables[ii+1]
			if 'worst versus' in tables[ii].lower():
				worst_versus = tables[ii+1]

		related_to.update(self.parse_versus(best_versus))
		related_to.update(self.parse_versus(worst_versus))

		return related_to

	def parse_versus(self, html):
		related_to = {}
		rows = [p for p in html.replace('</tr>', '<tr').split('<tr') if 'link-type-hero' in p]
		for row in rows:
			cols = [p for p in row.replace('</td>', '<td').split('<td') if len(p) > 1]

			tmp = cols[2][cols[2].find('>')+1:]
			tmp = tmp[tmp.find('>')+1:]
			tmp = tmp[:tmp.find('<')]
			name = tmp
			name = HeroLoader.prepare_name_from_html(name)

			advantage = cols[3][1:]
			advantage = float(advantage[:advantage.index('%')])

			related_to[name] = advantage

		return related_to


	def fetch_image(self, hero_name, html):
		"""
		Fetches the image for the hero from the website.
		"""

		headers = {
			'Host': 'en.dotabuff.com',
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0'
		}

		html_name = HeroLoader.prepare_name_for_html(hero_name)

		tokens = html.replace('<img', '/>').split('/>')  # split at the image tag <img and the closing tag /> to get the image tag contents
		# imtag = [tok for tok in tokens if 'title="{0}"'.format(html_name) in tok and 'src=' in tok][0]  # grab the image which contains the hero data
		imtag = [tok for tok in tokens if 'class="image-avatar image-hero"' in tok][0]

		src_index = imtag.find('src=')  # grab the image source ...
		img_url = imtag[src_index+5:imtag.find('"', src_index+5)]  # ... which is confined by ""
		img_url = 'http://en.dotabuff.com' + img_url

		new_img_name = path.join('images', FileManager.prepare_name(hero_name) + '.' + img_url.split('.')[-1])
		# urllib.urlretrieve(img_url, new_img_name)

		request = urllib2.Request(url=img_url, headers=headers)
		response = urllib2.urlopen(request)
		with open(new_img_name, 'wb') as fp:
			fp.write(response.read())

		return new_img_name

	@staticmethod
	def prepare_name_for_url(name):
		return name.replace("'", "").replace(" ", "-").lower()

	@staticmethod
	def prepare_name_for_html(name):
		return name.replace("'", "&#39;")

	@staticmethod
	def prepare_name_from_html(name):
		return name.replace("&#39;", "'")