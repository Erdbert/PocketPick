class DataFileError(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)

class HTMLParsingError(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)