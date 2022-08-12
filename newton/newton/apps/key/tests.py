from django.test import TestCase

# Create your tests here.
import random
import time
from openid.dh import DiffieHellman
from openid.constants import DEFAULT_DH_GENERATOR, DEFAULT_DH_MODULUS
from openid import cryptutil
from django.conf import settings
from utils import security
from ssl import RAND_bytes


class SecretTestCase(TestCase):
    def setUp(self):
        pass

    def test_generate(self):
        # prime_number = int.from_bytes(RAND_bytes(128), byteorder='big')
        prime = DEFAULT_DH_MODULUS

        dh_client = DiffieHellman(prime, DEFAULT_DH_GENERATOR)
        client_public_key = dh_client.public_key
        data = {
            'prime': prime,
            'public_key': client_public_key,
        }
        # 从配置文件的 APP_KEY_TO_SECRET 中随机抽取一个
        keys = random.sample(settings.APP_KEY_TO_SECRET.keys(), 1)
        app_key = keys[0]
        print("app_key: %s" % app_key)
        app_secret = settings.APP_KEY_TO_SECRET[app_key]
        data.update({
            'app_key': app_key,
            'timestamp': time.time(),
        })
        data['sign'] = security.sign_hmac(data, app_secret)
        response = self.client.post('/api/v1/secret/generate/', data=data)
        result = response.json()
        print(result)
        server_public_key = result['result']['server_public_key']
        client_secret = dh_client.getSharedSecret(server_public_key)
        client_secret = cryptutil.longToBase64(client_secret)
        print(client_secret)

    def test_register(self):
        private_key = 'KV1+AvYQU3OyPrCRVvgWEEgEqPao+vFhLlHE4rlb17Km9y9NycUdoYNPfX/yCdDdNIOjW6J+PMZi12qxacFO+1W3aTG7Lyr0Y1czMfxVyF7LH2bgEOPzy8KOrNNTAgSUuor1vRt6J9Mqwt4ccydvvZxnaemv+aS85SvjNpgScw0='
        data = {
            'contract_address': '0xA0C463E09B10d5238567993f0Db41B515eE362C6',
            'token_id': '0',
            'resouce_url': 'ipfs://QmWPf8rHxjG5dEtcaoy2SS1NF221AQJYhz57bKvqskpz3f',
            'csm_version': '1.0',
            'sign_r': '...',
            'sign_s': '...',
            'sign_v': '...',
            'sign_message': '...',
        }
        keys = random.sample(settings.APP_KEY_TO_SECRET.keys(), 1)
        app_key = keys[0]
        print("app_key: %s" % app_key)
        app_secret = settings.APP_KEY_TO_SECRET[app_key]
        data.update({
            'private_key': security.aes_encrypt(app_secret, private_key),
            'app_key': app_key,
            'timestamp': time.time(),
        })
        data['sign'] = security.sign_hmac(data, app_secret)
        response = self.client.post('/api/v1/secret/register/', data=data)
        result = response.json()
        print(result)

    def test_check(self):
        data = {
            'contract_address': '0xA0C463E09B10d5238567993f0Db41B515eE362C6',
            'token_id': '0',
            'sign_r': '...',
            'sign_s': '...',
            'sign_v': '...',
            'sign_message': '...',
        }
        keys = random.sample(settings.APP_KEY_TO_SECRET.keys(), 1)
        app_key = keys[0]
        print("app_key: %s" % app_key)
        app_secret = settings.APP_KEY_TO_SECRET[app_key]
        data.update({
            'app_key': app_key,
            'timestamp': time.time(),
        })
        data['sign'] = security.sign_hmac(data, app_secret)
        response = self.client.post('/api/v1/secret/check/', data=data)
        result = response.json()
        print(result)
        private_key = result['result']['private_key']
        private_key = security.aes_encrypt(app_secret, private_key)
        print(private_key)

    def is_success(self, response):
        result = response.json()
        if result['error_code'] == 1:
            return True
        return False
