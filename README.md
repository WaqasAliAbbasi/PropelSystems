# PropelSystems

### Requirements

* Python >3.5
* pipenv 2018.10.9
  * To install `pip install pipenv`

### How to start app

* Activate virtual environment by `pipenv shell`
* Install dependencies by `pipenv install --ignore-pipfile`
* Start web server by `python manage.py runserver`
* Access web app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* When you are done, exit virtual environment by `exit`

### How to install packages

* Use pip to install whatever package you want e.g `pip install requests`
* Update requirements file (Pipfile.lock) by `pipenv lock`
