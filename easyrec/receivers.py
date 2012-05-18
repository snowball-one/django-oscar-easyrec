from itertools import ifilter
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import get_model
from django.conf import settings

from oscar.core.loading import get_class
from easyrec.gateway import EasyRec

product_viewed = get_class('catalogue.signals', 'product_viewed')
order_placed = get_class('order.signals', 'order_placed')
review = get_model('reviews', 'productreview')


easyrec = EasyRec(getattr(settings, 'EASYREC_HOST',
                          'intralife.researchstudio.at'),
                  getattr(settings, 'EASYREC_PORT', 8080),
                  settings.EASYREC_TENENT_ID,
                  settings.EASYREC_API_KEY)


def _has_product(obj):
    try:
        obj.product.upc
    except AttributeError:
        return False
    return True


@receiver(product_viewed)
def receive_product_view(sender, product, user, request, **kwargs):
    image_url = None
    user_id = None
    if user.is_authenticated():
        user_id = user.user_id
    if product.images.count() > 0:
        image_url = product.images.all[0].thumbnail_url

    easyrec.add_view(request.session.session_key,
                    product.upc,
                    product.get_title(),
                    product.get_absolute_url(),
                    product.get_product_class().name,
                    user_id,
                    image_url)


@receiver(order_placed)
def receive_order_placed(sender, order, user, **kwargs):
    session_id = user.user_id # wish I could get the actual session key
    for line in ifilter(_has_product, order.line.all()):
        product = line.product
        image_url = None
        if product.images.count() > 0:
            image_url = product.images.all[0].thumbnail_url
        
        easyrec.add_buy(session_id,
                        product.upc,
                        product.get_title(),
                        product.get_absolute_url(),
                        product.get_product_class().name,
                        user.user_id,
                        image_url)


@receiver(post_save, sender=review)
def review_added(sender, instance, created, **kwargs):
    if created and _has_product(instance):
        user_id = None
        if instance.user and instance.user.is_authenticated():
            user_id = instance.user.user_id
        session_id = 'unknown?'
        product = instance.product
        image_url = None
        if product.images.count() > 0:
            image_url = product.images.all[0].thumbnail_url
        
        easyrec.add_buy(session_id,
                        product.upc,
                        product.get_title(),
                        product.get_absolute_url(),
                        product.get_product_class().name,
                        user_id,
                        image_url)

