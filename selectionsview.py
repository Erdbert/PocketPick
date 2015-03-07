from namedbutton import NamedButton
from PyQt4 import QtGui, QtCore

class SelectionsView(QtGui.QWidget):
	def __init__(self, frame, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.frame = frame

		self.parties = {"Radiant" : QtGui.QWidget(self), "Dire" : QtGui.QWidget(self)}

		for party in self.parties.keys():
			self.__setup_party__(party)

		self.switch_button = QtGui.QPushButton(self)
		self.switch_button.setFixedSize(64, 48)
		self.switch_button.setIcon(QtGui.QIcon('images/switch.png'))
		self.switch_button.setIconSize(QtCore.QSize(48, 48))

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.parties["Radiant"])
		hbox.addWidget(self.switch_button)
		hbox.addWidget(self.parties["Dire"])

		self.setLayout(hbox)

		self.layout_map = {"RB" : self.parties["Radiant"].layout().itemAt(1), "RP" : self.parties["Radiant"].layout().itemAt(2), "DB" : self.parties["Dire"].layout().itemAt(1), "DP" : self.parties["Dire"].layout().itemAt(2)}

		self.hero_count = {"RB" : 1, "RP" : 1, "DB" : 1, "DP" : 1}
		self.selected_heroes = {"RB" : [], "RP" : [], "DB" : [], "DP" : []}

		self.selection_order = []
		self.step_order = []

	def __setup_party__(self, party):
		title = QtGui.QLabel(party)
		title_layout = QtGui.QHBoxLayout()
		title_layout.addStretch(1)
		title_layout.addWidget(title)
		title_layout.addStretch(1)

		bans_layout = QtGui.QHBoxLayout()
		picks_layout = QtGui.QHBoxLayout()
		bans_layout.addWidget(QtGui.QLabel('Bans:'))
		picks_layout.addWidget(QtGui.QLabel('Picks:'))
		for ii in range(0, 5):
			field = NamedButton('', self.parties[party])
			field.setIcon(QtGui.QIcon('images/blank.png'))
			field.setFixedSize(64, 36)
			field.setIconSize(QtCore.QSize(64, 36))
			bans_layout.addWidget(field)

			field = NamedButton('', self.parties[party])
			field.setIcon(QtGui.QIcon('images/blank.png'))
			field.setFixedSize(64, 36)
			field.setIconSize(QtCore.QSize(64, 36))
			picks_layout.addWidget(field)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(title_layout)
		vbox.addLayout(bans_layout)
		vbox.addLayout(picks_layout)

		self.parties[party].setLayout(vbox)

	def expose_selected_heroes(self, step):
		mapping = {'RB' : 'RP', 'RP' : 'DP', 'DB' : 'DP', 'DP' : 'RP'}
		return self.selected_heroes[mapping[step]]

	def __get_item_from_step__(self, step, count_diff=0):
		layout = self.layout_map[step]
		return layout.itemAt(self.hero_count[step]+count_diff).widget()

	def hero_selected(self, hero, step, frame):
		item = self.__get_item_from_step__(step)
		item.name = hero.name
		item.setIcon(QtGui.QIcon(hero.img_name))
		self.connect(item, QtCore.SIGNAL('clicked()'), frame.hero_back_to_pool)

		try:
			frame.disconnect(self.__get_item_from_step__(self.step_order[-1], -1), QtCore.SIGNAL('clicked()'), frame.hero_back_to_pool)
		except (AttributeError, IndexError):
			pass

		self.selected_heroes[step].append(hero)
		self.hero_count[step] += 1

		self.selection_order.append(hero)
		self.step_order.append(step)

	def hero_back_to_pool(self, frame):
		step = self.step_order[-1]

		item = self.__get_item_from_step__(step, -1)
		item.setIcon(QtGui.QIcon('images/blank.png'))
		frame.disconnect(item, QtCore.SIGNAL('clicked()'), frame.hero_back_to_pool)

		try:
			frame.connect(self.__get_item_from_step__(self.step_order[-2], -1), QtCore.SIGNAL('clicked()'), frame.hero_back_to_pool)
		except (AttributeError, IndexError):
			pass

		self.selected_heroes[step].pop()
		self.hero_count[step] -= 1

		self.selection_order.pop()
		self.step_order.pop()