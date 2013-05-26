from unittest import TestCase
from mock import Mock
from json import dumps

from django.template import Template, Context
from django_dynamic_fixture import G
from django.db.models import get_model

from httpretty import HTTPretty
from httpretty import httprettified


Product = get_model('catalogue','Product')


def get_auth_user_mock():
    u = Mock()
    u.user_id = 1
    u.is_authenticated = Mock(return_value=True)
    return u


def get_product_list(length=1):
    products = []
    for i in range(length):
        products.append(G(Product))
    return products


class RankingsTest(TestCase):

    def setUp(self):
        self.product = G(Product, parent=None)
        self.recommendations = dumps({
            'recommendeditems': {
                'item': [
                    {'id': self.product.upc},
                ]
            }
        })

    def test_rankings_loads(self):
        Template(
            '{% load rankings %}'
        ).render(Context())
        self.assertTrue(True)

    @httprettified
    def test_most_viewed(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/mostvieweditems",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load rankings %}'
            '{% most_viewed as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context())
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_most_bought(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/mostboughtitems",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load rankings %}'
            '{% most_bought as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context())
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_most_rated(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/mostrateditems",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load rankings %}'
            '{% most_rated as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context())
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_best_rated(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/bestrateditems",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load rankings %}'
            '{% best_rated as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context())
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_worst_rated(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/worstrateditems",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load rankings %}'
            '{% worst_rated as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context())
        self.assertEqual(self.product.upc, rendered)
