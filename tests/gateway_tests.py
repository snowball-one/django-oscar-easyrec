from mock import Mock, patch
from unittest import TestCase
from json import loads


from easyrec.gateway import EasyRec


class MockedResponseTestCase(TestCase):

    def create_mock_response(self, body, status_code=200, is_json=False):
        response = Mock()
        response.content = body
        response.text = body
        response.json = None
        if is_json:
            response.json = loads(body)
        response.status_code = status_code
        return response


class GatewayTest(MockedResponseTestCase):

    def setUp(self):
        self.gateway = EasyRec("http://some.com", 'tenant', 'key')
        self.gateway._fetch_response = Mock(return_value="{}")
        self.gateway._build_url = Mock(return_value="http://a_test.com")

    def test_base_url_is_checked(self):
        self.assertRaises(RuntimeError, EasyRec, "some.com", 'tenant', 'key')

    def test_get_url(self):
        expected = 'http://some.com/api/1.0/json/path'
        gateway = EasyRec("http://some.com", 'tenant', 'key')
        url = gateway._build_url('path')
        self.assertEqual(expected, url)
        url = gateway._build_url('/path')
        self.assertEqual(expected, url)
        url = gateway._build_url('path/')
        self.assertEqual(expected, url)
        url = gateway._build_url('/path/')
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
        self.gateway.add_view('abc', 1, 'a description', '/book/product-1')
        self.gateway._build_url.assert_called_once_with('view')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

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
        self.gateway.add_buy('abc', 1, 'a description', '/book/product-1')
        self.gateway._build_url.assert_called_once_with('buy')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

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
        self.gateway.add_rating('abc', 1, 'a description', '/book/product-1', 5)
        self.gateway._build_url.assert_called_once_with('rate')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

    def test_get_user_recommendations(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'userid': 123,
        }
        self.gateway.get_user_recommendations(123)
        self.gateway._build_url.assert_called_once_with('recommendationsforuser')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

    def test_get_other_users_also_bought(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'itemid': 54321,
        }
        self.gateway.get_other_users_also_bought(54321)
        self.gateway._build_url.assert_called_once_with('otherusersalsobought')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

    def test_get_other_users_also_viewed(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'itemid': 54321,
        }
        self.gateway.get_other_users_also_viewed(54321)
        self.gateway._build_url.assert_called_once_with('otherusersalsoviewed')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

    def test_related_items(self):
        expected_options = {
            'apikey': 'key',
            'tenantid': 'tenant',
            'itemid': 54321,
        }
        self.gateway.get_related_items(54321)
        self.gateway._build_url.assert_called_once_with('relateditems')
        self.gateway._fetch_response.assert_called_once_with('http://a_test.com', params=expected_options)

    def test_fetch_response_for_posting(self):

        gateway = EasyRec("http://some.com", 'tenant', 'key')

        with patch('requests.post') as post:
            post.return_value = self.create_mock_response('{"bob": "hoskins"}', is_json=True)
            url = "http://a_site.com"
            method = 'POST'
            params = {'A': 'B'}

            response = gateway._fetch_response(url, method, params);
            post.assert_called_with(url, params=params)

