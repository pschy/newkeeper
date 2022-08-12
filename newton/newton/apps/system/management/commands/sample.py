from django.core.management.base import BaseCommand
from utils import newton_web3
from utils import ecc_tools, newchain_tools
from eth_account.messages import encode_defunct, _hash_eip191_message
import binascii
from eth_account import Account

class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):

        private_key = '0xb25c7db31feed9122727bf0939dc769a96564b2de4c4726d035b36ecf1e5b364'
        a = Account.from_key(private_key)
        wallet_address = a.address
        print('wallet_address:', wallet_address)
        w3 = newton_web3.get_web3()
        message = encode_defunct(text=wallet_address)
        message_hash = _hash_eip191_message(message)
        hex_message_hash = w3.toHex(message_hash)
        print('hex_message_hash:', hex_message_hash)
        signed_message = w3.eth.account.sign_message(message, private_key=private_key)
        print('signed_message:', signed_message)

        sign_r = hex(signed_message.r)
        sign_s = hex(signed_message.s)
        sign_v = signed_message.v
        sign_message = hex_message_hash
        vrs = (sign_v, sign_r, sign_s)
        hex_address = w3.eth.account.recoverHash(sign_message, vrs=vrs)
        print("hex_address:", hex_address)


        # hex_address = w3.eth.account.recover_message(sign_message, signature=signature)

        # sign_message = binascii.unhexlify(sign_message[2:])
        # print(sign_message, type(sign_message))
        # sign_message = encode_structured_data(primitive=sign_message)
        # print(sign_message)
        
        # w3 = newton_web3.get_web3()
        # vrs = (sign_v, sign_r, sign_s)
        # hex_address = w3.eth.account.recover_message(sign_message, vrs=vrs)
        # print('hex_address: %s' % hex_address)
