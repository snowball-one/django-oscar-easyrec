from django.conf import settings


from .gateway import EasyRec, DummyRequests


def get_gateway():
    endpoint = getattr(settings, 'EASYREC_ENDPOINT',
                      'http://intralife.researchstudio.at/easyrec-web')

    if 'DUMMY' == endpoint:
        easyrec = EasyRec("http://DUMMY", '', '')
        easyrec._requests = DummyRequests()
    else:
        tenant_id = settings.EASYREC_TENANT_ID
        api_key = settings.EASYREC_API_KEY
        easyrec = EasyRec(endpoint, tenant_id, api_key)

    return easyrec
