from django.db import models
from config import codes


class KeyList(models.Model):
    key_id = models.CharField(max_length=512, unique=True)
    contract_address = models.CharField(max_length=128, default='')
    nft_contract_address = models.CharField(max_length=128, default='')
    token_id = models.CharField(max_length=64, default='0')
    chain_id = models.CharField(max_length=64, default='0')
    rpc_url = models.CharField(max_length=512, default='')
    encrypt_key = models.CharField(max_length=512)
    bind_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'key_list'
