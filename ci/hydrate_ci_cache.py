import requests
import os, stat
from brownie import Contract, network, exceptions
from ape_safe import ApeSafe
import time
import ci.ci_override

vyper_releases = [
    "https://github.com/vyperlang/vyper/releases/download/v0.3.1/vyper.0.3.1.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.3.0/vyper.0.3.0+commit.8a23feb.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.16/vyper.0.2.16+commit.59e1bdd.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.15/vyper.0.2.15+commit.6e7dba7.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.12/vyper.0.2.12+commit.2c6842c.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.11/vyper.0.2.11+commit.5db35ef.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.8/vyper.0.2.8+commit.069936f.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.7/vyper.0.2.7+commit.0b3f3b3.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.6/vyper.0.2.6+commit.35467d5.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.5/vyper.0.2.5+commit.a0c561c.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.4/vyper.0.2.4+commit.7949850.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.3/vyper.0.2.3+commit.006968f.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.2/vyper.0.2.2+commit.337c2ef.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.1/vyper.0.2.1+commit.cac3d7d.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.2.0/vyper.0.2.0+commit.d2c0c87.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.1.0-beta.17/vyper.0.1.0-beta.17+commit.0671b7b.linux",
    "https://github.com/vyperlang/vyper/releases/download/v0.1.0-beta.16/vyper.0.1.0-beta.16+commit.5e4a94a.linux",
]

solc_url_prefix = "https://solc-bin.ethereum.org/linux-amd64/solc-linux-amd64-"

solc_release_versions = [
    "v0.8.11+commit.d7f03943",
    "v0.8.10+commit.fc410830",
    "v0.8.9+commit.e5eed63a",
    "v0.8.8+commit.dddeac2f",
    "v0.8.7+commit.e28d00a7",
    "v0.8.6+commit.11564f7e",
    "v0.8.5+commit.a4f2e591",
    "v0.8.4+commit.c7e474f2",
    "v0.8.3+commit.8d00100c",
    "v0.8.2+commit.661d1103",
    "v0.8.1+commit.df193b15",
    "v0.8.0+commit.c7dfd78e",
    "v0.7.6+commit.7338295f",
    "v0.7.5+commit.eb77ed08",
    "v0.7.4+commit.3f05b770",
    "v0.7.3+commit.9bfce1f6",
    "v0.7.2+commit.51b20bc0",
    "v0.7.1+commit.f4a555be",
    "v0.7.0+commit.9e61f92b",
    "v0.6.12+commit.27d51765",
    "v0.6.11+commit.5ef660b1",
    "v0.6.10+commit.00c0fcaf",
    "v0.6.9+commit.3e3065ac",
    "v0.6.8+commit.0bbfe453",
    "v0.6.7+commit.b8d736ae",
    "v0.6.6+commit.6c089d02",
    "v0.6.5+commit.f956cc89",
    "v0.6.4+commit.1dca32f3",
    "v0.6.3+commit.8dda9521",
    "v0.6.2+commit.bacdbe57",
    "v0.6.1+commit.e6f7d5a4",
    "v0.6.0+commit.26b70077",
    "v0.5.17+commit.d19bba13",
    "v0.5.16+commit.9c3226ce",
    "v0.5.15+commit.6a57276f",
    "v0.5.14+commit.01f1aaa4",
    "v0.5.13+commit.5b0b510c",
    "v0.5.12+commit.7709ece9",
    "v0.5.11+commit.22be8592",
    "v0.5.11+commit.c082d0b4",
    "v0.5.10+commit.5a6ea5b1",
    "v0.5.9+commit.c68bc34e",
    "v0.5.9+commit.e560f70d",
    "v0.5.8+commit.23d335f2",
    "v0.5.7+commit.6da8b019",
    "v0.5.6+commit.b259423e",
    "v0.5.5+commit.47a71e8f",
    "v0.5.4+commit.9549d8ff",
    "v0.5.3+commit.10d17f24",
    "v0.5.2+commit.1df8f40c",
    "v0.5.1+commit.c8a2cb62",
    "v0.5.0+commit.1d4f565a",
    "v0.4.26+commit.4563c3fc",
    "v0.4.25+commit.59dbf8f1",
    "v0.4.24+commit.e67f0147",
    "v0.4.23+commit.124ca40d",
    "v0.4.22+commit.4cb486ee",
    "v0.4.21+commit.dfe3193c",
    "v0.4.20+commit.3155dd80",
    "v0.4.19+commit.c4cbbb05",
    "v0.4.18+commit.9cf6e910",
    "v0.4.17+commit.bdeb9e52",
    "v0.4.16+commit.d7661dd9",
    "v0.4.15+commit.8b45bddb",
    "v0.4.15+commit.bbb8e64f",
    "v0.4.14+commit.c2215d46",
    "v0.4.13+commit.0fb4cb1a",
    "v0.4.12+commit.194ff033",
    "v0.4.11+commit.68ef5810",
]

home_directory = os.environ.get("HOME")


def hydrate_compiler_cache():
    for vyper_release in vyper_releases:
        mod = vyper_release.index("+") if "+" in vyper_release else vyper_release.index(".linux")
        name = vyper_release[vyper_release.index("vyper.") : mod]
        print("Downloading " + name)
        r = requests.get(vyper_release, allow_redirects=True)
        vvm_folder = os.path.join(home_directory, ".vvm/")
        if not os.path.exists(vvm_folder):
            os.mkdir(vvm_folder)
        file_name = vvm_folder + name.replace(".", "-", 1)
        with open(file_name, "wb+") as f:
            f.write(r.content)
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)

    for solc_release_version in solc_release_versions:
        solc_release_url = solc_url_prefix + solc_release_version
        prefix = "solc-linux-amd64"
        start = solc_release_url.index(prefix) + len(prefix)
        end = solc_release_url.index("+")
        name = "solc" + solc_release_url[start:end]
        print("Downloading " + name)
        r = requests.get(solc_release_url, allow_redirects=True)
        solcx_folder = os.path.join(home_directory, ".solcx/")
        if not os.path.exists(solcx_folder):
            os.mkdir(solcx_folder)
        file_name = os.path.join(home_directory, ".solcx/") + name
        with open(file_name, "wb+") as f:
            f.write(r.content)
            st = os.stat(file_name)
            os.chmod(file_name, st.st_mode | stat.S_IEXEC)