# ScraperAPI

### How it works

The application accepts HTTP GET requests of the form:
* `GET localhost:5000/url/https://www.bbc.com/news`

The application response will be of the form:

```
{
   'head':{
       'status': one within ['Complete','Incomplete','Failed'],
       'message': message describing the status,
       'missing_fields': list of missing fields in case of 'Incomplete' status
   },
   'body':{
       // all open graph field that could be found in the form of 'open_graph_key': 'content'
   }
}
```

### Setup

Clone this git repository using the following commands:
* `cd [your_favourite_path]`
* `git clone https://github.com/mrnblh/scraper.git`

If you did not install virtualenv python package, do it with the following command:
* `pip install virtualenv`

Get inside the project folder (cd scraper) and activate the corresponding virtual environment:
* windows: `scraper\Scripts\activate`
* linux/macos: `source scraper/bin/activate`

Install dependencies using the following command:
* `pip install -r requirements.txt`

Or run:
* `pipenv install request`

Set up variable connecting the flask app to the app python script as follows:
* windows: `set FLASK_APP=app.py`
* linux/macos: `export FLASK_APP=app.py`

### Test

Run command `pytest`.