# strategist-ms

Collection of useful scripts to manage gnosis multisig wallets
- [Gnosis Safe link](https://gnosis-safe.io/app/)

## Bootstrap
If you have downloaded this template repository, you need to fill in some config values and add some repository secrets.

List of tasks:
- 

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