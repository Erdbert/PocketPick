import info
from hero import Hero
from heropool import HeroPool
from heropoolview import HeroPoolView
from selectionsview import SelectionsView
from dialogs import SliderDialog
from gui import MainWindow
import httplib
import time

import sys
from PyQt4 import QtGui

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	# view = HeroPoolView()
	# view = SelectionsView()
	# view = SliderDialog()
	view = MainWindow()
	view.show()


	# conn = httplib.HTTPConnection('www.dotabuff.com')
	# with HeroPool('', 'www.dotabuff.com') as pool:
	# 	pool.save_heroes('hdata.json')
	# for hero_name in info.heroes_names:
	# 	hero = Hero(hero_name, '', [], conn)
	# 	hero.fetch_html_page()
	

	sys.exit(app.exec_())