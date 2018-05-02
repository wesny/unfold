==============================================================================
UnFold
==============================================================================
:Info: The UnFold platform allows publishers to collect micropayments for their articles.
:Author: Sweyn Venderbush <sweyn.venderbush@yale.edu>
:Copyright: © 2018, Sweyn Venderbush.
:Date: 2018-05-01
:Version: 0.1.0

.. index: README


PURPOSE
-------
UnFold allows publishers to integrate micropayments for articles quickly and easily into their sites using the `UnFold Django Plugin <http://github.com/wesny/unfold-plugin-django>`_. This repository contains the core UnFold server architecture and frontend interface.

SETUP
------------
To install, clone the UnFold directory to your development environment. While in the virtual environment for your application, cd into the cloned directory and run::

    pip install -r requirements.txt

You can then run the necessary migrations to initialize your database using::

    ./manage migrate

From there, you can run the UnFold server using::
    
    python manage.py runserver

You then need to create a .env file and fill the necessary variables in the .env file template below:

    # PostgreSQL
    POSTGRES_PASSWORD=
    POSTGRES_USER=
    CONN_MAX_AGE=

    # Domain name, used by caddy
    DOMAIN_NAME=

    # General settings
    DJANGO_READ_DOT_ENV_FILE=True
    DJANGO_ADMIN_URL=
    DJANGO_SETTINGS_MODULE=config.settings.local
    DJANGO_SECRET_KEY=4XG3HbNp2fMWWDlc4Z3wyY8rrIeHXglILRgaZG3CwB9QRuq6sJ
    DJANGO_ALLOWED_HOSTS=

    # AWS Settings
    DJANGO_AWS_ACCESS_KEY_ID=
    DJANGO_AWS_SECRET_ACCESS_KEY=
    DJANGO_AWS_STORAGE_BUCKET_NAME=

    # Used with email
    DJANGO_MAILGUN_API_KEY=
    DJANGO_SERVER_EMAIL=
    MAILGUN_SENDER_DOMAIN=

    # Security! Better to use DNS for this task, but you can use redirect
    DJANGO_SECURE_SSL_REDIRECT=False

    # django-allauth
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=True
    # Sentry
    DJANGO_SENTRY_DSN=

    #Stripe
    STRIPE_PUBLIC_KEY=
    STRIPE_PRIVATE_KEY=

This package also includes the Proc file necessary to deploy to Heroku. Using this production environment, you should set the fields described above as environment variables in your production environment. For help with this, see see detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to either the User or Publisher Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Running Your Own UnFold Server
^^^^^^^^^^^^^^^^^^^^^
The default UnFold Django Plugin lists the main UnFold server as the target for all queries. If you would like to change this, you can change it in the UnFold Django Plugin to point to your server. From there, your UnFold server can act as the central routing point for UnFold transactions.

UnFold allows for a variety of API calls, which are currently documented exclusively for use with the UnFold Django Plugin. However, while not documented, if you would like to integrate UnFold into your application manually, they are secure for use.




