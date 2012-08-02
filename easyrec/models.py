from django.conf import settings

from easyrec.gateway import EasyRec
from easyrec.receivers import EasyRecListeners


easyrec = EasyRec(getattr(settings, 'EASYREC_ENDPOINT',
                  'http://intralife.researchstudio.at'),
                  settings.EASYREC_TENENT_ID,
                  settings.EASYREC_API_KEY)

EasyRecListeners(easyrec).register_listeners()
