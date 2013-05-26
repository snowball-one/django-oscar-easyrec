Getting Rankings
================

Also provided are a collection of template tags for getting community rankings
of products. i.e. Their popularity within certain actions. Thing like most
bought or best rated products. All these template
tags share the same syntax::

    {% <ranking_type> [time_range "ALL"] [max_results 15] [requested_item_type "ITEM"] %}


Each template tag provides a list of rankings in the same way as the
recommendation tags. e.g. a dictionary containing a product object, and a
tracking url.::

    {
        "product": <Product>,
        "tracking_url": "http://somewhere.com"
    }

If no recommendations are found then an empty list is returned.


Rankings Template Tags
======================


``most_viewed``
---------------

Returns the most viewed products


``most_bought``
---------------

Provides the most purchased items


``most_rated``
-------------

Products with the most rating. This is not the best rated products, but those
that have the greatest number of ratings in total, high or low.


``best_rated``
--------------

The products with the best ratings.


``worst_rated``
---------------

The products with the worst rated over all.


Example::

    {% load rankings %}

    {% most_viewed as rankings %}
    <ol>
    {% for item in rankings %}
        <li>
            <a href="{{ item.tracking_url }}">
                {{ item.product.title }}
            </a>
        </li>
    {% endfor %}
    </ol>


Parameters
----------

Permitted values for some of the optional parameters or more obvious than other
so here they are explained:


``time_range``
    The range over which you want the ranking. Options include:
    "DAY", "WEEK", "MONTH", "ALL". The default is "ALL"
``max_results``
    The maximum number of products you want. The default is up to 15
``requested_item_type``
    The item type you want in the results. The default is "ITEM"
