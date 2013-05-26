Getting Started
===============

Installation
------------

From PyPI::

    pip install django-oscar-easyrec

or from Github::

    pip install git+git://github.com/tangentlabs/django-oscar-easyrec.git#egg=django-oscar-easyrec

Add ``'easyrec'`` to ``INSTALLED_APPS``.

You will also need to install easyrec itself.

Instructions for installing Easyrec can be found on `easyrec's sourceforge wiki`_

.. _`easyrec's sourceforge wiki`: http://easyrec.sourceforge.net/wiki/index.php?title=Installation_Guide

.. note::
    If you want to make use of back tracking urls. Ensure you set the site url
    correctly in the tenants configuration section of ``easyrec``.

I'd also heartily recommend reading through some of the basic concepts of
``easyrec`` to get a better idea of how to get the best out of it.


Configuration
-------------

Edit your ``settings.py`` to set the following settings::

    EASYREC_ENDPOINT = 'http://127.0.0.1:8080/easyrec-web/'
    EASYREC_TENANT_ID = '...'
    EASYREC_API_KEY = '...'

In easyrec all items have an 'itemtype'. django-oscar-easyrec passes the
product class name for this value. If the item type is not registered in
easyrec it will send the default value of 'ITEM'.

So each of your product classes needs to manually added as an itemtype via
easyrec's dashboard if you want them to be recorded separately.

.. note::
    If you add itemtypes to easyrec you will need to restart your django
    project to ensure they are picked up correctly.

And that's it! All purchases, product views and reviews will automatically be
pushed to easyrec.
