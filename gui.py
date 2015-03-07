from heropoolview import HeroPoolView
from selectionsview import SelectionsView
from picklistview import PickListView
from heroinfoview import HeroInfoView
from procedure import Procedure
from estimator import Estimator

from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.setWindowTitle('PocketPick')

		self.view = QtGui.QWidget(self)

		self.setCentralWidget(self.view)

		self.messages = QtGui.QLabel('', self.view)
		self.pool = HeroPoolView(self, self.view)
		self.selections = SelectionsView(self, self.view)
		self.picklist = PickListView(self, self.view)
		self.heroinfo = HeroInfoView(self, self.view)

		menubar = self.menuBar()

		menu = menubar.addMenu('Update')
		menu_update_images = QtGui.QAction('Update images', self)
		menu_update_images.triggered.connect(self.pool.update_images)
		menu.addAction(menu_update_images)
		menu_update_vs = QtGui.QAction('Update versus data', self)
		menu_update_vs.triggered.connect(self.pool.update_related_to)
		menu.addAction(menu_update_vs)

		menu = menubar.addMenu('Help')
		menu_howto = QtGui.QAction('HowTo', self)
		menu_howto.triggered.connect(self.howto)
		menu.addAction(menu_howto)
		menu_about = QtGui.QAction('About', self)
		menu_about.triggered.connect(self.about)
		menu.addAction(menu_about)

		messages_layout = QtGui.QHBoxLayout()
		messages_layout.addStretch(1)
		messages_layout.addWidget(self.messages)
		messages_layout.addStretch(1)

		grid_layout = QtGui.QGridLayout()
		grid_layout.addWidget(self.picklist, 0, 0, 4, 1)
		grid_layout.addLayout(messages_layout, 0, 1)
		grid_layout.addWidget(self.pool, 1, 1)
		grid_layout.addWidget(self.selections, 2, 1)
		grid_layout.addWidget(self.heroinfo, 3, 1)
		self.view.setLayout(grid_layout)

		self.procedure = Procedure('R')
		step = self.procedure.next()
		self.step = step[0]
		if not self.messages.text():
			self.messages.setText(step[1])

		self.estimator = Estimator(self.pool.heroes.values())

		self.__connect_heroes__()
		self.connect(self.selections.switch_button, QtCore.SIGNAL('clicked()'), self.switch_start)

	def __connect_heroes__(self):
		for hero in self.pool.heroes.values():
			self.connect(hero, QtCore.SIGNAL('clicked()'), self.hero_selected_from_pool)

	def __disconnect_heroes__(self):
		for hero in self.pool.heroes.values():
			self.disconnect(hero, QtCore.SIGNAL('clicked()'), self.hero_selected_from_pool)

	def request_hero_information(self, point):
		self.heroinfo.display_hero(self.sender())

	def switch_start(self):
		mapping = {'D' : 'R', 'R' : 'D'}
		self.procedure = Procedure(mapping[self.step[0]])
		step = self.procedure.next()
		self.step = step[0]
		self.messages.setText(step[1])

	def hero_selected_from_pool(self):
		self.hero_selected(self.sender())

	def hero_selected_from_picklist(self):
		self.hero_selected(self.pool.heroes[self.sender().name])

	def hero_selected(self, hero):
		hero.setEnabled(False)
		self.selections.hero_selected(hero, self.step, self)
		try:
			step = self.procedure.next()
		except StopIteration:
			self.__disconnect_heroes__()
			self.picklist.clear_layout()
			self.messages.setText("Good luck and have fun!")
		else:
			self.step = step[0]
			self.messages.setText(step[1])

			self.picklist.add_heroes(self.estimator.estimate(self.selections.expose_selected_heroes(self.step)))

		if self.selections.switch_button.isEnabled():
			self.selections.switch_button.setEnabled(False)

	def hero_back_to_pool(self):
		hero = self.pool.heroes[self.sender().name]
		hero.setEnabled(True)

		step = self.procedure.previous()
		self.step = step[0]
		self.messages.setText(step[1])

		self.selections.hero_back_to_pool(self)

		self.picklist.add_heroes(self.estimator.estimate(self.selections.expose_selected_heroes(self.step)))

		if len(self.selections.selection_order) == 0:
			self.selections.switch_button.setEnabled(True)

	def howto(self):
		self.popup = QtGui.QLabel()
		self.popup.setText('How to use this program:\nThis program simulates the pick/ban phase of the Dota 2 Captains Mode.\nEach turn all remaining heroes are sorted by the quality of picking/banning them and displayed on the left side.\nThis quality is based on the performance of the hero against other heroes as given on the website www.dotabuff.com (advantage).\nA left click on a hero selects it for the required action.\nA right click on a hero shows information about that hero on the bottom of the main window.\nHeroes can be sent back to the pool by left clicking their icon in the selection view. This can only be done in reversed order to that they were selected.\nThe double arrow button between the teams selections switches the beginning team. This button is only active if no hero has been picked.\nHero images and more important their statistics can be updated from the web. The source of information is www.dotabuff.com.\nIn case of an updated of the versus data the programm will parse the dotabuff website in order to extract the advantages/disadvantages for every hero.\nThis data will be saved to a file and on the next start loaded from that file.')
		self.popup.setWindowTitle('HowTo')
		self.popup.setGeometry(600, 300, 1000, 300)
		self.popup.show()

	def about(self):
		self.popup = QtGui.QLabel()
		self.popup.setText('PocketPick v0.1\n03/07/2015\n(c) None')
		self.popup.setWindowTitle('About')
		self.popup.setGeometry(600, 300, 250, 150)
		self.popup.show()