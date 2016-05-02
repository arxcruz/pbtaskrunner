# PB Task Runner


## About
This is a POC test runner, using python, celery, angularjs, flask and redis

Basically you have a frontend running in angularjs and a backend running flask
either as a mod_wsgi or standalone, a redis server used as a messaging system,
and celery who connects to redis server to manage the tasks.

## Installation

### Development environment
You need to have some packages installed:
* virtualenv
* npm
* redis-server
* development packages for redis

#### Setting up the environment
First you need to create a virtualenv

```bash
cd pbtaskrunner_dir
virtualenv .virtualenv
source .virtualenv/bin/activate
```

Then install the dependences:
```bash
pip install -r requirements.txt
```

Now you need to install gulp and bower globally

```bash
sudo npm install gulp -g
sudo npm install bower -g
```

Now you can run npm and bower install inside pbtaskrunner directory:

```bash
npm install
bower install
```

Depending on your distro, npm package doesn't link node, and during the package
installation, it might complain that you don't have node binary installed, so
you can just create a symbolic link:

```bash
sudo ln -sf /usr/bin/npm /usr/bin/node
```

Generate the web page files:
```bash
gulp dev
```

Create database
```bash
python loaddb.py
```

#### Running

Now you're able to run the services:
You need to have 4 terminals. Run each command bellow in one different terminal
since it will not be runnig as a daemon.
Assuming you have the .virtualenv loaded:

Run the Flask application (api running on port 5000):
```bash
python debug.py
```

Running gulp (this will create a web server on port 5001):
```bash
gulp watch
```

Running redis-server:
```bash
sh scripts/run-redis.sh
```

And finally, run celery:
```bash
celery worker -A pbtaskrunner.celery --loglevel=info
```

Now you can go on your browser on http://localhost:5001/

And you should see the the PB Task Runner in action.

## Some screenshots
### Tests running
![alt text](https://github.com/arxcruz/pbtaskrunner/raw/master/screenshot/running.png)

### Pending test
![alt text](https://github.com/arxcruz/pbtaskrunner/raw/master/screenshot/pending_test.png)

### Logs
![alt text](https://github.com/arxcruz/pbtaskrunner/raw/master/screenshot/show_logs.png)

### Several runs simultaneously
![alt text](https://github.com/arxcruz/pbtaskrunner/raw/master/screenshot/two_runs.png)
