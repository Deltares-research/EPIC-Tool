
<a href="https://github.com/django/django"><img alt="Uses: Django" src="https://img.shields.io/badge/uses-django-000000.svg?style=for-the-badge&color=informational"></a>
<a href="https://github.com/encode/django-rest-framework"><img alt="Uses: Django REST framework" src="https://img.shields.io/badge/uses-django_rest_framework-00000.svg?style=for-the-badge&color=informational"></a>
<a href="https://github.com/adamchainz/django-cors-headers"><img alt="Uses: Django CORS headers" src="https://img.shields.io/badge/uses-django_cors_headers-000000.svg?style=for-the-badge&color=informational"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge"></a>

### Table of contents

* [About EPIC-Tool](#about-epic-tool-backend)
* [Collaborationg](#collaborating)
    * [Getting your development environment ready](#getting-your-development-environment-ready)
* [EpicTool (development) deployment](#epictool-development-deployment)
* [EpicTool (production) deployment](#epictool-production-deployment)
    * [Checking requirements](#checking-requirements)
    * [Installing Django](#installing-django)
    * [Gunicorn run](#gunicorn-run)
    * [NGINX configuration](#nginx-configuration)
* [Updating EpicTool models](#updating-epictool-models)
* [Appendix](#appendix)
    * [Installing on a CentOs machine](#installing-on-a-centos-machine)
        * [Preparation](#preparation)
        * [Installing SQLite3](#installing-sqlite3)
        * [Installing Python3](#installing-python-39)
        * [Installing Poetry](#installing-poetry)
        * [References](#references)
    * [Invoking the libraries](#invoking-the-libraries)

## About EPIC-Tool backend
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

## EpicTool (development) deployment.
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

## EpicTool (production) deployment.
To deploy the backend in an open environment we recommend following [Django guidelines](https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/gunicorn/) by using [gunicorn](https://docs.gunicorn.org/en/latest/install.html) and [NGINX](https://www.nginx.com/).

The following requirements should be met:

* UNIX system.
* NGINX. Already installed and configured.
* SQLite. At least version 3.9
* Python. At least version 3.8

Are you deploying on a CentOs machine? You can follow the [CentOs installation steps](#installing-on-a-centos-machine) for SQLite and Python in the [appendix section](#appendix).

#### Checking requirements 
It could be possible that your UNIX system does not have the latest python and/or SQLite versions. Please ensure you have installed Python (at least) 3.8 and SQLite (at least) 3.9.
To check it do the following:
```cli
python3
>> import sqlite3
>> sqlite3.sqlite_version
```
> * The first line will prompt us into the python3 CLI. Right below the executed line we will be able to see the current version of our Python3.
> * The third line will display the associated version of SQLite with our Python build.
>   * If it does not return the expected value then we recommend recompiling your python binaries.

### Installing Django

* Checkout the /backend directory of the EPIC-Tool repository somewhere recognizable. Such as /var/www/epictool-site/.

* For the first deployment we recommend executing our shell script.

    ```cli
    cd /var/www/epictool-site/
    ./initial_deployment.sh
    ```
    > This script will do the following:
    > * Generate the .django_screts and .django_debug (to False)
    > * Install the epic_app with all its dependencies.
    > * Import the initial data for the EpicApp.
    > * Collect and correctly place the static files (css and related).
    > * Run the server through 'gunicorn' in the background.

* Alternatively, run the previous script step by step unless they are not required in your environment (for instance when you already have the .django_secrets file or you already have users' inputs in the database):
    ```cli
    python3 -c "import secrets; from pathlib import Path; Path('.django_secrets').write_text(secrets.token_hex(16))"
    python3 -c "from pathlib import Path; Path('.django_debug').write_text('False')"
    poetry install
    poetry run python3 manage.py collectstatic --noinput
    ```
    * If we wish to regenerate the database and import all data:
    ```cli
    poetry run python3 manage.py epic_setup
    ```
    * Run the server:
    ```cli 
    poetry run gunicorn epic_core.wsgi
    ```

* We might still need to generate a superuser:
    ```
    poetry run python manage.py createsuperuser
    ```
    * If desired you can change the password after creating the user by running: 
    ```
    poetry run python manage.py changepassword <admin username>
    ```

### Gunicorn run:

If we have not executed the custom script, then we need to run on a separate process gunicorn, we only need to execute the following command line as a background activity:
```cli
    poetry run gunicorn epic_core.wsgi
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

## Updating EpicTool models.
During development it is natural to create new tables or define new columns on a database entry. The most important is to manage the Django migrations with the following steps:
```cli
python manage.py makemigrations
python manage.py migrate
```
Also, keep in mind that if a new entity needs to be modified through the Django Admin page it will also have to be added into the admin.py page.


## Appendix

### Installing on a CentOs machine:
In this section you will find the steps to follow in order to install the latest Python and SQLite versions in a CentOs machine. These steps are a summarized walk-through from the references listed in the [references section](#references).

#### Preparation
In order to ensure the installation happens correctly it is better to first download, compile and install SQLite3, this way we guarantee the follow-up [installation of Python](#installing-python-39) will pick up said latest version.

* Do a system update:

        sudo yum -y install epel-release
        sudo yum -y update

* Reboot server:

        sudo reboot

* Install required packages (needed for both SQLite and Python):
        
        sudo yum -y install wget
        sudo yum groupinstall "Development Tools" -y

#### Installing SQLite3

* Download source code:

        cd /opt
        mkdir sqlite3 && cd sqlite3
        wget https://www.sqlite.org/2022/sqlite-autoconf-3380500.tar.gz
        tar xvfz sqlite-autoconf-3380500.tar.gz

* Build and install:
        
        cd sqlite-autoconf-3380500
        ./configure
        sudo make
        sudo install

    If everything went well the libraries will have been installed to: `/usr/local/lib`.


* Verify installation:

        sqlite3 -version
    It can be that your system does not pick up this version because you did not add it to the PATH (or another SQLite version exists). You can temporarily modify this by exporting the path:

        alias sqlite3="/usr/local/bin/sqlite3"

    When running again the `sqlite3 -version` command you should see something like:
    > 3.38.5 2022-05-06 15:25:27 

#### Installing Python 3.9

* Install required specific packages:

        sudo yum install openssl-devel libffi-devel bzip2-devel -y

* Export the libraries to ensure the [latest SQLite3](#installing-sqlite3) installed version gets picked up:

        export LD_LIBRARY_PATH="/usr/local/lib/"
        alias sqlite3="/usr/local/bin/sqlite3"

* Download source code:

        cd /opt
        mkdir python39 && cd python39
        wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
        tar xvf Python-3.9.10.tgz
        cd Python-3.9.10

* Build and install:

        ./configure --enable-optimizations
        sudo make altinstall

* Verify installation:

        python3 --version
    > Python 3.9.10
        
        python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
    > 3.38.5

    If the latest step does not return at least that value you may need to recompile and install python ensuring the libraries are correctly exported as described in previous steps.

#### Installing Poetry:

* Install package under latest python3 library:
        
        curl -sSL https://install.python-poetry.org | python3 -
        export PATH="/root/.local/bin:$PATH"

* Verify installation:
        
        poetry --version
    > Poetry version 1.1.13


#### References:
* SQLite3:
    * [Installing Latest SQLite3](https://www.hostnextra.com/kb/how-to-install-sqlite3-on-centos-7/)
    * https://www.sqlite.org/2022/sqlite-autoconf-3380500.tar.gz
    > It might be good to replace the previous version of sqlite by moving it to a bak directory and renaming the latest one to the ‘sqlite3’. Taking over future invocations.
* Python 3.9:
    * [Installing latest Python on CentOs](https://computingforgeeks.com/install-latest-python-on-centos-linux/)
    > It is also possible replacing the previous python3 version, as with SQLite3, moving the python 3.6 to a backup directory (python3.6.bak), this way the alias gets picked up always.
* (Extra) [Poetry official installer](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

### Invoking the libraries:
To ensure everything gets picked up correctly you can execute the following command lines:
```cli
export LD_LIBRARY_PATH="/usr/local/lib/"
PATH=$PATH:/usr/local/bin
alias sqlite3="/usr/local/bin/sqlite3"
alias python3="/usr/local/bin/python3.9"
```
In addition, poetry might require this extra step:
```cli
export PATH="/root/.local/bin:$PATH"
```