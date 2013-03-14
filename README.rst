================================
Easyrec package for django-oscar
================================

This package provides integration with the recommendation system, `easyrec`_.  It is designed to
integrate seamlessly with the e-commerce framework `django-oscar`_ but can be used without
using oscar.

.. _`easyrec`: http://easyrec.org/
.. _`django-oscar`: https://github.com/tangentlabs/django-oscar

Getting started
===============

Installation
------------

From PyPI::

    pip install django-oscar-easyrec

or from Github::

    pip install git+git://github.com/tangentlabs/django-oscar-easyrec.git#egg=django-oscar-easyrec

Add ``'easyrec'`` to ``INSTALLED_APPS``

Configuration
-------------

Edit your ``settings.py`` to set the following settings::

    EASYREC_ENDPOINT = 'http://127.0.0.1:8080/easyrec-web/'
    EASYREC_TENANT_ID = '...'
    EASYREC_API_KEY = '...'

In easyrec all items have an itemtype. django-oscar-easyrec passes the product
class name for this value. If the item type is not registered in easyrec it
will send the default value of 'ITEM'.

So each of your product classes needs to manually added as an itemtype via
easyrecs dashboard if you want them to be recorded separately.

Note - if you add item types to easyrec you will need to restart your django
project to ensure they are picked up correctly.

And that's it! All purchases, product views and reviews will automatically be
pushed to easyrec.

You can also disable this app by setting `EASYREC_HOST` to 'DUMMY'. Useful for
testing.

Getting Recommendations
=======================

django-oscar-easyrec comes with a templatetag allowing you to easily fetch
recommendations and display them in your templates. There are currently 5
supported template tags which do pretty much what they say::

    {% load recommendations %}

    {% user_recommendations request.user as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% users_also_bought a_product request.user as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% users_also_viewed a_product request.user as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% products_rated_good product as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% related_products product as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

Each template tag provides a list of recommended products. If no
recommendations are found then an empty QuerySet is returned. Each of these
tags also supports a number of other optional parameters.

You can also call the recommendation functions directly::

    from easyrec.utils import get_gateway
    easyrec = get_gateway()
    recommendations = easyrec.get_user_recommendations(user.user_id)
    recommendations = easyrec.get_other_users_also_bought(product.upc, user_id)
    recommendations = easyrec.get_other_users_also_viewed(product.upc, user_id)


user_recommendations
--------------------

Returns a list of recommended items for a user

parameters:

user
    The user to get recommendations for
max_results
    [optional] The maximum recommendation you wish to receive
requested_item_type
    [optional] The ProductClass of the items you want in the response
action_type
    [optional] The action type you want to get results based on. Valid values
    are: VIEW, RATE, BUY or any other custom action type you created. Default:
    VIEW

users_also_bought
-----------------

Returns a list of recommended items based on users who bought this all bought X

parameters:

product
    The produce you want to find recommendation based on
user
    The request user
max_results
    [optional] The maximum recommendation you wish to receive
requested_item_type
    [optional] The ProductClass of the items you want in the response

users_also_viewed
-----------------

Returns a list of recommended items based on users who viewed this all viewed X

parameters:

product
    The produce you want to find recommendation based on
user
    The request user
max_results
    [optional] The maximum recommendation you wish to receive
requested_item_type
    [optional] The ProductClass of the items you want in the response

products_rated_good
-------------------

Returns a list of recommended items based on users who rated this as good also
rated X as good.

parameters:

product
    The produce you want to find recommendation based on
user
    The request user
max_results
    [optional] The maximum recommendation you wish to receive
requested_item_type
    [optional] The ProductClass of the items you want in the response

related_products
----------------

Returns a list of items related to the supplied one

parameters:

product
    The produce you want to find recommendation based on
user
    The request user
max_results
    [optional] The maximum recommendation you wish to receive
assoc_type
    [optional] The association type that denotes the type of recommendation
    (e.g. BOUGHT_TOGETHER, GOOD_RATED_TOGETHER, etc.) you want to retrieve.
    If not supplied the default value IS_RELATED will be used.
requested_item_type
    [optional] The ProductClass of the items you want in the response

Vagrant
=======

To make testing and development easier I have created a vagrant box with
easyrec already installed and configured. If you have vagrant install you
can simply perform the following::

	vagrant up

The box itself is hosted on Dropbox and the initial download and install will
take a *long* time. So kick back and tasty hot beverage...

Once the box is up you can acces easyrec using::

	http://127.0.0.1:9090/easyrec-web

The username and password to log in are both `easyrec`. The box also runs
MySQL (`root`:`root`) and Tomcat-admin (`tomcat`:`tomcat`)

TODO
----

* Dashboard stats
* Ehance sandbox with some more data/products to allow easier testing
* Optional Celery delayed inserts
