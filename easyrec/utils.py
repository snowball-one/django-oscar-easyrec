from django.conf import settings

from easyrec.gateway import EasyRec, DummyRequests


def get_gateway():
    endpoint = getattr(settings, 'EASYREC_ENDPOINT',
                      'http://intralife.researchstudio.at/easyrec-web')

    if 'DUMMY' == endpoint:
        easyrec = EasyRec("http://DUMMY", '', '')
        easyrec._requests = DummyRequests()
        return easyrec

    tenant_id = settings.EASYREC_TENANT_ID
    api_key = settings.EASYREC_API_KEY
    return EasyRec(endpoint, tenant_id, api_key)
