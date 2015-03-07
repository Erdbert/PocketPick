from heropool import HeroPool
from progressinfo import ProgressInfo
from custom_exceptions import DataFileError, HTMLParsingError
from dialogs import SliderDialog
from PyQt4 import QtGui, QtCore
from multithreading import HeroLoader

class HeroPoolView(QtGui.QWidget):
	def __init__(self, frame, parent):
		QtGui.QWidget.__init__(self, parent)

		self.frame = frame

		self.view = QtGui.QWidget(self)  # view onto the hero pool; will be changed with a progress info widget in case of updates;

		self.stacked_layout = QtGui.QStackedLayout()
		self.stacked_layout.addWidget(self.view)

		main_layout = QtGui.QVBoxLayout()
		main_layout.addLayout(self.stacked_layout)
		self.setLayout(main_layout)

		self.pool = HeroPool('hdata.json', 'www.dotabuff.com')
		try:
			self.pool.load_heroes()
		except DataFileError as exc:
			choice = QtGui.QMessageBox.question(self, 'No Data File', exc.message + '\nDo you want to load the data from the web?', 'ok', 'cancel', defaultButtonNumber=0)
			if choice == 0:
				self.update_related_to()

		grid = QtGui.QGridLayout()

		maxcol = 15
		count = 0
		for hero_name in sorted(self.pool.heroes.keys()):
			hero = self.pool.heroes[hero_name]
			hero.setParent(self)
			grid.addWidget(hero, count/maxcol, count%maxcol)
			count += 1

		self.view.setLayout(grid)

		self.__connect_heroes__()

	def update_related_to(self):
		self.update_heroes('related_to')

	def update_images(self):
		self.update_heroes('images')

	def update_heroes(self, what):
		dialog = SliderDialog()
		if dialog.exec_():
			off_time = dialog.get_value()
		else:
			return

		self.frame.messages.setText('Updating hero data ...')

		self.progress = ProgressInfo(self)
		self.progress.init_pbar(0, len(self.pool.heroes.keys()))

		self.stacked_layout.addWidget(self.progress)
		self.stacked_layout.setCurrentWidget(self.progress)

		self.worker = HeroLoader(self.progress, self.pool, self.pool.conn, what, off_time)

		self.thread = QtCore.QThread()
		self.worker.moveToThread(self.thread)

		self.thread.started.connect(self.worker.load_hero_data)
		self.worker.job_done.connect(self.thread.quit)
		self.thread.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.progress.finalize)
		self.thread.finished.connect(self.pool.save_heroes)

		self.thread.start()

	def switch_to_hero_view(self):
		self.frame.messages.setText(self.frame.procedure.current_step()[1])
		self.stacked_layout.setCurrentWidget(self.view)

	def __connect_heroes__(self):
		for hero in self.pool.heroes.values():
			self.frame.connect(hero, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.frame.request_hero_information)

	def __getitem__(self, hero):
		return self.pool.heroes[hero]

	@property
	def heroes(self):
	    return self.pool.heroes
	@heroes.setter
	def heroes(self, value):
	    raise AttributeError("heroes cannot be changed.")
	