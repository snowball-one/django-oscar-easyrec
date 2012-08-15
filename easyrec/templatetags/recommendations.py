from easyrec.utils import get_gateway

from django import template
from django.db.models import get_model

Product = get_model('catalogue', 'Product')
easyrec = get_gateway()

register = template.Library()


def recommendations_to_products(recommendations):
    upcs = []
    if ('recommendeditems' not in recommendations
        or 'item' not in recommendations['recommendeditems']):
        return []

    for item in recommendations['recommendeditems']['item']:
        upcs.append(item['id'])

    return Product.browsable.filter(upc__in=upcs)


@register.assignment_tag
def user_recommendations(user):
    """
    Usage: {% user_recommendations [user] as [var] %}

    Sets [var] to contain a list of recommended titles
    for the passed in user
    """
    recommendations = easyrec.get_user_recommendations(user.user_id)
    return recommendations_to_products(recommendations)


@register.assignment_tag
def users_also_bought(product, user):
    """
    Usage: {% users_also_bought [product] [user] as [var] %}

    Sets [var] to contain a list of products which others who
    have bought [product] have also bought
    """
    try:
        user_id = user.user_id
    except AttributeError:
        user_id = None
    recommendations = easyrec.get_other_users_also_bought(product.upc, user_id)
    return recommendations_to_products(recommendations)


@register.assignment_tag
def users_also_viewed(product, user):
    """
    Usage: {% users_also_viewed [product] [user] as [var] %}

    Sets [var] to contain a list of products which others who
    have viewed [product] have also viewed
    """
    try:
        user_id = user.user_id
    except AttributeError:
        user_id = None

    recommendations = easyrec.get_other_users_also_viewed(product.upc, user_id)
    return recommendations_to_products(recommendations)
