import multisig_ci.ci_override
from scripts.ahhh_im_noncing import pending_nonce_override
from multisig_ci.ci_override import DelegateSafe as ApeSafe
ApeSafe.pending_nonce = pending_nonce_override
from multisig_ci.safes import safe
from multisig_ci.sign import sign


@sign
def example():
    safe.account.transfer(safe.account, "0 ether")


@sign(420)
def override_nonce_example():
    safe.account.transfer(safe.account, "0 ether")
