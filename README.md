# yearn-multisig-actions

Template repository for automating delegate transactions to [Gnosis Safe](https://gnosis-safe.io/app/) multisig wallets through Github Actions

Allows for teams to be notified in Telegram when a new transaction is queued for signature in a multisig. Preview output:

![](https://i.imgur.com/zKTnTY4.png)

## Bootstrapping
NOTE: Please ensure your copy of this repository is private, not public, when you use this template! Super important! You don't want randoms queuing TXs to your Gnosis Safe.

1. Set your workflow permissions to `Read and write permissions` and your actions permissions to `Allow all actions and reusable workflows` under https://github.com/{org}/{repo}/settings/actions. Note: replace {org} and {repo} with your information.
![image](https://github.com/yearn/yearn-multisig-actions/assets/7820952/2a945da1-31be-497b-817f-0149356eaa49)
![image](https://github.com/yearn/yearn-multisig-actions/assets/7820952/67292dc2-dc02-49d7-80fa-083b6d869552)

3. Also fork [yearn-workflows](https://github.com/yearn/yearn-workflows/fork), this should be public and you don't need to change it. You just need a fork of this because Github runners can only read workflows within the same organization/account.
4. If you have downloaded this template repository, you must fill in some config values and add some repository secrets. (see below for more details on how to do this)

#### Adding a delegate account

1. Create a new delegate account via brownie
 - `brownie accounts generate multi-sig-delegate`
 - Get the private key and save it for later:
    ```
    brownie console
    ```
    ```
    delegate = accounts.load('multi-sig-delegate')
    print("Address: ", delegate.address)
    print("Private Key: ", delegate.private_key)
    ```
    Note: Do NOT use this private key for anything else. We recommend you throw it away once you add the secret. Anyone with access to your repo and the actions can take this private key, so don't make any assumptions. Be ready to revoke your delegate if you see any suspicious transactions queued to it.

2. Authorize your new delegate on your safe. You must do this via an account that is a safe owner or signer.
    - You add delegates via a UI such as https://gnosis-safe-delegate.vercel.app/
    - Alternatively, if the UI doesn't work, you can import your safe owner into brownie and run a script to add the delegate:
        - Follow the steps under [Installation](#Installation) to setup this repo for running scripts locally 
        - run `brownie accounts new multi-sig-delegator` to import your safe owner account
        - open [delegates.py](scripts/delegates.py) and add in your safe address for the `safe` variable and also change the 
        `brownie run delegates add_delegate_from_existing_address <delegate_address> --network <network>-main`. Replace `<network>` with the short name for a network, e.g. eth, opti, ftm, arb, gor, etc.
    
### Secrets
Add these repository secrets. Go to https://github.com/{org}/{repo}/settings/secrets/actions. Note: replace {org} and {repo} with your information.

1. `PAT` - generate a personal access token. Go to https://github.com/settings/tokens/new and click repo for scopes. Make sure to reset this secret when the PAT expires. Note: if you are in the Yearn org, ask @kx9x for a PAT from the Robowoofy Github accout instead of using your own.
2. `{NETWORK}SCAN_TOKEN` - Define multiple secrets where {NETWORK} can be ETHER, FTM, SNOW, BSC, ARBI, or POLYGON. You can generate these tokens by making an account at the respective sites (e.g. etherscan.io, ftmscan.com, etc, etc). If you don't need a token for a given network, then either set the secret to something random or edit run-command.yml to pass in '' for the token you don't need.
3. `TELEGRAM_TOKEN` - This is the token for your telegram bot that will send messages to channels. To create a bot go to: https://core.telegram.org/bots. If you are in the yearn org, contact kx9x for the robowoofy token.
4. `PRIVATE_KEY` - Private key for your delegate (get this from the previous step where you added your delegate account)

### Config values
1. Fill in the telegram channel ids in run-command.yml. 

    You can find these ids by opening your chat on Telegram web, taking the number from the url, and adding a `100` between the "-" and the number. For example, `-3456789` would become `-1003456789`. Announcements and group chats allow you to notify 2 separate channels. Leave telegram chat ids blank if you don't want notifications.

    Alternatively, you can message @username_to_id_bot on Telegram to find a chat id.

1. Fill in values in the .env file. For any safes on networks you don't need, feel free to leave those blank. Some fields are marked optional.

## Usage
Follow the process steps below for queuing transactions to your multisig
1. Create a script using ape-safe syntax
2. Create a PR on a new branch
3. Add a comment on PR to trigger the bot to dry-run the txn:
    ```
    /run file=[main|hydrate_ci_cache] fn=[name_of_fxn] network=[eth|bsc|matic|ftm|rin|arb]
    ```
    Note: remove the [ ] symbols, e.g. /run fn=run_example network=matic
    The file param defaults to main, so you can usually omit it

    - The GitHub action runner will respond with:
    - a reply comment with link to the [action which was triggered](https://github.com/yearn/strategist-ms/actions/)
    - 👀 to indicate command is detected
    - 🚀 to indicate script is being run
    - 🎉 to indicate script is run successfully
    - Note: main is the default target script and eth is the default network, you can omit both 
4. After a successful dry run, get a peer review
5. When peer review is complete, they can indicate it by using GitHub runner bot to queue the transaction in Gnosis. To do this, add the same comment as step #3 but this time with "send=true"
    ```
    /run file=[main] fn=[name_of_fxn] network=[eth|bsc|matic|ftm|rin|arb] send=[true|false] delete-branch-after-send=[true|false]
    ```
    - delete-branch-after-send defaults to true. If you don't want your branch deleted, then set delete-branch-after-send=false
6. After a successful run with send=true, you can track a Gnosis TX back to its PR and original code by going to https://github.com/yearn/strategist-ms/labels and searching for the nonce number, then clicking the matching nonce Github label.

![image](https://user-images.githubusercontent.com/7820952/119859130-f1d67600-bec9-11eb-8ac1-3dbc05956210.png)


## Installation

### Run the [pyenv installer](https://github.com/pyenv/pyenv#automatic-installer)
```
curl https://pyenv.run | bash
```

### Install python 3.10
```
pyenv install 3.10
```

### Make a venv
```
pyenv virtualenv 3.10 <venv-name>
```

### Make it automatically activate while in the project folder
```
pyenv local <venv-name>
```

### Install deps
```
 pip install -r requirements-dev.txt 
```

It's THAT easy!

### You also need anvil installed (using a specific version as of 04/25/2024 due to a bug in foundry)
```
 curl -L https://foundry.paradigm.xyz | bash
 $HOME/.foundry/bin/foundryup --version nightly-f625d0fa7c51e65b4bf1e8f7931cd1c6e2e285e9
```

Open a new terminal and make sure Anvil exists
```
anvil --help
```

### Now install Brownie using [pipx](https://github.com/eth-brownie/brownie#via-pipx)

```
python -m pip install --user pipx
python -m pipx ensurepath
pipx install eth-brownie==1.19.2
```

Open a new terminal.

Run a multisig tx function on ethereum
```
brownie run main example -I
```
