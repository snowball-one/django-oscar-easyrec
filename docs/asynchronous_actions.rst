Asynchronous Actions
====================

As of `django-oscar-easyrec` 0.6 it is now possible to have collected actions
(views, ratings and purchases) delivered to easyrec asynchronously with the
aid of the most excellent `Celery`_. Installing and running celery is beyond
the scope of this documentation but can be found in the `Celery install guide`_


.. _`Celery`: http://www.celeryproject.org
.. _`Celery install guide`: http://www.celeryproject.org/install/

Once you have Celery up and running all that is needed to get
`django-oscar-haystack` using it to deliver actions asynchronously is to add
the following to your settings file::

    EASYREC_ASYNC = True

