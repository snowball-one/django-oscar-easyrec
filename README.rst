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

    EASYREC_HOST = 'http://intralife.researchstudio.at'
    EASYREC_PORT = 8080
    EASYREC_TENENT_ID = '...'
    EASYREC_API_KEY = '...'

And that's it! All purchases, product views and reviews will automatically be
pushed to easyrec.

You can also disable this app by setting `EASYREC_HOST` to 'DUMMY'.

Getting Recommendations
-----------------------

django-oscar-easyrec comes with a templatetag allowing you to easily fetch
recommendations and display them in your templates. There are currently 3
supported template tags which do pretty much what they say::

    {% load recommendations %}

    {% user_recommendations a_user as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% users_also_bought a_user a_product as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

    {% users_also_viewed a_user a_product as recommendations %}
    {% for recommended_product in recommendations %}
        <!-- Do your thing! -->
    {% endfor %}

Each template tag provides a list of recommended products. If no
recommendations are found then an empty list is returned.

TODO
----

* Dashboard stats stuff