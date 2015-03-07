from PyQt4 import QtGui, QtCore

class SliderDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

		self.setWindowTitle('Query off-time')

		default_value = 2

		self.info = QtGui.QLabel('Select the off-time in seconds between queries to the website\nin order to prevent ip-blocking due to high request frequencies.\nRecommended value: {0}'.format(default_value))
		self.text = QtGui.QLabel('Selected value: ', self)
		self.value = QtGui.QLabel(str(default_value), self)
		self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slider.setRange(0, 3)
		self.slider.setValue(default_value)
		self.slider.setTickInterval(1)
		self.slider.setSingleStep(1)
		self.slider.valueChanged.connect(self.update_value)

		self.ok_button = QtGui.QPushButton('ok', self)
		self.ok_button.clicked.connect(self.accept)
		self.cancel_button = QtGui.QPushButton('cancel', self)
		self.cancel_button.clicked.connect(self.reject)

		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(self.text)
		hbox1.addWidget(self.value)
		hbox1.addStretch(1)

		hbox2 = QtGui.QHBoxLayout()
		hbox2.addStretch(1)
		hbox2.addWidget(self.ok_button)
		hbox2.addStretch(1)
		hbox2.addWidget(self.cancel_button)
		hbox2.addStretch(1)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.info)
		vbox.addSpacing(20)
		vbox.addLayout(hbox1)
		vbox.addWidget(self.slider)
		vbox.addLayout(hbox2)

		self.setLayout(vbox)

	def update_value(self, value):
		self.value.setText(str(value))

	def get_value(self):
		return self.slider.value()