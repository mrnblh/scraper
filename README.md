# ScraperAPI

### How it works

The application accepts HTTP GET requests of the form:
* `GET http://localhost:5000/info?url=[requested_url]`

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

To run the example functional tests, run the command `$ pytest`. While the tests suite is quite simplicistic, it shows how to create a Flask app on demand to check if the REST APIs are working as expected. In a production-ready environment, lower level unit tests would be absolutely required too, along with higher level integration tests.

### Deployment on AWS/GCE and relative technologies

**DNS -** Before deployment, we would need to buy and setup a domain name to point to our server.
**WSGI server -** Flask’s built-in server is not suitable for production as it doesn’t scale well, therefore we need to choose a WSGI HTTP Server option. Gunicorn is a pre-fork worker model widely adopted by the community. Other then supporting eventlet and greenlet, it makes running a Flask application on multiple asynchronous processes quite simple.
**Proxy server -** It is best to use Gunicorn behind an HTTP proxy server, especially to handle slow clients. Nginx is one of the most common solutions. It enjoys much lower costs per client and doesn't suffer a penalty for handling slow clients, making it an advantageous solution both as a buffer and load balancer server.
**Virtualization -** The simplest way to easily deploy the service on AWS/GCE would be to dockerize Nginx, Gunicorn and Flask app using Docker and handle containers' orchestration using Kubernetes. Docker containers are particularly convenient because they allow us to pack and isolate each of our services with everything they need to run, without the burden of full virtualization (VMs).
**Production-ready -** A minimal list of tasks we need to implement before launching our service in production: (I) add caching as to avoid repeating queries to domains recently interrogated. MongoDB would be a good DB solution, providing both performances at scale and flexible data schema definition; (II) add a logging service along with its own log DB. At a global level, AWS and GCE already gives us many performance measures. At the opposite extreme, Flask custom Logger would give us the ability to measure performances at a much more fine-grained level, paying this advantage in terms of complexity; (III) add authentication in order to have control and potentially limit the number of queries performed by a single phisical entity; (IV) write integration tests; (V) automatically build documentation using tools like Sphinx or Pycco in order to make the app easier to mantain; (VI) set up a staging and production environments, along with a CI tool like Travis allowing us to automatically perform tests and deploy new features quickly and safely.

### Scale up to thousands QPS

We have to ways to scale up our application to an increasing number of requests:

* hotizontal scaling - use the Cluster Autoscaler tool available on both AWS and GCE as a way to increase (and decrease) the number of nodes necessary to respond to increasing service demand;
* vertical scaling - change backend stack and switch to fully asynchronous languages like Go instead of Python.

### Keep app scalable while adding services

If we wanted to augment the response with additional data, the most important concept to keep in mind would be services' abstraction. We should be able to compute each piece of data forming our final response in a completely asynchronous and independent way. The key to reach this goal is to keep our server-side as stateless as possible. More concretely, once we receive a hit on the server-side, we would split the requested resource into three independent resources, each independently computable: Open Graph tags, Facebook info and propietary data. To have this separation, we would need to split up the computation of the three resources into three corresponding services.



