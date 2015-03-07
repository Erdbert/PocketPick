from PyQt4 import QtGui

class MessageView(QtGui.QLabel):
	def __init__(self, parent=None):
		QtGui.QLabel.__init__(self, parent)

		self.setText("This is the Message Box.")