# NewKeeper

A Python implementation of NewKeeper.

* Python 3.8+ support

## Developer Setup

Take Linux as example:

```sh
git clone git@github.com:newtonproject/newkeeper.git
cd newkeeper
```

Then run these install commands:

```sh
virtualenv venv
source venv/bin/activate
pip install -r newkeeper/requirements.txt
```


## Using Docker

If you would like to develop and test inside a Docker environment, run these commands to start up:

```
docker build -t newkeeper .
docker run -it -d -p 80:8000 --name newkeeper-dev newkeeper
```

Then you can use 127.0.0.1 to test newkeeper api.


## Api

There is a demo script which show the whole process of how to use this api. Its path: newkeeper/newkeeper/apps/system/management/commands/demo.py

#### POST `/v1/key/generator` 

Use DiffieHellman algorithm to generate prime and peer_swap_key, swap node_swap_key from server api.

#### params 
| params | type | desc |
| ------ | ------ | ------ |
| prime | string | prime |
| peer_swap_key | string | peer swap key | 

#### response
| params | type | desc |
| ------ | ------ | ------ |
| node_swap_key | string | node swap key |



#### POST `/v1/key/bind`

Register the binding relationship with key_id and encrypt_key, contract_address, token_id in newkeeper.

#### params 
| params | type | desc |
| ------ | ------ | ------ |
| sign_data | string | hex string of data encoded by rlp | 

Actual data to encode by rlp：

| params | type | desc |
| ------ | ------ | ------ |
| key_id | string | keyID | 
| chain_id | string | chainID |
| contract_address | string | contract address |
| token_id | string | tokenID | 
| private_key | string | encrypt key after AES encryption |
| r | string |  |
| s | string |  |
| v | string |  |
| message | string |  |

#### response
| params | type | desc |
| ------ | ------ | ------ |
| error_code | int |  |




#### POST `/v1/key/` 

Get encrypt_key from newkeeper using key_id. Use DiffieHellman algorithm to protect the transmission of private_key.

#### params 
| params | type | desc |
| ------ | ------ | ------ |
| sign_data | string | hex string of data encoded by rlp | 

Actual data to encode by rlp：

| params | type | desc |
| ------ | ------ | ------ |
| prime | string | prime |
| peer_swap_key | string | peer swap key | 
| key_id | string | keyID | 
| r | string |  |
| s | string |  |
| v | string |  |
| message | string |  |

#### response
| params | type | desc |
| ------ | ------ | ------ |
| node_swap_key | string | node swap key |
| private_key | string | encrypt key after AES encryption |

