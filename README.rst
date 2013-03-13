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

From PyPi::

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
class name for this value if it is registered in easyrec itself, otherwise it
will send the default value of 'ITEM'.

So each or you product classes need to manually added as an itemtype via
easyrecs dashboard if you want them to be recorded separately.

Note - if you add item types to easyrec you will need to restart your django
project to ensure they are picked up correctly.

And that's it! All purchases, product views and reviews will automatically be
pushed to easyrec.

You can also disable this app by setting `EASYREC_HOST` to 'DUMMY'. Useful for
testing.

Getting Recommendations
-----------------------

django-oscar-easyrec comes with a templatetag allowing you to easily fetch
recommendations and display them in your templates. There are currently 3
supported template tags which do pretty much what they say::

    {% load recommendations %}

    {% user_recommendations request.user as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% users_also_bought request.user a_product as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% users_also_viewed request.user a_product as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

Each template tag provides a list of recommended products. If no
recommendations are found then an empty QuerySet is returned.

You can also call the recommendation functions directly::

    from easyrec.utils import get_gateway
    easyrec = get_gateway()
    recommendations = easyrec.get_user_recommendations(user.user_id)
    recommendations = easyrec.get_other_users_also_bought(product.upc, user_id)
    recommendations = easyrec.get_other_users_also_viewed(product.upc, user_id)

TODO
----

* Dashboard stats
* Optional Celery delayed inserts
