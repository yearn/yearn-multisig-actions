import os
from ci.ci_override import DelegateSafe as ApeSafe
from brownie import network


if network.chain.id == 250:
    safe = ApeSafe(os.getenv("FTM_SAFE_ADDRESS"))
elif network.chain.id == 137:
    safe = ApeSafe(os.getenv("POLYGON_SAFE_ADDRESS"))
elif network.chain.id == 56:
    safe = ApeSafe(os.getenv("BSC_SAFE_ADDRESS"))
elif network.chain.id == 4:
    safe = ApeSafe(os.getenv("RIN_SAFE_ADDRESS"))
elif network.chain.id == 42161:
    safe = ApeSafe(os.getenv("ARB_SAFE_ADDRESS"))
else:
    safe = ApeSafe(os.getenv("ETH_SAFE_ADDRESS"))
