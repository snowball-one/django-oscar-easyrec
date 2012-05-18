from unittest import TestCase

from mock import Mock

from easyrec.gateway import EasyRec

class GatewayTest(TestCase):
    
    def setUp(self):
        self.gateway = EasyRec("some.com", 8080, 'tenant', 'key')
        self.gateway._fetch_response = Mock(return_value="{}")
    
    def test_base_url_is_checked(self):
        self.assertRaises(RuntimeError, EasyRec, "http://some.com", 8080, 'tenant', 'key')
    
    def test_get_url(self):
        expected = '/api/1.0/json/path'
        url = self.gateway._build_url('path')
        self.assertEqual(expected, url)
        url = self.gateway._build_url('/path')
        self.assertEqual(expected, url)
        url = self.gateway._build_url('path/')
        self.assertEqual(expected, url)
        url = self.gateway._build_url('/path/')
        self.assertEqual(expected, url)
        
    def test_add_view(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'sessionid': 'abc',
            'itemid': 1,
            'itemdescription': 'a description',
            'itemurl': '/book/product-1',
            'itemtype': 'ITEM',
        }
        self.gateway._build_url = Mock()
        self.gateway.add_view('abc', 1, 'a description', '/book/product-1')
        self.gateway._build_url.assert_called_once_with('view', expected_options)
        
    def test_add_buy(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'sessionid': 'abc',
            'itemid': 1,
            'itemdescription': 'a description',
            'itemurl': '/book/product-1',
            'itemtype': 'ITEM',
        }
        self.gateway._build_url = Mock()
        self.gateway.add_buy('abc', 1, 'a description', '/book/product-1')
        self.gateway._build_url.assert_called_once_with('buy', expected_options)
        
    def test_add_rating(self):        
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'sessionid': 'abc',
            'itemid': 1,
            'itemdescription': 'a description',
            'itemurl': '/book/product-1',
            'itemtype': 'ITEM',
            'ratingvalue': 5
        }
        self.gateway._build_url = Mock()
        self.gateway.add_rating('abc', 1, 'a description', '/book/product-1', 5)
        self.gateway._build_url.assert_called_once_with('rate', expected_options)
        
    
        