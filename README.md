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
* Access admin at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
* When you are done, exit virtual environment by `exit`

### User Accounts

* Admin
  * Username: `admin@propelsystems.com`
  * Password: `propel123`
* Clinic Manager
  * Username: `waqas.abbasi@outlook.com`
  * Password: `propel123`
* Warehouse Personnel
  * Username: `david@propelsystems.com`
  * Password: `propel123`
* Dispatcher
  * Username: `piyushjha0999@gmail.com`
  * Password: `propel123`

### How to change models

* Change your models (in `models.py` of respective app).
* Run `python manage.py makemigrations` to create migrations for those changes
* Run `python manage.py migrate` to apply those changes to the database.
* Register model to admin interface so we can access/modify objects from the backend. For example, a model `Category` was created in `/supplies`. To register the model add the following lines to `/supplies/admin.py`:
  * `from .models import Category`
  * `admin.site.register(Category)`

### How to install packages

* Use `pipenv` instead of `pip` to install whatever package you want e.g `pipenv install requests`
