from os import listdir
from os.path import isfile, join
import json

class FileManager:
	"""
	Class for managing files.
	"""
	def __init__(self, base_dir):
		base_dir += '/' if base_dir[-1] != '/' else ''
		self.files = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
		self.base_dir = base_dir

	def is_available(self, name):
		name = FileManager.prepare_name(name)
		try:
			im = self.base_dir + [f for f in self.files if name == f.split('.')[0]][0]
		except IndexError:
			im = ''

		return im

	@staticmethod
	def prepare_name(name):
		return ''.join([c for c in name if c.isalnum()]).lower()

	@staticmethod
	def save_html(html, file_path):
		with open(file_path, 'w') as fp:
			fp.write(html)

	@staticmethod
	def save_json(data, file_path):
		with open(file_path, 'w') as fp:
			json.dump(data, fp)

	@staticmethod
	def load_json(file_path):
		with open(file_path, 'r') as fp:
			data = json.load(fp)

		return data