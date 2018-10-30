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
* `$ cd [your_favourite_path]`
* `$ git clone https://github.com/mrnblh/scraper.git`

If you did not install virtualenv python package, do it with the following command:
* `$ pip install virtualenv`

Create a virtual environment:
* `$ cd scraper`
* `$ virtualenv scraper_env`

Activate the created virtual environment:
* windows: `$ scraper_env\Scripts\activate`
* linux/macos: `$ source scraper_env/bin/activate`

Install dependencies using the following command:
* `$ pip install -r requirements.txt`

Set up variable connecting the flask app to the app python script as follows:
* windows: `$ set FLASK_APP=app.py`
* linux/macos: `$ export FLASK_APP=app.py`

Finally run the application:
* `$ python -m flask run`

### Test

Run command `$ pytest`.