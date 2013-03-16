from easyrec.utils import get_gateway

from django import template
from django.db.models import get_model

Product = get_model('catalogue', 'Product')

easyrec = get_gateway()

register = template.Library()

@register.assignment_tag
def most_viewed(
    time_range=None,
    max_results=None,
    requested_item_type=None,
    ):
    """
    Usage: {% most_viewed as [var] %}

    Sets [var] to contain a list of most viewed titles
    for the passed in user
    """
    try:
        return easyrec.get_most_viewed_items(
            time_range,
            max_results,
            requested_item_type
        )
    except:
        return Product.objects.none()

@register.assignment_tag
def most_bought(
    time_range=None,
    max_results=None,
    requested_item_type=None,
    ):
    """
    Usage: {% most_bought as [var] %}

    Sets [var] to contain a list of most bought titles
    for the passed in user
    """
    try:
        return easyrec.get_most_bought_items(
            time_range,
            max_results,
            requested_item_type
        )
    except:
        return Product.objects.none()

@register.assignment_tag
def most_rated(
    time_range=None,
    max_results=None,
    requested_item_type=None,
    ):
    """
    Usage: {% most_rated as [var] %}

    Sets [var] to contain a list of most rated titles
    for the passed in user
    """
    try:
        return easyrec.get_most_rated_items(
            time_range,
            max_results,
            requested_item_type
        )
    except:
        return Product.objects.none()

@register.assignment_tag
def best_rated(
    time_range=None,
    max_results=None,
    requested_item_type=None,
    ):
    """
    Usage: {% best_rated as [var] %}

    Sets [var] to contain a list of best rated titles
    for the passed in user
    """
    try:
        return easyrec.get_best_rated_items(
            time_range,
            max_results,
            requested_item_type
        )
    except:
        return Product.objects.none()

@register.assignment_tag
def worst_rated(
    time_range=None,
    max_results=None,
    requested_item_type=None,
    ):
    """
    Usage: {% worst_rated as [var] %}

    Sets [var] to contain a list of worst rated titles
    for the passed in user
    """
    try:
        return easyrec.get_worst_rated_items(
            time_range,
            max_results,
            requested_item_type
        )
    except:
        return Product.objects.none()
