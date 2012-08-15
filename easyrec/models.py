from easyrec.receivers import EasyRecListeners
from easyrec.utils import get_gateway


easyrec = get_gateway()
EasyRecListeners(easyrec).register_listeners()
