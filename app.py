from flask import Flask, jsonify
app = Flask(__name__)
#app.run(debug=True, host='0.0.0.0', port=8000)
#app.run()

from bs4 import BeautifulSoup
from flask import request
import requests


@app.route('/info', methods=['GET'])
def scrape_url():
	'''
	Method responding to 'GET http://localhost:5000/info?url=[requested_url]' HTTP requests.
	The REST API returns a json object composed of a header and body.
	'''
	url_requested = request.args.get('url')
	parser = Parser()
	response = parser.parse_url(url_requested)

	return jsonify(response)


class Parser:

	def parse_url(self, base_url):
		'''
		Given a url string as input, the method interrogates the correpondent 
		web page and returns the following Open Graph tags when available: 
		canonical url, title, description and image.
		Params:
			- base_url:@string - url of the requested page
		Return:
			- result:@dict - object containing either complete or partial Open 
			  Graph results based on availability
		'''
		try:
			# retrieve HTML page
			request = requests.get(base_url, headers={'User-Agent': 'Mozilla/5.0'})
			# raise error when HTTP response of type 4XX and 5xx is retrieved
			request.raise_for_status()
			# parge statis HTML page
			soup = BeautifulSoup(request.text, "html.parser")

		except requests.exceptions.MissingSchema as ex:
			result = self._handle_missing_schema_error(base_url)
		except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL) as ex:
			result = self._handle_connection_error(base_url)
		except requests.exceptions.HTTPError as ex:
			result = self._handle_http_error(base_url)			
		except Exception as ex:
			result = self._handle_generic_error(ex)

		else:
			# if HMTL retrieval succeeded, extract Open Graph objects
			result = self._parse_html_page(soup)

		return result


	def _parse_html_page(self, soup):
		'''
		Given a BeautifulSoup object (which already parsed the html page of interest), 
		this method looks for the following Open Graph tags: canonical url, title, 
		description and image.
		Params:
			- soup:@BeautifulSoup - object containing parsed html page of interest
		Return:
			- result:@dict - object containing either complete or incomplete 
			  Open Graph tags based on availability 
		'''
		result_functions = {
			"title": self._parse_title,
			"description": self._parse_description,
			"canonical_url": self._parse_canonical_url,
			"image": self._parse_image
		}
		result = {'header':{}, 'body':{}}
		missing_fields = []
		for key,f in result_functions.items():
			try: 
				result['body'][key] = f(soup)
			except:
				missing_fields.append(key)
		if len(missing_fields) > 0:
			result['header']['status'] = 'Incomplete'
			result['header']['message'] = 'Request succedeed but open graph fields are incomplete.'
			result['header']['missing_fields'] = missing_fields
		else:
			result['header']['status'] = 'Complete'
			result['header']['message'] = 'Request succedeed and all open graph fields were found.'
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


	def _handle_generic_error(self, url):
		result = {'header':{}}
		result['header']['status'] = 'Failed'
		result['header']['message'] = 'A generic error occurred.'
		return result


	def _handle_missing_schema_error(self, url):
		result = {'header':{}}
		result['header']['status'] = 'Failed'
		error_message = 'Invalid URL \'{}\': No schema supplied.'.format(url)
		solution_message = 'Perhaps you meant \'http://{}\'?.'.format(url)
		result['header']['message'] = error_message + ' ' + solution_message
		return result


	def _handle_connection_error(self, url):
		result = {'header':{}}
		result['header']['status'] = 'Failed'
		error_message = 'A connection error occured.'
		solution_message = 'Please, make sure that \'{}\' is a valid url.'.format(url)
		result['header']['message'] = error_message + ' ' + solution_message
		return result


	def _handle_http_error(self, url):
		result = {'header':{}}
		result['header']['status'] = 'Failed'
		error_message = 'A HTTP error occured.'
		solution_message = 'Please, make sure that \'{}\' is a valid resource.'.format(url)
		result['header']['message'] = error_message + ' ' + solution_message
		return result


if __name__ == '__main__':
	app.run(debug=True, port=5000)