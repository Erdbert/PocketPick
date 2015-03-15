from filemanager import FileManager
from PyQt4 import QtGui, QtCore
import json

class Hero(QtGui.QPushButton):
	"""
	Class that represents a hero. It will be displayed in form of its image.
	"""

	data_received = QtCore.pyqtSignal('QString')

	def __init__(self, name, img_name, related_to, parent=None):
		QtGui.QPushButton.__init__(self, parent)

		self.name = name

		fm = FileManager('images')		
		if not img_name:
			self.img_name = fm.is_available(self.name)
			if not self.img_name:
				self.img_name = 'images/nopic.png'
		else:
			self.img_name = img_name

		self.setIcon(QtGui.QIcon(self.img_name))
		self.setIconSize(QtCore.QSize(64, 36))

		if not related_to:
			self.related_to = {}
		else:
			self.related_to = related_to

		self.setToolTip(self.name)
		self.setFixedSize(64, 36)

		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

	def catch_data(self, name, img_name, related_to):
		if not str(name) == self.name:
			return

		img_name = str(img_name)
		related_to = json.loads(str(related_to))

		if img_name:
			self.img_name = img_name
			self.setIcon(QtGui.QIcon(self.img_name))

		if related_to:
			self.related_to = related_to

		self.data_received.emit(self.name)

	def to_json(self):
		return {'img_name' : self.img_name, 'related_to' : self.related_to}

	def __str__(self):
		return self.name