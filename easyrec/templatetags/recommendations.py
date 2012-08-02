from easyrec.models import easyrec

from django import template
from django.db.models import get_model

Product = get_model('catalogue','Product')

register = template.Library()


def recommendations_to_products(recommendations):
    upcs = []

    if 'recommendeditems' not in recommendations or
        'item' not in recommendations['recommendeditems']:
        return []

    for item in recommendations['recommendeditems']['item']:
        upcs.append(item['id'])

    return Product.browsable.filter('upc__in'=upcs)

@register.assignment_tag(name=user_recommendations)
def user_recommendations(user):
    """
    Usage: {% user_recommendations [user] as [var] %}

    Sets [var] to contain a list of recommended titles
    for the passed in user
    """
    recommendations = easyrec.get_user_recommendations(user.user_id)
    return recommendations_to_products(recommendations)

@register.assignment_tag(name=users_also_bought)
def users_also_bought(product, user=None):
    """
    Usage: {% users_also_bought [product] [user] as [var] %}

    Sets [var] to contain a list of products which others who
    have bought [product] have also bought
    """
    user_id = None
    if user:
        user_id = user.user_id

    recommendations = easyrec.get_other_users_also_bought(product.upc, user_id)
    return recommendations_to_products(recommendations)

@register.assignment_tag(name=users_also_viewed)
def users_also_viewed(product, user=None):
    """
    Usage: {% users_also_viewed [product] [user] as [var] %}

    Sets [var] to contain a list of products which others who
    have viewed [product] have also viewed
    """
    user_id = None
    if user:
        user_id = user.user_id

    recommendations = easyrec.get_other_users_also_viewed(product.upc, user_id)
    return recommendations_to_products(recommendations)
