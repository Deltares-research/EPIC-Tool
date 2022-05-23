
<a href="https://github.com/django/django"><img alt="Uses: Django" src="https://img.shields.io/badge/uses-django-000000.svg?style=for-the-badge&color=informational"></a>
<a href="https://github.com/encode/django-rest-framework"><img alt="Uses: Django REST framework" src="https://img.shields.io/badge/uses-django_rest_framework-00000.svg?style=for-the-badge&color=informational"></a>
<a href="https://github.com/adamchainz/django-cors-headers"><img alt="Uses: Django CORS headers" src="https://img.shields.io/badge/uses-django_cors_headers-000000.svg?style=for-the-badge&color=informational"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge"></a>

# EPIC-Tool backend
The EPIC-Tool backend uses [Django](https://www.djangoproject.com/), a python web framework, which will be used by the frontend as an API.
For the current approach (Django + Vue) we will follow an approach similar to the one described in the following [vue+django guide](https://levelup.gitconnected.com/vue-django-getting-started-88d3f4c2ba62), and [django restapi guide](https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c) kudos to Bennett Garner for these extremely helpful resources.

## Collaborating
If you wish to collaborate on this project you may want to get familiar with our tooling. In this project the following packages are used:
* [poetry](https://python-poetry.org/) for package handler.
* [black](https://black.readthedocs.io/en/stable/) for code styling.
* [commitizen](https://commitizen-tools.github.io/commitizen/) for version control.

### Getting your development environment ready.
* Using pip:
    ```
    pip install poetry
    poetry install
    poetry run
    ```
* Using conda:
    > Note: it turns out if you work with conda as a python environment you may come against a compatibility problem with virtualenv, we therefore recommend downgrading the pre-installed package of virtualenv of poetry to 20.0.3.
    ```
    conda install poetry
    conda install virtualenv==20.0.33
    poetry install
    poetry run
    ```

You should have now all the dependencies, including django and djangorestframework, installed in our environment.

## Django (development) deployment.
Installing django is pretty simple. For the next steps we assume poetry has been installed as described in the previous steps.
* Navigate with the commandline to the \backend directory.
* Create a secret key through Python CLI
    ```cli
    python
    >> import secrets
    >> from pathlib import Path
    >> Path('.django_secrets').write_text(secrets.token_hex(16))
    ```
    > A new file is now generated containing your unique token key expected by /epic_core/settings.py. In case this key is not valid please contact carles.sorianoperez@deltares.nl to provide a valid one.
    > Define also the debug value: 'False' for production, 'True' for development:
    ```cli
    python
    >> from pathlib import Path
    >> Path('.django_debug').write_text("True")
    ```
* Run our custom command to create the database and add an admin user:
    ```
    poetry python manage.py epic_setup --test
    ```
    > This will import all initial data and generate a test admin user (admin-admin) and several test 'EpicUsers'.
    > An output in the command line will show you where the (local) server is deployed. By default you should be able to check its functioning here: http://127.0.0.1:8000/ 

## Creating new models.
During development it is natural to create new tables or define new columns on a database entry. The most important is to manage the Django migrations with the following steps:
```cli
python manage.py makemigrations
python manage.py migrate
```
Also, keep in mind that if a new entity needs to be modified through the Django Admin page it will also have to be added into the admin.py page.


## EpicTool backend deployment.
To deploy the backend in an open environment we recommend following [Django guidelines](https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/gunicorn/) by using [gunicorn](https://docs.gunicorn.org/en/latest/install.html) and [NGINX].

For this part we will assume a deployment in a UNIX environment.

### Setting up the EpicApp:

#### Pre-requirements.
* Unix system
* NGINX (we assume in this guideline it's already configured).
It could be possible that the current UNIX version does not have the latest python and/or SQLite versions. Please ensure you have installed Python (at least) 3.8 and SQLite (at least) 3.9.
To check it do the following:
```cli

python3
>> import sqlite3
>> sqlite3.sqlite_version
```
> The first line will prompt us into the python3 CLI. Right below the executed line we will be able to see the current version of our Python3.
> The third line will display the associated version of SQLite with our Python build.
> If it does not much the expected value then you should consider recompiling your python checkout.

### Installing Django

* Checkout the /backend directory of the EPIC-Tool repository somewhere recognizable. Such as /var/www/epictool-site/.

* Navigate to the fresh checkout

    ```cli
    /var/www/epictool-site/
    ```
* Create a secret key through Python CLI
    ```cli
    python
    >> import secrets
    >> from pathlib import Path
    >> Path('.django_secrets').write_text(secrets.token_hex(16))
    ```
    > A new file is now generated containing your unique token key expected by /epic_core/settings.py. In case this key is not valid please contact carles.sorianoperez@deltares.nl to provide a valid one.
    > Define also the debug value: 'False' for production:
    ```cli
    python
    >> from pathlib import Path
    >> Path('.django_debug').write_text("False")
    ```
* Run our custom command to create the database and then add an admin user:
    ```
    poetry run python manage.py epic_setup
    poetry run python manage.py createsuperuser
    ```
    > The last line will prompt us to a few dialogue in order to create a new admin user.
    > If desired you can change the password after creating the user by running: 
    ```
    poetry run python manage.py changepassword <admin username>
    ```
### Gunicorn run:
Assuming we have correctly installed gunicorn, we only need to execute the following command line as a background activity:
    ```cli
    poetry run gunicorn epic_setup.wsgi
    ```

### NGINX configuration:
Although we are already 'serving' our Django applicaiton, this does not mean that it is accessible outside our local machine.
Most likely you will require to do a redirection of the requests to the backend. For that it's necessary adding the following lines into your 'nginx' .conf file:
```conf
server {
    ...
    location ^~ /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location ^~ /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host      $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
Now our NGINX server will be able to redirect our http calls to our application. As a last step, restart the NGINX server:
    ```cli
    sudo systemctl restart nginx
    ```