from time import time

import requests
from brownie import *
from brownie.network.account import LocalAccount
from eth_account import Account

BASE_URL = "https://safe-transaction.gnosis.io/api/v1"

## Modify values here
# 1. Add your safe
safe = web3.ens.resolve("web.ychad.eth") ## TODO: Replace with your safe address


# 2. Add your delegator. This account needs to be a owner of the safe
_delegator = accounts.load('multi-sig-delegator') ## TODO: Load your account


# Use the Account from eth_account to make signing hashs easier
delegator = Account.from_key(_delegator.private_key)


## You can also use a hardware wallet like Trezor or Ledger with clef. See https://eth-brownie.readthedocs.io/en/stable/account-management.html?highlight=private%20key#using-a-hardware-wallet
# accounts.connect_to_clef("/Users/gazumps/Library/Signer/clef.ipc")
# delegator = accounts[1]

# 3. Add your delegate
## Create a new throw away account 


def list_delegates(safe: str):
    response = requests.get(f"{BASE_URL}/delegates/", params={"safe": safe})
    print(response.json()["results"])


def make_payload(safe: str, delegate: str, delegator: Account, label: str = None):
    message = web3.keccak(text=delegate + str(int(time() // 3600)))
    signature = delegator.signHash(message).signature.hex()
    return {"safe": safe, "delegate": delegate, "signature": signature, "label": label}


def add_delegate(safe: str, delegate: str, delegator: Account, label: str = None):
    payload = make_payload(safe, delegate, delegator, label)
    response = requests.post(f"{BASE_URL}/safes/{safe}/delegates/", json=payload)
    color = "green" if response.ok else "red"
    print(f"{response.status_code}: {response.text}")


def create_and_add_delegate():
    delegate = Account.create()
    add_delegate(safe, delegate.address, delegator, label="Robowoofy")
    print("Delegate Address: ", delegate.address)
    print("Delegate Private Key: ", delegate.privateKey.hex())
    print()
    print("List of Delegates:")
    print (list_delegates(safe))


def add_delegate_from_existing_address(address):
    add_delegate(safe, address, delegator, label="Robowoofy")
    print("Delegate Address: ", address)
    print()
    print("List of Delegates:")
    print (list_delegates(safe))
