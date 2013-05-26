Settings
========

``EASYREC_ENDPOINT``

A url pointing to the location of your easyrec
install.

Syntax::

    EASYREC_ENDPOINT = 'http://127.0.0.1:9090/easyrec-web'


``EASYREC_TENANT_ID``

This is effectively the user name for your `easyrec` account.

Syntax::

    EASYREC_TENANT_ID = 'EASYREC_DEMO'


``EASYREC_API_KEY``

Effectively the password for you `easyrec` account.

Syntax::

    EASYREC_API_KEY = '8ab9dc3ffcdac576d0f298043a60517a'


``EASYREC_ASYNC``

Alows you to switch the sending of actions to `easyrec` asynchronously. This
requires `Celery`_ to be installed any running. Defaults to `False`

Syntax::

    EASYREC_ASYNC = False


.. _`Celery`: http://www.celeryproject.org
