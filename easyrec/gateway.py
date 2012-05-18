import urllib
import httplib
import json


class EasyRec():

    _base_url = "/api/1.0/json/"

    def __init__(self, host, port, tenant, api_key):
        if host.startswith('http'):
            raise RuntimeError("EASYREC_HOST should not include the http")
        self._host = host
        self._port = port
        self._tenant = tenant
        self._api_key = api_key

    def add_view(self, session_id, item_id, item_desc, item_url,
                 item_type='ITEM', user_id=None, image_url=None,
                 action_time=None):
        options = {
            'apikey': self._api_key,
            'tenantid': self._tenant,
            'sessionid': session_id,
            'itemid': item_id,
            'itemdescription': item_desc,
            'itemurl': item_url,
            'itemtype': item_type
        }
        if user_id:
            options['userid'] = user_id

        if image_url:
            options['imageurl'] = image_url

        if action_time:
            options['actiontime'] = action_time

        url = self._build_url('view', options)
        return self._fetch_response(url)

    def add_buy(self, session_id, item_id, item_desc, item_url,
                item_type='ITEM', user_id=None, image_url=None,
                action_time=None):
        options = {
            'apikey': self._api_key,
            'tenantid': self._tenant,
            'sessionid': session_id,
            'itemid': item_id,
            'itemdescription': item_desc,
            'itemurl': item_url,
            'itemtype': item_type
        }
        if user_id:
            options['userid'] = user_id

        if image_url:
            options['imageurl'] = image_url

        if action_time:
            options['actiontime'] = action_time

        url = self._build_url('buy', options)
        return self._fetch_response(url)

    def add_rating(self, session_id, item_id, item_desc, item_url, rating,
                   item_type='ITEM',  user_id=None, image_url=None,
                   action_time=None):
        options = {
            'apikey': self._api_key,
            'tenantid': self._tenant,
            'sessionid': session_id,
            'itemid': item_id,
            'itemdescription': item_desc,
            'itemurl': item_url,
            'itemtype': item_type,
            'ratingvalue': rating,
        }
        if user_id:
            options['userid'] = user_id

        if image_url:
            options['imageurl'] = image_url

        if action_time:
            options['actiontime'] = action_time

        url = self._build_url('rate', options)
        return self._fetch_response(url)

    def _build_url(self, path, options=None):
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        url = "%s%s" % (self._base_url, path)

        if options:
            url = (url, urllib.urlencode(options)).join('?')
        return url

    def _fetch_response(self, url, method="GET"):
        conn = httplib.HTTPSConnection(self._host, self._port, timeout=30)
        conn.request(method, url)
        response = conn.getresponse()
        raw_response = response.read()
        if response.status != httplib.OK:
            raise RuntimeError("Unable to communicate with easyrec (code: %s, response: %s)" % (response.status, raw_response))
        conn.close()
        return json.loads(raw_response)
