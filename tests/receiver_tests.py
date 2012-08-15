from unittest import TestCase
from datetime import datetime

from mock import Mock

from easyrec.gateway import EasyRec
from easyrec.receivers import EasyRecListeners


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

def get_mock_request():
    r = Mock()
    r.session = Mock()
    r.session.session_key = '287384'
    return r

def get_mock_order():

    lines = []
    for i in range(3):
        line = Mock()
        line.product = get_product_mock()
        lines.append(line)

    o = Mock()
    o.line = Mock()
    o.line.all = Mock(return_value=lines)
    o.user = get_auth_user_mock()
    o.is_anonymous = False
    o.date_placed = datetime.fromtimestamp(100)
    return o

def get_mock_review():
    r = Mock();
    r.product = get_product_mock()
    r.user = get_auth_user_mock()
    r.score = 4
    r.date_placed = datetime.fromtimestamp(100)
    return r

class EasyRecListenersTest(TestCase):

    def setUp(self):
        self.gateway = EasyRec("http://some.com", 'tenant', 'key')
        self.gateway._fetch_response = Mock(return_value="{}")
        self.listeners = EasyRecListeners(self.gateway)

    def test_on_product_view(self):

        expected  = {
            'itemid': '12345',
            'apikey': 'key',
            'itemtype': 'ITEM',
            'userid': 1,
            'itemdescription': 'Product Title',
            'itemurl': 'http://a.test.com/product/prduct-title-12345',
            'sessionid': '287384',
            'tenantid': 'tenant'
        }
        user = get_auth_user_mock()
        product = get_product_mock()
        request = get_mock_request()
        self.gateway._fetch_response = Mock()
        self.listeners.on_product_view(self, product, user, request)
        self.gateway._fetch_response.assert_called_with('http://some.com/api/1.0/json/view', params=expected)

    def test_on_order_placed(self):
        expected = {
            'itemid': '12345',
            'apikey': 'key',
            'itemtype': 'ITEM',
            'userid': 1,
            'itemdescription': 'Product Title',
            'itemurl': 'http://a.test.com/product/prduct-title-12345',
            'sessionid': 1,
            'actiontime': '01_01_1970_10_01_40',
            'tenantid': 'tenant'
        }
        user = get_auth_user_mock()
        order = get_mock_order()
        self.gateway._fetch_response = Mock()
        self.listeners.on_order_placed(self, order, user)
        self.gateway._fetch_response.assert_called_with('http://some.com/api/1.0/json/buy', params=expected)

    def test_on_review_added(self):
        expected = {
            'itemid': '12345',
            'sessionid': 1,
            'apikey': 'key',
            'itemtype': 'ITEM',
            'ratingvalue': 4,
            'itemurl': 'http://a.test.com/product/prduct-title-12345',
            'userid': 1, 'itemdescription': 'Product Title',
            'tenantid': 'tenant',
            'actiontime': '01_01_1970_10_01_40',
        }
        self.gateway._fetch_response = Mock()
        self.listeners.on_review_added(self, get_mock_review(), True)
        self.gateway._fetch_response.assert_called_with('http://some.com/api/1.0/json/rate', params=expected)
