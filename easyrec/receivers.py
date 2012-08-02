from itertools import ifilter
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import get_model

from oscar.core.loading import get_class


product_viewed = get_class('catalogue.signals', 'product_viewed')
order_placed = get_class('order.signals', 'order_placed')
review = get_model('reviews', 'productreview')


def has_product(obj):
    try:
        obj.product.upc
    except AttributeError:
        return False
    return True


class EasyRecListeners():

    def __init__(self, easyrec):
        self._easyrec = easyrec

    def on_product_view(self, sender, product, user, request, **kwargs):
        image_url = None
        user_id = None
        if user.is_authenticated():
            user_id = user.user_id
        if product.images.count() > 0:
            image_url = product.images.all[0].thumbnail_url

        self._easyrec.add_view(request.session.session_key,
                        product.upc,
                        product.get_title(),
                        product.get_absolute_url(),
                        product.get_product_class().name,
                        user_id,
                        image_url)

    def on_order_placed(self, sender, order, user, **kwargs):
        if order.is_anonymous:
            return

        session_id = order.user.user_id # wish I could get the actual session key
        for line in ifilter(has_product, order.line.all()):
            product = line.product
            image_url = None
            if product.images.count() > 0:
                image_url = product.images.all[0].thumbnail_url

            self._easyrec.add_buy(session_id,
                            product.upc,
                            product.get_title(),
                            product.get_absolute_url(),
                            product.get_product_class().name,
                            order.user.user_id,
                            image_url)

    def on_review_added(self, sender, instance, created, **kwargs):
        if created and has_product(instance):
            user_id = None
            if instance.user and instance.user.is_authenticated():
                user_id = instance.user.user_id
            session_id = 'unknown?'
            product = instance.product
            image_url = None
            if product.images.count() > 0:
                image_url = product.images.all[0].thumbnail_url

            self._easyrec.add_buy(session_id,
                            product.upc,
                            product.get_title(),
                            product.get_absolute_url(),
                            product.get_product_class().name,
                            user_id,
                            image_url)

    def register_listeners(self):
        product_viewed.connect(self.on_product_view, dispatch_uid="easyrec_product_viewed")
        order_placed.connect(self.on_order_placed, dispatch_uid="easyrec_order_placed")
        post_save.connect(self.on_review_added, dispatch_uid="easyrec_review_created", sender=review)
