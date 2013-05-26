from unittest import TestCase
from datetime import datetime

from httpretty import HTTPretty
from httpretty import httprettified
from django_dynamic_fixture import G
from django.db.models.loading import get_model

from easyrec.gateway import EasyRec
from easyrec.errors import EasyRecException

Product = get_model('catalogue', 'Product')


class GatewayTest(TestCase):

    def setUp(self):
        self.gateway = EasyRec("http://some.com", 'tenant', 'key')
        self.maxDiff = 1000

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

    @httprettified
    def test_get_item_types(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        item_types = self.gateway.get_item_types()
        self.assertEqual(item_types, ['ITEM', 'LUBE'])

    @httprettified
    def test_get_item_type(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        item_type = self.gateway._get_item_type('lube')
        self.assertEqual(item_type, 'LUBE')
        item_type = self.gateway._get_item_type('i_do_not_exist')
        self.assertEqual(item_type, 'ITEM')


    @httprettified
    def test_error_raises_exception(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")

        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/view",
                           body='{"error": {"@code": 299, "@message": "Wrong APIKey/Tenant combination!"}}',
                           content_type="application/json")
        params = {
            "session_id": "asession",
            "item_id": 1234,
            "item_desc": "an item",
            "item_url": "http://a-shop.com/items/1234/",
            "item_type":'ITEM',
        }
        try:
            self.gateway.add_view(**params)
        except EasyRecException as e:
            self.assertEqual(e.message, "(299) Wrong APIKey/Tenant combination!")


    @httprettified
    def test_add_view(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")

        params = {
            "session_id": "asession",
            "item_id": 1234,
            "item_desc": "an item",
            "item_url": "http://a-shop.com/items/1234/",
            "item_type":'ITEM',
            "user_id": 123,
            "image_url": "http://a-shop/image.jpg",
            "action_time": datetime.now()
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "sessionid": ["asession"],
            "itemid": ["1234"],
            "itemdescription": ["an item"],
            "itemurl": ["http://a-shop.com/items/1234/"],
            "itemtype": ['ITEM'],
            "userid": ["123"],
            "itemimageurl": ["http://a-shop/image.jpg"],
            "actiontime": [params["action_time"].strftime("%d_%m_%Y_%H_%M_%S")],
        }

        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/view",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")

        self.gateway.add_view(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)

    @httprettified
    def test_add_buy(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")

        params = {
            "session_id": "asession",
            "item_id": 1234,
            "item_desc": "an item",
            "item_url": "http://a-shop.com/items/1234/",
            "item_type":'ITEM',
            "user_id": 123,
            "image_url": "http://a-shop/image.jpg",
            "action_time": datetime.now()
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "sessionid": ["asession"],
            "itemid": ["1234"],
            "itemdescription": ["an item"],
            "itemurl": ["http://a-shop.com/items/1234/"],
            "itemtype": ['ITEM'],
            "userid": ["123"],
            "itemimageurl": ["http://a-shop/image.jpg"],
            "actiontime": [params["action_time"].strftime("%d_%m_%Y_%H_%M_%S")]
        }

        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/buy",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")

        self.gateway.add_buy(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)

    @httprettified
    def test_add_rating(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")

        params = {
            "session_id": "asession",
            "item_id": 1234,
            "item_desc": "an item",
            "item_url": "http://a-shop.com/items/1234/",
            "item_type":'ITEM',
            "rating": 5,
            "user_id": 123,
            "image_url": "http://a-shop/image.jpg",
            "action_time": datetime.now()
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "sessionid": ["asession"],
            "itemid": ["1234"],
            "itemdescription": ["an item"],
            "itemurl": ["http://a-shop.com/items/1234/"],
            "itemtype": ['ITEM'],
            "ratingvalue": ["5"],
            "userid": ["123"],
            "itemimageurl": ["http://a-shop/image.jpg"],
            "actiontime": [params["action_time"].strftime("%d_%m_%Y_%H_%M_%S")]
        }

        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/rate",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")

        self.gateway.add_rating(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)

    @httprettified
    def test_add_action(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")

        params = {
            "session_id": "asession",
            "item_id": 1234,
            "item_desc": "an item",
            "item_url": "http://a-shop.com/items/1234/",
            "item_type":'ITEM',
            "action": "like",
            "user_id": 123,
            "image_url": "http://a-shop/image.jpg",
            "action_time": datetime.now(),
            "value": 7
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "sessionid": ["asession"],
            "itemid": ["1234"],
            "itemdescription": ["an item"],
            "itemurl": ["http://a-shop.com/items/1234/"],
            "itemtype": ['ITEM'],
            "actiontype": ["like"],
            "userid": ["123"],
            "itemimageurl": ["http://a-shop/image.jpg"],
            "actiontime": [params["action_time"].strftime("%d_%m_%Y_%H_%M_%S")],
            "actionvalue": ["7"]
        }

        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/rate",
                           body='{"bob": "hoskin"}',
                           content_type="application/json")

        self.gateway.add_action(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(expected_get_params, get_params)

    @httprettified
    def test_get_user_recommendations(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "user_id": "auser",
            "max_results": 15,
            "requested_item_type": "item",
            "action_type": "view"
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "userid": ["auser"],
            "numberOfResults": ["15"],
            "requesteditemtype": ["ITEM"],
            "actiontype": ["view"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/recommendationsforuser",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_user_recommendations(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_other_users_also_bought(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "user_id": "auser",
            "item_id": 1234,
            "max_results": 10,
            "item_type": "ITEM",
            "requested_item_type": "LUBE"
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "userid": ["auser"],
            "itemid": ["1234"],
            "numberOfResults": ["10"],
            "itemtype": ["ITEM"],
            "requesteditemtype": ["LUBE"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/otherusersalsobought",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_other_users_also_bought(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_other_users_also_viewed(self):
        product = G(Product, parent=None)

        params = {
            "user_id": "auser",
            "item_id": 1234
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "userid": ["auser"],
            "itemid": ["1234"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/otherusersalsoviewed",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_other_users_also_viewed(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_items_rated_as_good_by_other_users(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")

        product = G(Product, parent=None)

        params = {
            "user_id": "auser",
            "item_id": 1234
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "userid": ["auser"],
            "itemid": ["1234"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemsratedgoodbyotherusers",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_items_rated_as_good_by_other_users(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_related_items(self):
        product = G(Product, parent=None)

        params = {
            "item_id": 1234
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "itemid": ["1234"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/relateditems",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_related_items(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_most_viewed_items(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "max_results": 1,
            "requested_item_type": "ITEM",
            "time_range": 'week'
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "numberOfResults": ["1"],
            "requesteditemtype": ["ITEM"],
            "timeRange": ["WEEK"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/mostvieweditems",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_most_viewed_items(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_most_bought_items(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "max_results": 1,
            "requested_item_type": "ITEM",
            "time_range": 'week'
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "numberOfResults": ["1"],
            "requesteditemtype": ["ITEM"],
            "timeRange": ["WEEK"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/mostboughtitems",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_most_bought_items(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_most_rated_items(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "max_results": 1,
            "requested_item_type": "ITEM",
            "time_range": 'week'
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "numberOfResults": ["1"],
            "requesteditemtype": ["ITEM"],
            "timeRange": ["WEEK"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/mostrateditems",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_most_rated_items(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_best_rated_items(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "max_results": 1,
            "requested_item_type": "ITEM",
            "time_range": 'week'
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "numberOfResults": ["1"],
            "requesteditemtype": ["ITEM"],
            "timeRange": ["WEEK"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/bestrateditems",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_best_rated_items(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)

    @httprettified
    def test_get_worst_rated_items(self):
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/itemtypes",
                           body='{"itemTypes": {"itemType": ["ITEM", "LUBE"]}}',
                           content_type="application/json")
        product = G(Product, parent=None)

        params = {
            "max_results": 1,
            "requested_item_type": "ITEM",
            "time_range": 'week'
        }

        expected_get_params = {
            "tenantid": ["tenant"],
            "apikey": ["key"],
            "numberOfResults": ["1"],
            "requesteditemtype": ["ITEM"],
            "timeRange": ["WEEK"]
        }
        expected_response = '{"recommendeditems": {"item": [{"id": %s}]}}' % product.upc
        HTTPretty.register_uri(HTTPretty.GET, "http://some.com/api/1.0/json/worstrateditems",
                           body=expected_response,
                           content_type="application/json")

        response = self.gateway.get_worst_rated_items(**params)
        get_params = HTTPretty.last_request.querystring
        self.assertEqual(get_params, expected_get_params)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]['product'].upc, product.upc)
