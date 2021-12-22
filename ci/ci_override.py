import os
from ape_safe import ApeSafe
from brownie import accounts
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


class DelegateSafe(ApeSafe):
    @property
    def is_ci(self):
        return os.environ.get("CI", "").lower() == "true"

    @property
    def is_send(self):
        return os.environ.get("GITHUB_ACTION_SEND", "").lower() == "true"

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
