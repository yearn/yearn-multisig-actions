import os
from dotenv import load_dotenv
from ci.ci_override import DelegateSafe as ApeSafe
from brownie import network


load_dotenv()
if network.chain.id == 250:
    safe = ApeSafe(os.getenv("FTM_SAFE_ADDRESS"))
elif network.chain.id == 137:
    safe = ApeSafe(os.getenv("POLYGON_SAFE_ADDRESS"))
elif network.chain.id == 56:
    safe = ApeSafe(os.getenv("BSC_SAFE_ADDRESS"))
else:
    safe = ApeSafe(os.getenv("ETH_SAFE_ADDRESS"))
