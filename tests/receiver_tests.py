from unittest import TestCase
from datetime import datetime

from httpretty import HTTPretty
from httpretty import httprettified
from django_dynamic_fixture import G
from mock import Mock

from easyrec.gateway import EasyRec
from easyrec.receivers import EasyRecListeners

def get_auth_user_mock():
    u = Mock()
    u.id = 1
    u.is_authenticated = Mock(return_value=True)
    return u

def get_product_mock():
    pc = Mock()
    pc.name = 'Product Class'
    p = Mock()
    p.upc = '12345'
    p.get_title = Mock(return_value="Product Title")
    p.images = Mock()
    p.images.count = Mock(return_value=1)
    image = Mock()
    image.thumbnail_url ="http://a.test.com/images/12345.jpg"
    images = [
        image
    ]
    p.images.all = Mock(return_value=images)
    p.get_absolute_url = Mock(return_value="http://a.test.com/product/product-title-12345")
    p.get_product_class.name = "Product Class"
    pclass = Mock()
    pclass.name = 'ITEM'
    p.get_product_class = Mock(return_value=pclass)

    return p

def get_mock_request():
    r = Mock()
    r.session = Mock()
    r.session.session_key = '287384'
    r.build_absolute_uri = lambda x: x
    return r

def get_mock_order():

    lines = []
    for i in range(3):
        line = Mock()
        line.product = get_product_mock()
        line.quantity = 1
        lines.append(line)

    o = Mock()
    o.lines = Mock()
    o.lines.all = Mock(return_value=lines)
    o.user = get_auth_user_mock()
    o.is_anonymous = False
    o.date_placed = datetime.utcfromtimestamp(100)
    return o

def get_mock_review():
    r = Mock();
    r.product = get_product_mock()
    r.user = get_auth_user_mock()
    r.score = 4
    r.date_created = datetime.utcfromtimestamp(100)
    return r


class EasyRecListenersTest(TestCase):

    def setUp(self):
        self.gateway = EasyRec("http://some.com", 'tenant', 'key')
        self.listeners = EasyRecListeners(self.gateway)
        self.maxDiff=1000

    @httprettified
    def test_on_product_view(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/view",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")

        user = get_auth_user_mock()
        product = get_product_mock()
        request = get_mock_request()

        expected  = {
            'itemid': ['12345'],
            'apikey': ['key'],
            'itemtype': ['ITEM'],
            'userid': ["1"],
            'itemdescription': ['Product Title'],
            'itemurl': ['http://a.test.com/product/product-title-12345'],
            'sessionid': ['287384'],
            'tenantid': ['tenant'],
            'itemimageurl': ['http://a.test.com/images/12345.jpg']
        }

        self.listeners.on_product_view(self, product, user, request)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected)

    @httprettified
    def test_on_post_checkout(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/buy",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")
        user = get_auth_user_mock()
        order = get_mock_order()
        request = get_mock_request()

        expected = {
            'itemid': ['12345'],
            'apikey': ['key'],
            'itemtype': ['ITEM'],
            'userid': ["1"],
            'itemdescription': ['Product Title'],
            'itemurl': ['http://a.test.com/product/product-title-12345'],
            'sessionid': ['287384'],
            'actiontime': ['01_01_1970_00_01_40'],
            'tenantid': ['tenant'],
            'itemimageurl': ['http://a.test.com/images/12345.jpg']
        }


        self.listeners.on_post_checkout(self, order, user, request, None)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected)

    @httprettified
    def test_on_review_added(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM"]}}',
                           content_type="application/json")
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/rate",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")

        expected = {
            'itemid': ['12345'],
            'apikey': ['key'],
            'itemtype': ['ITEM'],
            'userid': ["1"],
            'itemdescription': ['Product Title'],
            'itemurl': ['http://a.test.com/product/product-title-12345'],
            'sessionid': ['287384'],
            'actiontime': ['01_01_1970_00_01_40'],
            'tenantid': ['tenant'],
            'ratingvalue': ['4'],
            'itemimageurl': ['http://a.test.com/images/12345.jpg']
        }

        user = get_auth_user_mock()
        review = get_mock_review()
        request = get_mock_request()
        self.listeners.on_review_added(self, review, user, request)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected)
