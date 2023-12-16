Moscow Python Meetup site
=========================

Sources of https://moscowpython.ru (previously moscowdjango.ru)


Running locally
---------------

Prerequisites:

- python 3.11
- node 11
- postgresql

Setup the postgresql database (psql snippet)::

    create role moscowdjango with password 'password' login createdb;
    create database moscowdjango with owner moscowdjango;

Clone the repository::

    git clone git@github.com:moscowpython/moscowpython.git

Create a virtualenv and install the requirements::

    cd moscowpython
    python3.11 -m venv env
    source env/bin/activate
    pip install pip-tools invoke
    inv install-requirements

Run migrations and load fixtures::

    inv migrate
    python manage.py loaddata development.json

Compile frontend::

    inv frontend

Run the server::

    inv run

Or with test settings to use the Django staticfiles storage::

    DJANGO_CONFIGURATION=Test inv run

Tests
-----
::

    inv check
    inv test
