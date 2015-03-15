from webcontent import WebContent
from multithreading import HeroLoader
import httplib

class SingleRequest(WebContent):
	def __init__(self, conn):
		WebContent.__init__(self, conn)

	def fetch_hero_list(self):
		html = self.__get_html__('/heroes')

		parts = [p for p in html.replace('</div>', '<div').split('<div') if 'class="name"' in p]
		heroes = [HeroLoader.prepare_name_from_html( p[p.index('>')+1:] ) for p in parts]

		return heroes

conn  = httplib.HTTPConnection('www.dotabuff.com')
sreq = SingleRequest(conn)

for hero in sreq.fetch_hero_list():
	print hero