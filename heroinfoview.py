from PyQt4 import QtGui

class HeroInfoView(QtGui.QWidget):
	def __init__(self, frame, parent):
		QtGui.QWidget.__init__(self, parent)

		self.frame = frame
		self.pool = frame.pool

		title = QtGui.QLabel('Hero information:', self)
		self.title_layout = QtGui.QHBoxLayout()
		self.title_layout.addWidget(title)
		self.title_layout.addStretch(1)

		self.__set_default_layout__()

	def display_hero(self, hero):
		layout = self.layout()

		layout.itemAt(1).itemAt(1).widget().setText(hero.name)
		layout.itemAt(1).itemAt(0).widget().setPixmap(QtGui.QPixmap(hero.img_name))

		count=0
		for vshero, adv in sorted([(k,hero.related_to[k]) for k in hero.related_to.keys()], key=lambda x: x[1], reverse=True):
			layout.itemAt(2).itemAt(count).widget().setPixmap(QtGui.QPixmap(self.pool.heroes[vshero].img_name))
			layout.itemAt(3).itemAt(count).widget().setText(str(adv))
			count += 1

	def __set_default_layout__(self):
		name = QtGui.QLabel()
		image = QtGui.QLabel()

		hbox_im = QtGui.QHBoxLayout()
		hbox_adv = QtGui.QHBoxLayout()
		for ii in range(16):
			hbox_im.addWidget(QtGui.QLabel())
			hbox_adv.addWidget(QtGui.QLabel())

		hbox_hero = QtGui.QHBoxLayout()
		hbox_hero.addWidget(image)
		hbox_hero.addWidget(name)
		hbox_hero.addStretch(1)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(self.title_layout)
		vbox.addLayout(hbox_hero)
		vbox.addLayout(hbox_im)
		vbox.addLayout(hbox_adv)

		self.setLayout(vbox)