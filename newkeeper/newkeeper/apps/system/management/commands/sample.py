from django.core.management.base import BaseCommand
from utils import newton_web3, security
from utils import ecc_tools, newchain_tools
from newchain_account.messages import encode_defunct
import binascii
from newchain_account import Account
from key.rlp_services import BindParams, GetParams
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

        rpc_url = 'https://rpc1.newchain.newtonproject.org/'
        w3 = newton_web3.get_web3(rpc_url, 1007)
        message = 'abcdefgjkqwerrttyuio'
        signable_message = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(signable_message, private_key=wallet_private_key)

        key_id = 'ab0282f22fc421c5bfe60a77b92692a06af7a14ae205ea424348352d368ae9d7'
        encrypt_key = 'd41d8cd98f00b204e9800998ecf8427e'
        shared_secret = '0x7f1f94707dddd6cd5d7e0092b0031c32ea55519265914806b3c60187c271cb848fb69deb82f895ef37392e9d5f3b7c3ac230265897b77ff15beb110bf082fcf8'
        private_key = security.aes_encrypt(shared_secret[2:34], encrypt_key)
        bindParams = BindParams(
            key_id=bytes(key_id, encoding='utf-8'),
            r=signed_message.r,
            s=signed_message.s,
            v=signed_message.v,
            private_key=bytes(private_key, encoding='utf-8'),
            message=bytes(message, encoding='utf-8'),
            contract_address=bytes('0x66fE876AD7C00319aF3030D3736A6D921CDF744B', encoding='utf-8'),
            nft_contract_address=bytes('0xFD1d4413030c39758Afd48b34b839BFe265FD9D9', encoding='utf-8'),
            rpc_url=bytes(rpc_url, encoding='utf-8'),
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

        w3 = newton_web3.get_web3('https://rpc1.newchain.newtonproject.org/')
        message = 'abcdefgjkqwerrttyuio'
        signable_message = encode_defunct(text=message)
        signed_message = w3.eth.account.sign_message(signable_message, private_key=wallet_private_key)
        key_id = 'ab0282f22fc421c5bfe60a77b92692a06af7a14ae205ea424348352d368ae9d7'
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
