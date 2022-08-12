from web3 import Web3 as SourceWeb3
from django.conf import settings
from web3.middleware import geth_poa_middleware

# sys.modules['web3.middleware.validation'] = __import__('newchain_web3_middleware_validation')


def get_web3(rpc_url=None):
    if not rpc_url:
        rpc_url = settings.NEWCHAIN_RPC_URL
    w3 = SourceWeb3(SourceWeb3.HTTPProvider(rpc_url))
    # inject the poa compatibility middleware to the innermost layer
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


class Web3(SourceWeb3):
    """new ton web3"""
    def __init__(self, *args, **kwargs):
        provider = Web3.HTTPProvider(settings.NEWCHAIN_RPC_URL)
        super(Web3, self).__init__(provider, *args, **kwargs)
        self.middleware_onion.inject(geth_poa_middleware, layer=0)

