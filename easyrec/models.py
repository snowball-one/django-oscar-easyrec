from .receivers import EasyRecListeners
from .utils import get_gateway


easyrec = get_gateway()
listeners = EasyRecListeners(easyrec)
listeners.register_listeners()
