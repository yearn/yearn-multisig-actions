# yearn-multisig-actions

Template repository for automating delegate transactions to [Gnosis Safe](https://gnosis-safe.io/app/) multisig wallets through Github Actions

Allows for teams to be notified in Telegram when a new transaction is queued for signature in a multisig. Preview output:

![](https://i.imgur.com/zKTnTY4.png)

## Bootstrapping
NOTE: Please ensure your copy of this repository is private, not public, when you use this template! Super important! You don't want randoms queuing TXs to your Gnosis Safe.

1. Also fork [yearn-workflows](https://github.com/yearn/yearn-workflows/fork), this should be public and you don't need to change it. You just need a fork of this because Github runners can only read workflows within the same organization/account.
2. If you have downloaded this template repository, you must fill in some config values and add some repository secrets. (see below for more details on how to do this)

#### Adding a delegate account
Generate a private key for your multisig delegate. Do NOT use this private key for anything else. We recommend you throw it away once you add the secret. Anyone with access to your repo and the actions can take this private key, so don't make any assumptions.

Be ready to revoke your delegate if you see any suspicious transactions queued to it.

You must be an owner of the safe to add a delegate to it.

You can generate a new delegate using the brownie console. Before you start, make sure that you have your safe owner account in brownie: `brownie accounts new multi-sig-delegator`

Modify scripts/delegates.py with your safe and delegator details.

To create and add a new delegate, run `brownie run delegates create_and_add_delegate`. Note: adjust base url if you need to use a network other than Ethereum. Also, make a note of the private key that is printed for the delegate, you will need that later.

To add an existing account as a delegate, run `brownie run delegates add_delegate_from_existing_address <address>`

If you want to add a delegate via a UI, you can also use https://gnosis-safe-delegate.vercel.app/. Just create a new throwaway private key for the delegate, you will need it later.

### Secrets
Add these repository secrets. Go to https://github.com/{org}/{repo}/settings/secrets/actions

1. `PAT` - generate a personal access token. Go to https://github.com/settings/tokens/new and click repo for scopes. Make sure to reset this secret when the PAT expires.
2. `{NETWORK}SCAN_TOKEN` - Define multiple secrets where {NETWORK} can be ETHER, FTM, SNOW, BSC, ARBI, or POLYGON. You can generate these tokens by making an account at the respective sites (e.g. etherscan.io, ftmscan.com, etc, etc). If you don't need a token for a given network, then either set the secret to something random or edit run-command.yml to pass in '' for the token you don't need.
3. `TELEGRAM_TOKEN` - This is the token for your telegram bot that will send messages to channels. To create a bot go to: https://core.telegram.org/bots. If you are in the yearn org, contact kx9x for the robowoofy token.
4. `PRIVATE_KEY` - Private key for your delegate (get this from the previous step where you added your delegate account)

### Config values
1. Fill in the telegram channel ids in run-command.yml. 

    You can find these ids by opening your chat on Telegram web, taking the number from the url, and adding a `100` between the "-" and the number. For example, `-3456789` would become `-1003456789`. Announcements and group chats allow you to notify 2 separate channels. Leave telegram chat ids blank if you don't want notifications.

    Alternatively, you can message @username_to_id_bot on Telegram to find a chat id.

1. Fill in everything in the .env file. Leave placeholder values for any safes on networks you don't need.

Optional:
Fill in scripts/shame.py with a mapping of addresses to signer names for the /shame command.

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
    /run file=[main|hydrate_ci_cache] fn=[name_of_fxn] network=[eth|bsc|matic|ftm|rin|arb] send=[true|false] delete-branch-after-send=[true|false]
    ```
    - delete-branch-after-send defaults to true. If you don't want your branch deleted, then set delete-branch-after-send=false
6. After a successful run with send=true, you can track a Gnosis TX back to its PR and original code by going to https://github.com/yearn/strategist-ms/labels and searching for the nonce number, then clicking the matching nonce Github label.

![image](https://user-images.githubusercontent.com/7820952/119859130-f1d67600-bec9-11eb-8ac1-3dbc05956210.png)


## Installation
You need [Python 3.8](https://www.python.org/downloads/release/python-389/) and [pip](https://pip.pypa.io/en/stable/installation/) installed

Install dependencies

```
pip install -r requirements-dev.txt
```

You also need [ganache-cli](https://www.npmjs.com/package/ganache-cli) installed, and [Node.js](https://nodejs.org/en/)

```
npm install -g ganache-cli
```

Run a multisig tx function on Ethereum

```
brownie run main run_example --network eth-main-fork
```

Run a multisig tx function on FTM

```
brownie run main run_example --network ftm-main-fork
```

## Hydrating the compiler cache

This is important if you want fast runs.

1. In run-command.yml, bump compiler_cache_version by 1 (i.e. v0.0.1 to v0.0.2)
2. Check this change in your master/main branch
3. Create a PR from master into a random branch. This is important. Master has to be the base branch for this PR.
4. Comment "/run fn=hydrate_compiler_cache"
5. After this command finishes, you will have all vyper and solc compilers in your cache for each subsequent run.
