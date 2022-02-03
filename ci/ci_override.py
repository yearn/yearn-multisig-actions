import os
from ape_safe import ApeSafe, transaction_service
from brownie import accounts, network
from gnosis.safe.safe_tx import SafeTx
from typing import Optional, Union
from brownie.network.account import LocalAccount

# CI horribleness lurks below
# If running in CI, let's override ApeSafe.post_transaction so
# that it writes a file with the nonce. This is used to later tag
# the pull request with a label matching the nonce

# TODO: configuration file
DELEGATE_ADDRESS = os.environ.get("DELEGATE_ADDRESS")
home_directory = os.environ.get("HOME")

gnosis_frontend_urls = {
    'gnosis': {
        1: 'https://gnosis-safe.io/app/eth:{0}/transactions/queue',
        4: 'https://gnosis-safe.io/app/rin:{0}/transactions/queue',
        56: 'https://gnosis-safe.io/app/bsc:{0}/transactions/queue',
        100: 'https://gnosis-safe.io/app/xdai:{0}/transactions/queue',
        137: 'https://gnosis-safe.io/app/matic:{0}/transactions/queue',
        250: 'https://safe.fantom.network/#/safes/{0}/transactions',
        42161: 'https://gnosis-safe.io/app/arbi:{0}/transactions/queue'
    }
}

class DelegateSafe(ApeSafe):
    def __init__(self, address, base_url=None, multisend=None):
        """
        Create an ApeSafe from an address or a ENS name and use a default connection.
        """
        backend_urls = {
            'gnosis': transaction_service,
        }

        # default to gnosis if we don't have a custom version
        if network.chain.id not in backend_urls[self.backend_type]:
            backend_url_from_config = backend_urls["gnosis"][network.chain.id]
            self.frontend_url = gnosis_frontend_urls["gnosis"][network.chain.id]
        else:
            backend_url_from_config = backend_urls[self.backend_type][network.chain.id]
            self.frontend_url = gnosis_frontend_urls[self.backend_type][network.chain.id]

        self.base_url = base_url or backend_url_from_config
        super().__init__(address, base_url, multisend)

    @property
    def is_ci(self):
        return os.environ.get("CI", "").lower() == "true"

    @property
    def is_send(self):
        return os.environ.get("GITHUB_ACTION_SEND", "").lower() == "true"

    @property
    def backend_type(self):
        backend_from_env = os.environ.get("BE", "").lower()
        return backend_from_env if backend_from_env != "" else "gnosis"

    def post_transaction(self, safe_tx: SafeTx):
        super().post_transaction(safe_tx)

        if self.is_ci and self.is_send:
            with open(os.path.join(home_directory, "nonce.txt"), "w") as f:
                f.write(str(safe_tx.safe_nonce))
            exit(0)

    def preview(self, safe_tx: SafeTx, events=True, call_trace=False, reset=True):
        if self.is_ci:
            events = False
            call_trace = False

        return super().preview(safe_tx, events=events, call_trace=call_trace, reset=reset)

    def get_signer(self, signer: Optional[Union[LocalAccount, str]] = None) -> LocalAccount:
        if self.is_ci:
            with open(os.path.join(home_directory, "safe.txt"), "w") as f:
                f.write(str(self.frontend_url.format(self.address)))

            if self.is_send:
                key = os.environ.get("PRIVATE_KEY")
                assert (
                    key is not None
                ), "CI environment missing PRIVATE_KEY environment variable. Please add it as a repository secret."
                user = accounts.add(key)
                assert (
                    user.address == DELEGATE_ADDRESS
                ), "Delegate address mismatch. Check you have correct private key."
                return user
            else:
                print("CI dry-run enabled, set send to true to run to completion")
                exit(0)
        else:
            return super().get_signer(signer)


with open(os.path.join(home_directory, "alive.signal"), "w") as f:
    f.write("I am alive")
