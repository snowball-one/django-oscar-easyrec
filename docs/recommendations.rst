Getting Recommendations
=======================

django-oscar-easyrec comes with a templatetag allowing you to easily fetch
recommendations and display them in your templates. There are a number
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

Each template tag provides a list of recommendations. Each recommendation is a
dictionary containing a product object, and a tracking url. e.g.::

    {
        "product": <Product>,
        "tracking_url": "http://somewhere.com"
    }

If no recommendations are found then an empty list is returned. Each of these
tags also supports a number of other optional parameters.

You can also call the recommendation functions directly::

    from easyrec.utils import get_gateway

    easyrec = get_gateway()
    recommendations = easyrec.get_user_recommendations(user.user_id)
    recommendations = easyrec.get_other_users_also_bought(product.upc, user_id)
    recommendations = easyrec.get_other_users_also_viewed(product.upc, user_id)


Recommendation Template Tags
============================


``user_recommendations``
------------------------

Returns a list of recommended items for a user

Syntax::

    {% user_recommendations <user> [max_results 15] [requested_item_type "ITEM"] [action_type "VIEW"] %}


``users_also_bought``
---------------------

Returns a list of recommended items based on users who bought this also bought X

Syntax::

    {% users_also_bought <product> <user> [max_results 15] [requested_item_type "ITEM"] %}


``users_also_viewed``
---------------------

Returns a list of recommended items based on users who viewed this also viewed X

Syntax::

    {% users_also_viewed <product> <user> [max_results 15] [requested_item_type "ITEM"] %}


``products_rated_good``
-----------------------

Returns a list of recommended items based on users who rated this as good also
rated X as good.

Syntax::

    {% product_rated_good <product> <user> [max_results 15] [requested_item_type "ITEM"] %}


``related_products``
--------------------

Returns a list of items related to the supplied one

Syntax::

    {% related_products <product> <user> [max_results 15] [assoc_type "IS_RELATED"] [requested_item_type "ITEM"] %}


Parameters
----------

Permitted values for some of the optional parameters are more obvious than other
so let go through them here just to make sure:

``max_results``
    The maximum number of products you want. The default is up to 15
``requested_item_type``
    The item type you want in the results. The default is "ITEM"
``assoc_type``
    The associate type between the products. The default is "IS_RELATED" but
    you have the following options: "BOUGHT_TOGETHER", "GOOD_RATED_TOGETHER",
    "IS_RELATED", "VIEWED_TOGETHER".
