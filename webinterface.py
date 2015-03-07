import httplib

class WebInterface:
	"""
	Class for interaction with websites. Establishes and stores a connection to a website.
	"""
	def __init__(self, base_url):
		self.conn  = httplib.HTTPConnection(base_url)

	def close_connection(self):
		self.conn.close()

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.close_connection()

	@property
	def host(self):
	    return self.conn.__dict__["host"]
	@host.setter
	def host(self, url):
	    self.conn.close()
	    self.conn = httplib.HTTPConnection(url)
	