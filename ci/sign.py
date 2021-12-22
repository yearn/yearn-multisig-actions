from ci.safes import safe


def sign(nonce_arg = None, post_tx = False):
    def _sign(func):
        def wrapper():
            func()
            safe_tx = safe.multisend_from_receipts(safe_nonce=nonce)
            safe.preview(safe_tx, call_trace=False)
            if not post_tx and not safe.is_ci:
                print("dry-run finished, run again with @sign(post_tx = True) to sign and submit the tx.")
            else:
                safe.sign_transaction(safe_tx)
                safe.post_transaction(safe_tx)

        return wrapper

    if callable(nonce_arg):
        nonce = None
        return _sign(nonce_arg)

    nonce = int(nonce_arg) if nonce_arg else nonce_arg
    return _sign