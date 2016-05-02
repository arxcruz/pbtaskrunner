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
* nodejs-legacy (ubuntu)
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

If the above commands fail with the following error:
```
464 error Error: EACCES, mkdir '/home/arxcruz/tmp/npm-15103-QLU5egEY'
464 error  { [Error: EACCES, mkdir '/home/arxcruz/tmp/npm-15103-QLU5egEY']
464 error   errno: 3,
464 error   code: 'EACCES',
464 error   path: '/home/arxcruz/tmp/npm-15103-QLU5egEY' }
465 error Please try running this command again as root/Administrator.
466 error System Linux 4.2.0-27-generic
467 error command "/usr/bin/nodejs" "/usr/bin/npm" "install"
468 error cwd /home/arxcruz/pbtaskrunner
469 error node -v v0.10.25
470 error npm -v 1.3.10
471 error path /home/arxcruz/tmp/npm-15103-QLU5egEY
472 error code EACCES
473 error errno 3
474 error stack Error: EACCES, mkdir '/home/arxcruz/tmp/npm-15103-QLU5egEY'
```

Run again as root


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
