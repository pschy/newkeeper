from web3 import Web3 as SourceWeb3
from django.conf import settings
from web3.middleware import geth_poa_middleware
import json
import requests

# sys.modules['web3.middleware.validation'] = __import__('newchain_web3_middleware_validation')


def get_web3(rpc_url):
    w3 = SourceWeb3(SourceWeb3.HTTPProvider(rpc_url))
    # inject the poa compatibility middleware to the innermost layer
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


def get_contracts_balance(rpc_url, wallet_address, contract_address):
    wallet_address = wallet_address.lower()
    w3 = get_web3(rpc_url)
    func_sign = w3.keccak(text='balanceOf(address)').hex()
    func = func_sign[0:10] + "000000000000000000000000" + wallet_address[2:]

    contract_address = contract_address.lower()
    payload = {
        "jsonrpc": "2.0",
        "id": contract_address,
        "method": "eth_call",
        "params": [{'to': contract_address, 'data': func}, "latest"]
    }
    data = _post_call(rpc_url, payload)
    balance = 0
    if data:
        if 'result' in data and data['result'] != '0x':
            balance = int(data['result'], 16)
    return balance


def _post_call(url, payload):
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    content = response.json()
    response.close()
    del response
    return content


def has_permission(rpc_url, wallet_address, token_id, key_id, contract_address):
    wallet_address = wallet_address.lower()
    w3 = get_web3(rpc_url)
    func_sign = w3.keccak(text='hasPermission(uint256,bytes32,address)').hex()
    func = func_sign[0:10]
    token_id_hex = w3.toHex(token_id)[2:]
    func = func + token_id_hex.zfill(64)
    func = func + key_id
    func = func + wallet_address[2:].zfill(64)

    print('func:', func)
    contract_address = contract_address.lower()
    payload = {
        "jsonrpc": "2.0",
        "id": contract_address,
        "method": "eth_call",
        "params": [{'to': contract_address, 'data': func}, "latest"]
    }
    data = _post_call(rpc_url, payload)
    print('permission:', data)
    has_permission = False
    if data:
        if 'result' in data and data['result'] != '0x':
            result = int(data['result'], 16)
            if result == 1:
                has_permission = True
    return has_permission
