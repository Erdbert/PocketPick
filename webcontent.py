import httplib

class WebContent:
	"""
	Class for loading webcontents.
	"""
	def __init__(self, conn):
		self.conn = conn
		self.hdr = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-encoding" : "deflate", "Accept-language" : "en-US,en;q=0.5", "Connection" : "close", "Host" : conn.__dict__["host"], "User-agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0", "X-http-proto" : "HTTP/1.1", "X-real-ip" : "90.27.84.4"}

	def __get_html__(self, url):
		if not self.conn:
			raise ValueError("No connection established")

		self.conn.request('GET', url, headers=self.hdr)
		response = self.conn.getresponse()
		
		return response.read()