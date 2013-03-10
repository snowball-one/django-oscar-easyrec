from easyrec.utils import get_gateway

from django import template

easyrec = get_gateway()

register = template.Library()


@register.assignment_tag
def user_recommendations(user, max_results=None):
    """
    Usage: {% user_recommendations [user] as [var] %}

    Sets [var] to contain a list of recommended titles
    for the passed in user
    """
    return easyrec.get_user_recommendations(user.user_id, max_results)


@register.assignment_tag
def users_also_bought(
        product,
        user=None,
        max_results=None,
        item_type=None,
        requested_item_type=None
    ):
    """
    Usage: {% users_also_bought [product] [user] as [var] %}

    Sets [var] to contain a list of products which others who
    have bought [product] have also bought
    """
    user_id = None
    if user:
        user_id = user.id
    return easyrec.get_other_users_also_bought(
        product.upc,
        user_id,
        max_results,
        item_type,
        requested_item_type
    )


@register.assignment_tag
def users_also_viewed(
        product,
        user=None,
        max_results=None,
        item_type=None,
        requested_item_type=None
    ):
    """
    Usage: {% users_also_viewed [product] [user] as [var] %}

    Sets [var] to contain a list of products which others who
    have viewed [product] have also viewed
    """
    user_id = None
    if user:
        user_id = user.id

    return easyrec.get_other_users_also_viewed(
        product.upc,
        user_id,
        max_results,
        item_type,
        requested_item_type
    )


@register.assignment_tag
def products_rated_good(
        product,
        user=None,
        max_results=None,
        item_type=None,
        requested_item_type=None
    ):
    user_id = None
    if user:
        user_id = user.id
    return easyrec.get_items_rated_as_good_by_other_users(
        product.upc,
        user_id,
        max_results,
        item_type,
        requested_item_type
    )


@register.assignment_tag
def related_items(
        product,
        max_results=None,
        assoc_type=None,
        requested_item_type=None
    ):
    """
    Usage: {% related_items [product] as [var] %}

    Sets [var] to a list of products related to that specified by [product]
    """
    return easyrec.get_related_items(
        product.upc,
        max_results,
        assoc_type,
        requested_item_type
    )
