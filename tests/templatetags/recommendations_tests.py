from unittest import TestCase
from mock import Mock, patch
from django.template import Template, Context
from django_dynamic_fixture import get
from django.db.models import get_model

from easyrec.gateway import EasyRec, DummyRequests


Product = get_model('catalogue','Product')


def get_auth_user_mock():
    u = Mock()
    u.user_id = 1
    u.is_authenticated = Mock(return_value=True)
    return u


def get_product_mock():
    pc = Mock()
    pc.name = 'Product Class'
    p = Mock()
    p.upc = '12345'
    p.get_title = Mock(return_value="Product Title")
    p.images = Mock()
    p.images.count = Mock(return_value=0)
    p.get_absolute_url = Mock(return_value="http://a.test.com/product/prduct-title-12345")
    p.get_product_class.name = "Product Class"
    pclass = Mock()
    pclass.name = 'ITEM'
    p.get_product_class = Mock(return_value=pclass)
    return p


def get_product_list(length=1):
    products = []
    for i in range(length):
        products.append(get_product_mock())
    return products


class RecommendationsTests(TestCase):

    def setUp(self):
        self.product = get(Product, parent=None)
        self.response = {
            'recommendeditems': {
                'item': [
                    {'id': self.product.upc},
                ]
            }
        }
        self.dummy_easyrec = EasyRec("http://DUMMY", '', '')
        self.dummy_easyrec._requests = DummyRequests(self.response)

    def test_recommendations_loads(self):
        with patch('easyrec.utils.get_gateway') as get_gateway:
            get_gateway.return_value = self.dummy_easyrec

            Template(
                '{% load recommendations %}'
            ).render(Context())

    def test_user_recommendations_with_empty_response(self):
        with patch('easyrec.utils.get_gateway') as get_gateway:
            get_gateway.return_value = self.dummy_easyrec

            Template(
                '{% load recommendations %}'
                '{% user_recommendations user as recommendations %}'
            ).render(Context({
                'user': get_auth_user_mock()
            }))

    def test_user_recommendations_with_response(self):
        with patch('easyrec.utils.get_gateway') as get_gateway:
            get_gateway.return_value = self.dummy_easyrec
            rendered =  Template(
                '{% load recommendations %}'
                '{% user_recommendations user as recommendations %}'
                '{% for p in recommendations %}'
                '{{ p.upc }}'
                '{% endfor %}'
            ).render(Context({
                'user': get_auth_user_mock()
            }))
            self.assertEqual(self.product.upc, rendered)
