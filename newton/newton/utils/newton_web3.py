from web3 import Web3 as SourceWeb3
from django.conf import settings
from web3.middleware import geth_poa_middleware

# sys.modules['web3.middleware.validation'] = __import__('newchain_web3_middleware_validation')


def get_web3(chain_id=1007):
    if chain_id not in settings.CHAIN_ID:
        return False
    rpc_url = settings.RPC_URL[chain_id]
    w3 = SourceWeb3(SourceWeb3.HTTPProvider(rpc_url))
    # inject the poa compatibility middleware to the innermost layer
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3
