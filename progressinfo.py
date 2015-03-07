from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal

class ProgressInfo(QtGui.QWidget):

	updated = pyqtSignal('QString')

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.pbar = QtGui.QProgressBar(self)
		self.logview = QtGui.QScrollArea(self)
		self.log = QtGui.QLabel(self.logview)
		self.logview.setWidget(self.log)
		self.logview.setWidgetResizable(True)

		self.slider = self.logview.verticalScrollBar()

		self.log.setObjectName('log')
		self.log.setStyleSheet('font-size: 12pt')
		# self.log.setStyleSheet('QLabel#log {text-align: right, font-size: 12pt, font-style: bold}')

		self.ok_button = QtGui.QPushButton('continue')
		self.ok_button.setEnabled(False)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.pbar)
		vbox.addWidget(self.logview)
		vbox.addWidget(self.ok_button)
		self.setLayout(vbox)

		# self.setGeometry(500, 400, 200, 200)

		self.show()

	def init_pbar(self, vmin, vmax):
		self.pbar.setMinimum(vmin)
		self.pbar.setMaximum(vmax)

	def update(self, name, slot):
		name = str(name)
		slot = str(slot)
		
		msg = {'catch_image' : 'image', 'catch_related_to' : 'versus data'}[slot]
		msg = '{0}: {1} loaded.'.format(name, msg)

		self.pbar.setValue(self.pbar.value() + 1)
		self.log.setText(self.log.text() + '\n' + msg)
		self.slider.setValue(self.slider.maximum())

		self.updated.emit(name)

	def finalize(self):
		self.pbar.setValue(self.pbar.maximum())
		self.log.setText(self.log.text() + '\nCompleted!')

		self.parentWidget().frame.selections.switch_button.setEnabled(True)

		self.ok_button.setEnabled(True)
		self.ok_button.clicked.connect(self.parentWidget().switch_to_hero_view)