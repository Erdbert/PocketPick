from PyQt4 import QtGui

class NamedButton(QtGui.QPushButton):
	def __init__(self, name, parent=None):
		QtGui.QPushButton.__init__(self, parent)

		self.name = name