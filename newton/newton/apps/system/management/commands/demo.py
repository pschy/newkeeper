# -*- coding: utf-8 -*-
__author__ = 'xiawu@xiawu.org'
__version__ = '$Rev$'
__doc__ = """   """

import time
import json
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from utils import ecc_tools, security
from web3 import Web3, HTTPProvider
from eth_abi import encode_abi
from eth_abi.packed import encode_abi_packed
from sha3 import keccak_256
from fastecdsa import curve, ecdsa, keys
from utils import newchain_tools, newton_web3
import rlp
from openid.dh import DiffieHellman
from openid.constants import DEFAULT_DH_GENERATOR, DEFAULT_DH_MODULUS
from openid import cryptutil
from ssl import RAND_bytes
from eth_account import Account as EthAccount
from eth_account.messages import encode_defunct
from key.services import BindParams, GetParams


class Command(BaseCommand):
    args = ''
    help = 'Run test'
    DEFAULT_SYMBOL = ''

    def __init__(self):
        self.rpc = 'https://rpc1.newchain.newtonproject.org'
        self.user = {
            'hex_address': '0x827fc529Ad9FF85c9D127a1161CAfF8F2324e273',
            'new_address': 'NEW17zQFRRuv8hViEqRK3ZpxULGfajYtE1uydaq',
            'private_key': '0xfe57344d5442fef7aadc69406adb5e1641de9a6a5353272c7133eed61b299d03',
        }
        self.ntf_address = '0xFD1d4413030c39758Afd48b34b839BFe265FD9D9'
        self.evt_contract = '0x66fE876AD7C00319aF3030D3736A6D921CDF744B'
        self.api_host = 'http://127.0.0.1:8000/api/v1/'
        super(Command, self).__init__(no_color=True)

    def add_arguments(self, parser):
        parser.add_argument('api', nargs='+', type=str,
                            default=self.DEFAULT_SYMBOL)

    def handle(self, *args, **options):
        api = options['api'][0]
        method = 'api_' + api
        if hasattr(self, method):
            getattr(self, method)()
        else:
            print("...")
    
    def _post(self, url, payload):
        # headers = {'content-type': 'application/json'}
        response = requests.post(url, data=payload)
        print(response, response.text)
        content = response.json()
        response.close()
        del response
        return content

    def api_test(self):
        try:
            print('Step1: mint nft for permission')
            # tokenId = self.mint_nft()
            # if tokenId < 0:
            #     print('mint nft error')
            #     return
            # else:
            #     print('mint nft tokenId: %s' % str(tokenId))

            print()
            print('Step2: call api for swap key')
            api_url = self.api_host + 'key/generator'
            g = DEFAULT_DH_GENERATOR
            p_number = int.from_bytes(RAND_bytes(66), byteorder='big')
            p = cryptutil.longToBase64(p_number)
            dh_client = DiffieHellman(p, g)
            client_public_key = dh_client.public_key
            payload = {
                'prime': p,
                'peer_swap_key': client_public_key
            }
            resp = self._post(api_url, payload)
            if resp['error_code'] == 1:
                server_public_key = resp['result']['node_swap_key']
                print('node_swap_key: %s' % server_public_key)
            else:
                print('swap key failed')
                return

            keyId = security.generate_digest_sha256(client_public_key)
            print('keyId: %s' % keyId)
            shared_secret = dh_client.getSharedSecret(server_public_key)
            shared_secret = hex(shared_secret)
            # server_secret = cryptutil.longToBase64(server_secret)
            print('shared_secret: %s' % shared_secret)
            print()
            
            print('Step3: mint evt and register and add permisson')
            evtTokenId = self.evt_oper(keyId)
            print()
            time.sleep(3)

            print('Step4: call bind api')
            encrypt_key = 'd41d8cd98f00b204e9800998ecf8427e'
            a = EthAccount.from_key(self.user['private_key'])
            wallet_address = a.address
            print('wallet_address:', wallet_address)

            rpc_url = 'https://rpc1.newchain.newtonproject.org/'
            w3 = newton_web3.get_web3(rpc_url)
            message = 'asdf23fef34t45t54dfsfsd'
            signable_message = encode_defunct(text=message)
            signed_message = w3.eth.account.sign_message(signable_message, private_key=self.user['private_key'])

            private_key = security.aes_encrypt(shared_secret[2:32], encrypt_key)
            bindParams = BindParams(
                key_id=bytes(keyId, encoding='utf-8'),
                r=signed_message.r,
                s=signed_message.s,
                v=signed_message.v,
                private_key=bytes(private_key, encoding='utf-8'),
                message=bytes(message, encoding='utf-8'),
                contract_address=bytes('0x66fE876AD7C00319aF3030D3736A6D921CDF744B', encoding='utf-8'),
                nft_contract_address=bytes('0xFD1d4413030c39758Afd48b34b839BFe265FD9D9', encoding='utf-8'),
                rpc_url=bytes(rpc_url, encoding='utf-8'),
                token_id=evtTokenId,
                chain_id=1007
            )
            sign_data = w3.toHex(rlp.encode(bindParams, BindParams))
            print('bind sign_data: %s' % sign_data)
            payload = {
                'sign_data': sign_data
            }
            api_url = self.api_host + 'key/bind'
            resp = self._post(api_url, payload)
            if resp['error_code'] == 1:
                print('bind key success')
                print()
            else:
                print('bind key failed')
                return

            print('Step5: get encrypt key')
            message = 'abcdefgjkqwerrttyuio'
            signable_message = encode_defunct(text=message)
            signed_message = w3.eth.account.sign_message(signable_message, private_key=self.user['private_key'])
            p_number = int.from_bytes(RAND_bytes(66), byteorder='big')
            prime = cryptutil.longToBase64(p_number)
            dh_client = DiffieHellman(prime, g)
            peer_swap_key = dh_client.public_key
            getParams = GetParams(
                key_id=bytes(keyId, encoding='utf-8'),
                r=signed_message.r,
                s=signed_message.s,
                v=signed_message.v,
                message=bytes(message, encoding='utf-8'),
                prime=bytes(prime, encoding='utf-8'),
                peer_swap_key=bytes(peer_swap_key, encoding='utf-8')
            )
            sign_data = w3.toHex(rlp.encode(getParams, GetParams))
            print('get sign_data: %s' % sign_data)
            payload = {
                'sign_data': sign_data
            }
            api_url = self.api_host + 'key/'
            resp = self._post(api_url, payload)
            print('resp:', resp)
            if resp['error_code'] == 1:
                server_public_key = resp['result']['node_swap_key']
                private_key = resp['result']['private_key']
            else:
                print('get key failed')
                return
            shared_secret = dh_client.getSharedSecret(server_public_key)
            shared_secret = hex(shared_secret)
            encrypt_key = security.aes_decrypt(shared_secret[2:32], private_key)
            print('encrypt_key: %s' % encrypt_key)
        except Exception as e:
            print("error: %s" % str(e))

    def mint_nft(self):
        try:
            w3 = Web3(HTTPProvider(self.rpc))
            ClientVersion = int(w3.net.version)
            w3.eth.account.chain_id = ClientVersion
            from_address = w3.toChecksumAddress(self.user['hex_address'])
            Account = w3.eth.account.privateKeyToAccount(self.user['private_key'])

            with open('contracts/Nft.json', 'rb') as f:
                nft_json = json.load(f)
            nft_address = w3.toChecksumAddress(self.ntf_address)
            nft_contract = w3.eth.contract(address=nft_address, abi=nft_json)

            to = from_address
            nonce = w3.eth.getTransactionCount(from_address)
            transaction = {
                'from': from_address,
                'gasPrice': w3.eth.gasPrice,
                'chainId': ClientVersion,
                'nonce': nonce,
                'value': w3.toWei(100, 'ether'),
            }
            gas = nft_contract.functions.safeMint(to).estimateGas(transaction)
            transaction['gas'] = gas
            tx = nft_contract.functions.safeMint(to).buildTransaction(transaction)
            signed_txn = Account.signTransaction(tx)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_hash = tx_hash.hex()
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            logs = nft_contract.events.Transfer().processReceipt(tx_receipt)
            token_id = -1
            if logs:
                for log in logs:
                    if log['event'] == 'Transfer':
                        token_id = log.args['tokenId']
                        break
            return token_id
        except Exception as e:
            print("error: %s" % str(e))

    def evt_oper(self, keyId):
        try:
            w3 = Web3(HTTPProvider(self.rpc))
            ClientVersion = int(w3.net.version)
            w3.eth.account.chain_id = ClientVersion
            from_address = w3.toChecksumAddress(self.user['hex_address'])
            Account = w3.eth.account.privateKeyToAccount(self.user['private_key'])

            with open('contracts/Encryption.json', 'rb') as f:
                encrypt_json = json.load(f)
            evt_address = w3.toChecksumAddress(self.evt_contract)
            evt_contract = w3.eth.contract(address=evt_address, abi=encrypt_json)

            nonce = w3.eth.getTransactionCount(from_address)
            transaction = {
                'from': from_address,
                'gasPrice': w3.eth.gasPrice,
                'chainId': ClientVersion,
                'nonce': nonce,
            }
            gas = evt_contract.functions.mint(from_address).estimateGas(transaction)
            transaction['gas'] = gas
            tx = evt_contract.functions.mint(from_address).buildTransaction(transaction)
            signed_txn = Account.signTransaction(tx)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_hash = tx_hash.hex()
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            logs = evt_contract.events.Transfer().processReceipt(tx_receipt)
            print('mint evt logs:')
            print(str(logs))
            evtTokenId = -1
            if logs:
                for log in logs:
                    if log['event'] == 'Transfer':
                        evtTokenId = log.args['tokenId']
                        break
            if evtTokenId < 0:
                print('mint evt error')
                return False
            print('evtTokenId: %s' % evtTokenId)

            # register
            enkeyId = bytes.fromhex(keyId)
            nonce = w3.eth.getTransactionCount(from_address)
            transaction = {
                'from': from_address,
                'gasPrice': w3.eth.gasPrice,
                'chainId': ClientVersion,
                'nonce': nonce,
            }
            gas = evt_contract.functions.registerEncryptedKey(evtTokenId, enkeyId).estimateGas(transaction)
            transaction['gas'] = gas
            tx = evt_contract.functions.registerEncryptedKey(evtTokenId, enkeyId).buildTransaction(transaction)
            signed_txn = Account.signTransaction(tx)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_hash = tx_hash.hex()
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print('registerEncryptedKey tx_receipt:')
            print(tx_receipt)
            
            # add permission
            nonce = w3.eth.getTransactionCount(from_address)
            transaction = {
                'from': from_address,
                'gasPrice': w3.eth.gasPrice,
                'chainId': ClientVersion,
                'nonce': nonce,
            }
            gas = evt_contract.functions.addPermission(evtTokenId, enkeyId, from_address).estimateGas(transaction)
            transaction['gas'] = gas
            tx = evt_contract.functions.addPermission(evtTokenId, enkeyId, from_address).buildTransaction(transaction)
            signed_txn = Account.signTransaction(tx)
            tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_hash = tx_hash.hex()
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print('addPermission tx_receipt:')
            print(tx_receipt)

            return evtTokenId
        except Exception as e:
            print("error: %s" % str(e))

    def api_evt_check(self):
        try:
            w3 = Web3(HTTPProvider(self.rpc))
            ClientVersion = int(w3.net.version)
            w3.eth.account.chain_id = ClientVersion
            from_address = w3.toChecksumAddress(self.user['hex_address'])
            print('from_address:', from_address)

            with open('contracts/Encryption.json', 'rb') as f:
                base_token_json = json.load(f)
            evt_address = w3.toChecksumAddress(self.evt_contract)
            evt_contract = w3.eth.contract(address=evt_address, abi=base_token_json)

            keyId = '220ea6ed90f699d95595b529c49ed398256b4b0cbadf614e4d0880deb96d5911'
            tokenId = 2
            res = evt_contract.functions.hasPermission(tokenId, keyId, from_address).call()
            print(res)
        except Exception as e:
            print("error: %s" % str(e))
