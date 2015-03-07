from namedbutton import NamedButton
from PyQt4 import QtGui, QtCore

class PickListView(QtGui.QScrollArea):
	def __init__(self, frame, parent):
		QtGui.QScrollArea.__init__(self, parent)

		self.view = QtGui.QWidget()
		self.view_layout = QtGui.QVBoxLayout()
		self.view.setLayout(self.view_layout)

		self.setWidget(self.view)
		self.setWidgetResizable(True)

		self.title = QtGui.QLabel('Suggestions:', self)
		self.view_layout.addWidget(self.title)

		self.frame = frame

	def __add_hero__(self, hero, advantage):
		advantage_layout = QtGui.QHBoxLayout()
		advantage_layout.addStretch(1)
		advantage_layout.addWidget(QtGui.QLabel('%1.2f'%(advantage)))
		advantage_layout.addStretch(1)

		hero_img = NamedButton(hero.name)
		hero_img.setIcon(QtGui.QIcon(hero.img_name))
		hero_img.setFixedSize(64, 36)
		hero_img.setIconSize(QtCore.QSize(64, 36))
		self.frame.connect(hero_img, QtCore.SIGNAL('clicked()'), self.frame.hero_selected_from_picklist)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(hero_img)
		hbox.addLayout(advantage_layout)
		self.view_layout.addLayout(hbox)

	def add_heroes(self, heroes):
		self.clear_layout()
		for hero in heroes:
			self.__add_hero__(hero[0], hero[1])

	def clear_layout(self):
		# while(self.view_layout.count() > 0):
		# 	self.view_layout.itemAt(0).itemAt(0).widget().hide()
		# 	self.view_layout.itemAt(0).itemAt(1).widget().hide()
		# 	self.view_layout.removeItem(self.view_layout.itemAt(0))

		for index in range(self.view_layout.count(), 1, -1):
			self.view_layout.itemAt(index-1).itemAt(0).widget().deleteLater()

			self.frame.disconnect(self.view_layout.itemAt(index-1).itemAt(1).itemAt(1).widget(), QtCore.SIGNAL('clicked()'), self.frame.hero_selected_from_picklist)
			self.view_layout.itemAt(index-1).itemAt(1).itemAt(1).widget().deleteLater()

			self.view_layout.itemAt(index-1).itemAt(1).deleteLater()

			self.view_layout.removeItem(self.view_layout.itemAt(index-1))