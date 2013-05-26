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


class RecommendationsTests(TestCase):

    def setUp(self):
        self.product = G(Product, parent=None)
        self.recommendations = dumps({
            'recommendeditems': {
                'item': [
                    {'id': self.product.upc},
                ]
            }
        })

    def test_recommendations_loads(self):
        Template(
            '{% load recommendations %}'
        ).render(Context())
        self.assertTrue(True)

    @httprettified
    def test_user_recommendations_with_empty_response(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/recommendationsforuser",
                           body='{"b": "b"}',
                           content_type="application/json")

        rendered = Template(
            '{% load recommendations %}'
            '{% user_recommendations user as recommendations %}'
        ).render(Context({
            'user': get_auth_user_mock()
        }))
        self.assertEqual('', rendered)

    @httprettified
    def test_user_recommendations_with_response(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/recommendationsforuser",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load recommendations %}'
            '{% user_recommendations user as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context({
            'user': get_auth_user_mock()
        }))
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_products_rated_good(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/itemsratedgoodbyotherusers",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load recommendations %}'
            '{% products_rated_good product user as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context({
            'product': G(Product),
            'user': get_auth_user_mock()
        }))
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_related_products(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/relateditems",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load recommendations %}'
            '{% related_products product user as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context({
            'product': G(Product),
            'user': get_auth_user_mock()
        }))
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_users_also_viewed(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/otherusersalsoviewed",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load recommendations %}'
            '{% users_also_viewed product user as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context({
            'product': G(Product),
            'user': get_auth_user_mock()
        }))
        self.assertEqual(self.product.upc, rendered)

    @httprettified
    def test_users_also_bought(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://easyrec-test.com/api/1.0/json/otherusersalsobought",
                           body=self.recommendations,
                           content_type="application/json")
        rendered =  Template(
            '{% load recommendations %}'
            '{% users_also_bought product user as recommendations %}'
            '{% for r in recommendations %}'
            '{{ r.product.upc }}'
            '{% endfor %}'
        ).render(Context({
            'product': G(Product),
            'user': get_auth_user_mock()
        }))
        self.assertEqual(self.product.upc, rendered)
