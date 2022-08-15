from django.core.management.base import BaseCommand
from utils import newton_web3, security
from utils import ecc_tools, newchain_tools
from eth_account.messages import encode_defunct
import binascii
from eth_account import Account
from key.services import BindParams, GetParams
import rlp

class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('action', nargs='+')

    def handle(self, *args, **options):

        action = options['action'][0]
        if action == 'bind':
            self.bind()
        elif action == 'get':
            self.get()

    def bind(self):
        wallet_private_key = '0xfe57344d5442fef7aadc69406adb5e1641de9a6a5353272c7133eed61b299d03'
        a = Account.from_key(wallet_private_key)
        wallet_address = a.address
        print('wallet_address:', wallet_address)

        w3 = newton_web3.get_web3(1007)
        message = 'abcdefgjkqwerrttyuio'
        signable_message = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(signable_message, private_key=wallet_private_key)

        key_id = '39d9403f502e6c4d14fab1733a27b6712029a392f34462b92a3f8a1b626cc972'
        encrypt_key = '75d78bdb89dd0baeaeacdbef66ba4240'
        shared_secret = '0x3c6ed3a0d88d664f418158d413dfb2aa655bcb306ccf4f5f14df12f2f55be8a3d1db4cd0707bc5e5236ffb3eddbd55bccaa39d4f03099d4955941f0fe105488927a2'
        private_key = security.aes_encrypt(shared_secret[2:32], encrypt_key)
        bindParams = BindParams(
            key_id=bytes(key_id, encoding='utf-8'),
            r=signed_message.r,
            s=signed_message.s,
            v=signed_message.v,
            private_key=bytes(private_key, encoding='utf-8'),
            message=bytes(message, encoding='utf-8'),
            contract_address=bytes('0xFD1d4413030c39758Afd48b34b839BFe265FD9D9', encoding='utf-8'),
            token_id=0,
            chain_id=1007
        )
        data = rlp.encode(bindParams, BindParams)
        print(w3.toHex(data))

    def get(self):
        wallet_private_key = '0xfe57344d5442fef7aadc69406adb5e1641de9a6a5353272c7133eed61b299d03'
        a = Account.from_key(wallet_private_key)
        wallet_address = a.address
        print('wallet_address:', wallet_address)

        w3 = newton_web3.get_web3(1007)
        message = 'abcdefgjkqwerrttyuio'
        signable_message = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(signable_message, private_key=wallet_private_key)
        key_id = '39d9403f502e6c4d14fab1733a27b6712029a392f34462b92a3f8a1b626cc972'
        prime = 'AMrE1jd2GZVUUUqf2+vKNCrBCiZhUKIeVt7cOb75y9/OFJqWOt+fT70fW84Q8q/ylM9frco77+XPlicOY0czYOs='
        peer_swap_key = 'Lws4ROYFY8LBhlrLFWJNy9CAhF7xDvavsK6BRwr28DhsMu65FEY1bbJwJNVM0Y+m/tconbq7TyCZe32syj03mw=='
        getParams = GetParams(
            key_id=bytes(key_id, encoding='utf-8'),
            r=signed_message.r,
            s=signed_message.s,
            v=signed_message.v,
            message=bytes(message, encoding='utf-8'),
            prime=bytes(prime, encoding='utf-8'),
            peer_swap_key=bytes(peer_swap_key, encoding='utf-8')
        )
        data = rlp.encode(getParams, GetParams)
        print(w3.toHex(data))
