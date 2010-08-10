Django Depiction
================

What's this for
---------------

We were looking for profiling tools as we worked on improving the performance of
one of our Django applications.  We didn't find anything that tripped our
triggers so this was created.

It's some tooling, right now Middleware and a decorator, that allows you to
quickly see some profile data and optionally export a ``.kgrind`` file suitable
for viewing in KDE's KCacheGrind.

Installation
------------

You need Django for this to work, if you need help with that `head here
<http://djangoproject.com>`_

Using Pip::

    pip install django-depiction

.. todo:: Need to get this out on PyPi

Or::

    pip install -e git+http://github.com/robmadole/django-depiction.git#egg=djangodepiction

Usage
-----

Edit your Django settings, adding this to the ``MIDDLEWARE_CLASSES``. ::

    MIDDLEWARE_CLASSES = (
        ...
        'depiction.middleware.ProfilerMiddleware',
    )

You can trigger output by adding ``prof`` to the query string.  For example, say
this was a URL in your application ::

    http://127.0.0.1:8000/lumberjacks/list

To get some profile data on this page ::

    http://127.0.0.1:8000/lumberjacks/list?prof

If you already have a query string, add to it like this ::

    http://127.0.0.1:8000/lumberjacks/list?playsDressup=True&prof

To filter by filename ::

    http://127.0.0.1:8000/lumberjacks/list?playsDressup=True&prof=django/template
    
Credits
-------

This was mostly inspired by David Cramer's Middleware.  He get's most of the
credit for the idea and seed of the code we wrote.

`Here is the Middleware snippet <http://www.pastethat.com/dlnsr>`_
