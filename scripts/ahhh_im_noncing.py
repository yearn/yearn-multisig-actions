from urllib.parse import urljoin
import requests

def pending_nonce_override(self) -> int:
    """
    Subsequent nonce which accounts for pending transactions in the transaction service.
    """
    url = urljoin(self.transaction_service.base_url, f'/api/v1/safes/{self.address}/multisig-transactions/')
    results = requests.get(url).json()['results']
    # loop through the TXs return and detect a gap in nonce
    # if there is a gap, return a nonce so we fill that gap
    i = 1
    while i < len(results):
        nonce_after = results[i-1]['nonce']
        nonce_before = results[i]['nonce']
        if abs(nonce_after-nonce_before) > 1:
            print(nonce_before + 1)
            return nonce_before + 1
        i += 1

    return results[0]['nonce'] + 1 if results else 0
