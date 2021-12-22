from brownie import *
from ci.safes import safe
import requests
from contextlib import redirect_stdout
import os


SIGNERS = {
    # Map address to name for each signer
    #"0xdeadbeefdeadbeefdeadbeefdeadbeef": "Hard Rock Nick",
}


def ci_alert():
    home_directory = os.environ.get("HOME")
    with open(os.path.join(home_directory, "alert.txt"), "w+") as f:
        with redirect_stdout(f):
            main()


def main():
    url = f"https://safe-transaction.mainnet.gnosis.io/api/v1/safes/{safe}/transactions/"
    data = requests.get(url).json()
    nonce = safe.retrieve_nonce()
    pending = [tx for tx in data["results"][::-1] if not tx["isExecuted"] and tx["nonce"] >= nonce]

    if len(pending) > 4:
        print(
            "Okay, Okay, Okay. I need the signatures to go up. I can't take this anymore. Everyday I'm checking the signatures and it's dipping. Everyday I check the signatures, bad signatures. I can't take this anymore man. I have over-delegated, by A LOT. It is what it is but I need the signatures to go up. Can signers do something?\n"
        )

    print(f"pls sign https://gnosis-safe.io/app/eth:{safe}/transactions/queue")
    for tx in pending:
        unsigned = set(SIGNERS) - {x["owner"] for x in tx["confirmations"]}
        users = " ".join(f"@{SIGNERS[x]}" for x in unsigned)
        print(f'{tx["nonce"]}: {users}')
