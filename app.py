from flask import Flask, jsonify
app = Flask(__name__)

from bs4 import BeautifulSoup
import requests


@app.route('/url/<path:url_requested>')
def scrape_url(url_requested):

	parser = Parser()
	response = parser.parse_url(url_requested)

	return jsonify(response)


def create_app(debug=False):
	app = Flask(__name__)
	app.debug = debug
	return app


class Parser:

	def parse_url(self, base_url):
		'''
		
		Params:
			- base_url:@string - url of the requested page
		Return:
			- dictionary with return values
		'''
		try:
			request = requests.get(base_url)
			soup = BeautifulSoup(request.text, "html.parser")
		except:
			result = self._handle_failed_retrieval()
		else:
			result = self._parse_html_page(soup)

		return result


	def _parse_html_page(self, soup):
		result_functions = {
			"title": self._parse_title,
			"description": self._parse_description,
			"canonical_url": self._parse_canonical_url,
			"image": self._parse_image
		}
		result = {'head':{}, 'body':{}}
		missing_fields = []
		for key,f in result_functions.items():
			try: 
				result['body'][key] = f(soup)
			except:
				missing_fields.append(key)
		if len(missing_fields) > 0:
			result['head']['status'] = 'Incomplete'
			result['head']['message'] = 'Request succedeed but open graph fields are incomplete.'
			result['head']['missing_fields'] = missing_fields
		else:
			result['head']['status'] = 'Complete'
			result['head']['message'] = 'Request succedeed and open graph fields found.'
		return result


	def _parse_title(self, soup):
		try:
			title = soup.find("meta", property="og:title", content=True)["content"]
		except:
			raise ValueError('Title not found')
		return title


	def _parse_description(self, soup):
		try:
			description = soup.find("meta", property="og:description", content=True)["content"]
		except:
			raise ValueError('Description not found')
		return description


	def _parse_canonical_url(self, soup):
		try:
			canonical_url = soup.find("meta", property="og:url", content=True)["content"]
		except:
			raise ValueError('Canonical url not found')
		return canonical_url


	def _parse_image(self, soup):
		try:
			image = soup.find("meta", property="og:image", content=True)["content"]
		except:
			raise ValueError('Image not found')
		return image


	def _handle_failed_retrieval(self):
		result = {'head':{}, 'body':{}}
		result['head']['status'] = 'Failed'
		result['head']['message'] = 'Requested url could not be accessed.'
		return result

if __name__ == '__main__':
	app = create_app(debug=False)
	app.run()