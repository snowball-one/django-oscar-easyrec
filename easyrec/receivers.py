from itertools import ifilter

from oscar.core.loading import get_class


product_viewed = get_class('catalogue.signals', 'product_viewed')
post_checkout = get_class('checkout.signals', 'post_checkout')
review_added = get_class('catalogue.reviews.signals', 'review_added')


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
            user_id = user.id
        images = product.images.all()[:1]
        if len(images) > 0:
            image_url = images[0].thumbnail_url
            image_url = self._get_full_url(request, image_url)

        product_url = self._get_full_url(request, product.get_absolute_url())
        self._easyrec.add_view(request.session.session_key,
                               product.upc,
                               product.get_title(),
                               product_url,
                               product.get_product_class().name,
                               user_id,
                               image_url)

    def on_post_checkout(self, sender, order, user, request, response, **kwargs):
        user_id = None
        if user.is_authenticated():
            user_id = user.id
        for line in ifilter(has_product, order.lines.all()):
            product = line.product
            image_url = None
            images = product.images.all()[:1]
            if len(images) > 0:
                image_url = images[0].thumbnail_url
                image_url = self._get_full_url(request, image_url)

            product_url = self._get_full_url(
              request,
              product.get_absolute_url()
            )
            for n in range(line.quantity):
                self._easyrec.add_buy(request.session.session_key,
                                      product.upc,
                                      product.get_title(),
                                      product_url,
                                      product.get_product_class().name,
                                      user_id,
                                      image_url,
                                      order.date_placed)

    def on_review_added(self, sender, instance, user, request, response, **kwargs):
        if has_product(instance):
            user_id = None
            if user.is_authenticated():
                user_id = instance.user.id

            rating = instance.score
            product = instance.product
            image_url = None
            images = product.images.all()[:1]
            if len(images) > 0:
                image_url = images[0].thumbnail_url
                image_url = self._get_full_url(request, image_url)
            product_url = self._get_full_url(
              request,
              product.get_absolute_url()
            )
            self._easyrec.add_rating(request.session.session_key,
                                     product.upc,
                                     product.get_title(),
                                     product_url,
                                     rating,
                                     product.get_product_class().name,
                                     user_id,
                                     image_url,
                                     instance.date_created)

    def register_listeners(self):
        product_viewed.connect(self.on_product_view,
                               dispatch_uid="easyrec_product_viewed")
        post_checkout.connect(self.on_post_checkout,
                             dispatch_uid="easyrec_order_placed")
        review_added.connect(self.on_review_added,
                          dispatch_uid="easyrec_review_created")

    def _get_full_url(self, request, url):
      return request.build_absolute_uri(url)
