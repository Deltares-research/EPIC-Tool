# EPIC-Tool backend
The EPIC-Tool backend uses [Django](https://www.djangoproject.com/), a python web framework, which will be used by the frontend as an API.
For the current approach (Django + Vue) we will follow an approach similar to the one described in the following [vue+django guide](https://levelup.gitconnected.com/vue-django-getting-started-88d3f4c2ba62), and [django restapi guide](https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c) kudos to Bennett Garner for these extremely helpful resources.

## Collaborating
If you wish to collaborate on this project you may want to get familiar with our tooling. In this project the following packages are used:
* [poetry](https://python-poetry.org/) for package handler.
* [black](https://black.readthedocs.io/en/stable/) for code styling.
* [commitizen](https://commitizen-tools.github.io/commitizen/) for version control.
* [pytest] for internal testing of the tool.
### Getting your development environment ready.
* Using pip:
    ```
    pip install poetry
    poetry run
    ```
* Using conda:
    ```
    conda install poetry
    conda install virtualenv==20.0.33
    poetry run
    ```
    > Note: it turns out if you work with conda as a python environment you may come against a compatibility problem with virtualenv, we therefore recommend downgrading the pre-installed package of virtualenv of poetry to 20.0.3.


## Django installation and deployment.
Installing django is pretty simple. For the steps that follow we assume the user has their own python environment already running up.
* Navigate with the commandline to the \backend directory.
* Install django in your machine (check latest stable django version on their official website.)
    ```
    pip install django
    ```
* Create a secret key through Python CLI
    ```cli
    python
    >> import secrets
    >> from pathlib import Path
    >> Path('.django_secrets').write_text(secrets.token_hex(16))
    ```
    * A new file is now generated containing your unique token key expected by /epic_core/settings.py
    * In case this key is not valid please contact carles.sorianoperez@deltares.nl to provide a valid one.
* Migrate the database to ensure you have the correct scheme
    ```
    python manage.py migrate
    ```
* Run the Django server with the defined settings
    ```
    python manage.py runserver
    ```
    * An output in the command line will show you where the server is deployed.
    * By default you should be able to check its functioning here: http://127.0.0.1:8000/ 