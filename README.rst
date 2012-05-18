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

    EASYREC_HOST = 'intralife.researchstudio.at'
    EASYREC_PORT = 8080
    EASYREC_TENENT_ID = '...'
    EASYREC_API_KEY = '...'

And that's it! All purchases, product views and reviews will automatically be pushed to easyrec.

TODO
----

* Recommendation retrieval
* Dashboard stats stuff