from easyrec.receivers import EasyRecListeners
from easyrec.utils import get_gateway

easyrec = get_gateway()
listeners = EasyRecListeners(easyrec)
listeners.register_listeners()
