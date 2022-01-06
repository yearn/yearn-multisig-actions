# strategist-ms

Collection of useful scripts to manage gnosis multisig wallets
- [Gnosis Safe link](https://gnosis-safe.io/app/)

## Bootstrapping
If you have downloaded this template repository, you need to fill in some config values and add some repository secrets.

### Secrets
Add these repository secrets. Go to https://github.com/{org}/{repo}/settings/secrets/actions

1. PAT - generate personal access token. Go to https://github.com/settings/tokens/new and click repo for scopes. Make sure to reset this secret when the PAT expires.
2. *SCAN_TOKEN - Put in a token from *scan, where * can be ether, ftm, snow, bsc, arbi, or polygon
3. TELEGRAM_TOKEN - This is the token for your telegram bot that will send messages to channels. If you are in the yearn org, contact kx9x for the robowoofy token.
4. PRIVATE_KEY - Generate a private key for your multisig delegate and put it in a github secret. Do not use this private key for anything else. We recommend that you just throw it away once you add the secret. Anyone with access to your repo and the actions will be able to take this private key, so don't make any assumptions. Be ready to revoke your delegate if you see any suspicious transactions queued to it. 

### Config values
In .github/workflows/run-command.yml, fill in eth_safe and ftm_safe with the addresses for your eth and ftm safes. 

Fill in the telegram channel ids as well. You can find these ids by opening your chat in telegram web, taking the number from the url, and adding a 100 between the - and the number. For example, -3456789 would become -1003456789. Announcement and group chats allow you to notify 2 seperate channels. Leave telegram chat ids blank if you don't want notifications.

Fill in everything in the .env file.

Optional:
Fill in scripts/shame.py with a mapping of addresses to signer names for the /shame command.

## Usage
Follow the process steps below for queuing transaction to your multisig
1. Create script using ape safe syntax
2. Create PR on new branch
3. Add a comment on PR to trigger bot to dry-run the txn:
    ```
    /run file=[main|hydrate_ci_cache] fn=[name_of_fxn] network=[eth|bsc|matic|ftm]
    ```
    - The GitHub action runner will respond with:
    - a reply comment with link to the [action which was triggered](https://github.com/yearn/strategist-ms/actions/)
    - 👀 to indicate command is detected
    - 🚀 to indicate script is being run
    - 🎉 to indicate script is run successfully
    - Note: main is the default target script and eth is the default network, you can omit both 
4. After successful dry run, get a peer review
5. When peer review is complete, they can indicate it by using GitHub runner bot to queue the transaction in Gnosis. This is done by adding same comment as step #3, but this time with "send=true"
    ```
    /run file=[main|hydrate_ci_cache] network=[eth|bsc|matic|ftm] fn=[name_of_fxn] send=[true|false] delete-branch-after-send=[true|false]
    ```
    - delete-branch-after-send defaults to true, if you don't want your branch deleted, then set delete-branch-after-send=false
6. After a successful run with send=true, you can track a Gnosis TX back to its PR and original code by going to https://github.com/yearn/strategist-ms/labels and searching for the nonce number and clicking the matching nonce Github label.

![image](https://user-images.githubusercontent.com/7820952/119859130-f1d67600-bec9-11eb-8ac1-3dbc05956210.png)


## Installation
You need Python 3.8 and pip installed

Install dependencies

```
pip install -r requirements-dev.txt
```

You need also ganache-cli installed (and Node)

```
npm install -g ganache-cli
```

Run a multisig tx function on ethereum

```
brownie run main run_example --network eth-main-fork
```

Run a multisig tx function on ftm

```
brownie run main run_example --network ftm-main-fork
```
