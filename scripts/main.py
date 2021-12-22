import ci.ci_override
from ci.ci_override import DelegateSafe as ApeSafe
from ci.safes import safe
from ci.sign import sign


@sign
def run_example():
    safe.account.transfer(safe.account, "0 ether")


@sign(420)
def run_override_nonce_example():
    safe.account.transfer(safe.account, "0 ether")
