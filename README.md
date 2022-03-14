## Description
This project intends to merge a front and backend being the first a VUE.js application and the latter a Django one.

# Installation steps
It is a requirement to first have Python and node.js installed in our machines. We will assume both requirements are fulfilled after checking out this repository.
The coupling of both front and back end has been done with the help of the following [guide](https://auth0.com/blog/building-modern-applications-with-django-and-vuejs/) Kudos to them.

First, we need to install django
```
pip install django
```

Then we will run the django backend to make suure it works correctly:
```
python manage.py migrate
python manage.py runserver
```
Note that the first step is to migrate / create the database, during regular development you might just run only the second line.

To run both together:

```
# run Django in the background
python manage.py runserver &

# move to the frontend directory
cd frontend

# run Vue.js in the background &
npm run dev &
```