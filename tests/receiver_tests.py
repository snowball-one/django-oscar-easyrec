from unittest import TestCase

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
    return p

def get_mock_request():
    r = Mock()
    r.session = Mock()
    r.session.session_key = '287384' 
    return r

def get_mock_order():
    
    lines = [
        {'product': get_product_mock()},
        {'product': get_product_mock()},
        {'product': get_product_mock()},
    ]
    o = Mock()
    o.line = Mock()
    o.line.all = Mock(return_value=lines)
    return o

def get_mock_review():
    r = Mock();
    r.product = get_product_mock()
    r.user = get_auth_user_mock()
    return r

class EasyRecListenersTest(TestCase):
    
    def setUp(self):
        gateway = EasyRec("http://some.com", 'tenant', 'key')
        gateway._fetch_response = Mock(return_value="{}")
        self.listeners = EasyRecListeners(gateway)
    
    def test_on_product_view(self):
        user = get_auth_user_mock()
        product = get_product_mock()
        request = get_mock_request()
        self.listeners.on_product_view(self, product, user, request)
        
    def test_on_order_placed(self):
        user = get_auth_user_mock()
        order = get_mock_order()
        self.listeners.on_order_placed(self, order, user)
        
    def test_on_review_added(self):
        self.listeners.on_review_added(self, get_mock_review(), True)