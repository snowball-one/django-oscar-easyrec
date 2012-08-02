from unittest import TestCase

from mock import Mock

from easyrec.gateway import EasyRec

class GatewayTest(TestCase):

    def setUp(self):
        self.gateway = EasyRec("http://some.com", 'tenant', 'key')
        self.gateway._fetch_response = Mock(return_value="{}")

    def test_base_url_is_checked(self):
        self.assertRaises(RuntimeError, EasyRec, "some.com", 'tenant', 'key')

    def test_get_url(self):
        expected = 'http://some.com/api/1.0/json/path'
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

    def test_get_user_recommendations(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'userid': 123,
        }
        self.gateway._build_url = Mock()
        self.gateway.get_user_recommendations(123)
        self.gateway._build_url.assert_called_once_with('recommendationsforuser', expected_options)

    def test_get_other_users_also_bought(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'itemid': 54321,
        }
        self.gateway._build_url = Mock()
        self.gateway.get_other_users_also_bought(54321)
        self.gateway._build_url.assert_called_once_with('otherusersalsobought', expected_options)

    def test_get_other_users_also_bought(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'itemid': 54321,
        }
        self.gateway._build_url = Mock()
        self.gateway.get_other_users_also_viewed(54321)
        self.gateway._build_url.assert_called_once_with('otherusersalsoviewed', expected_options)

    def test_related_items(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'itemid': 54321,
        }
        self.gateway._build_url = Mock()
        self.gateway.get_related_items(54321)
        self.gateway._build_url.assert_called_once_with('relateditems', expected_options)
