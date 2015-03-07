import sys
from gui import MainWindow
from PyQt4 import QtGui

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	view = MainWindow()
	view.show()

	sys.exit(app.exec_())