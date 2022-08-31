import xrpl
from xrpl.wallet import generate_faucet_wallet

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)
faucet_url = "https://faucet.altnet.rippletest.net/accounts"


# Issue_quantity "1000000000000000e-96"
def mint_nft_on_xrpl(cold_wallet, hot_wallet, currency_code, issue_quantity, memo_data, memo_type):
    # Configure issuer (cold address) settings -------------------------------------
    cold_settings_tx = xrpl.models.transactions.AccountSet(
        account=cold_wallet.classic_address,
        transfer_rate=0,
        set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE,
    )

    cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=cold_settings_tx,
        wallet=cold_wallet,
        client=client,
    )
    print("Sending cold address AccountSet transaction...")
    response = xrpl.transaction.send_reliable_submission(cst_prepared, client)
    print(response)
    print("==============================================")
    # Configure hot address settings -----------------------------------------------
    hot_settings_tx = xrpl.models.transactions.AccountSet(
        account=hot_wallet.classic_address,
        set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
    )
    hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=hot_settings_tx,
        wallet=hot_wallet,
        client=client,
    )
    print("Sending hot address AccountSet transaction...")
    response = xrpl.transaction.send_reliable_submission(hst_prepared, client)
    print(response)
    print("==============================================")

    # Create trust line from hot to cold address -----------------------------------
    trust_set_tx = xrpl.models.transactions.TrustSet(
        account=hot_wallet.classic_address,
        limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=issue_quantity,
        )
    )

    ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=trust_set_tx,
        wallet=hot_wallet,
        client=client,
    )

    print("Creating trust line from hot address to issuer...")
    response = xrpl.transaction.send_reliable_submission(ts_prepared, client)
    print(response)
    print("==============================================")

    # Send token -------------------------------------------------------------------
    send_token_tx = xrpl.models.transactions.Payment(
        account=cold_wallet.classic_address,
        destination=hot_wallet.classic_address,
        amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=issue_quantity
        ),
        memos=[xrpl.models.transactions.Memo(memo_data=memo_data, memo_type=memo_type)]
    )

    pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=send_token_tx,
        wallet=cold_wallet,
        client=client,
    )
    print(f"Sending {issue_quantity} {currency_code} to {hot_wallet.classic_address}...")
    response = xrpl.transaction.send_reliable_submission(pay_prepared, client)
    print("Transaction Succeded! Here's the ledger hash: "+response.result.get('hash'))
    print("==============================================")

    # Check balances ---------------------------------------------------------------
    print("Getting hot address balances...")
    response = client.request(xrpl.models.requests.AccountLines(
        account=hot_wallet.classic_address,
        ledger_index="validated",
    ))
    print(response)
    print("==============================================")
    print("Getting cold address balances...")
    response = client.request(xrpl.models.requests.GatewayBalances(
        account=cold_wallet.classic_address,
        ledger_index="validated",
        hotwallet=[hot_wallet.classic_address]
    ))
    print(response)
    print("==============================================")

def sell_nft_after_minting(currency_code, cold_wallet, amt_for_sale, hot_wallet):
    print("SELLING THE NFT...")
    sell_nft = xrpl.models.transactions.OfferCreate(
        account=hot_wallet.classic_address,
        taker_pays = "100000000",
        taker_gets = xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=amt_for_sale
        ),
        memos=[xrpl.models.transactions.Memo(memo_data=memo_data, memo_type=memo_type)]
    )

    sell_nft_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=sell_nft,
        wallet=hot_wallet,
        client=client,
    )

    response = xrpl.transaction.send_reliable_submission(sell_nft_prepared, client)
    print(response.result)
    print("Transaction Succeded! Here's the ledger hash: "+response.result.get('hash'))
    print("==============================================")

def buy_nft_after_offer_create(buyer, currency_code, nft_issuer_classic_address, amt_for_sale):
    print("BUYING THE NFT....")
    buy_nft = xrpl.models.transactions.OfferCreate(
        account=buyer.classic_address,

        taker_gets = "100000000",

        taker_pays = xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=nft_issuer_classic_address,
            value=amt_for_sale
        ),

        memos=[xrpl.models.transactions.Memo(memo_data=memo_data, memo_type=memo_type)]
    )

    buy_nft_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=buy_nft,
        wallet=buyer,
        client=client,
    )

    response = xrpl.transaction.send_reliable_submission(buy_nft_prepared, client)
    print(response.result)
    print("Transaction Succeded! Here's the ledger hash: "+response.result.get('hash'))
    print("==============================================")


def str_to_hex(string):
    return ''.join([hex(ord(c))[2:].zfill(2) for c in string])

# 0.000000000000000000000000000000000000000000000000000000000000000000000000000000031 = 31
def nftval_to_sci(amt):
    return str(amt/1000000000000000000000000000000000000000000000000000000000000000000000000000000000)

#Issuer
cold_wallet = generate_faucet_wallet(client, debug=True)

# Distributor
hot_wallet = generate_faucet_wallet(client, debug=True)

currency_code = "4e617468616e6973746865626573740000000000".upper()
print(currency_code)

issue_quantity = nftval_to_sci(10)
sell_quantity = nftval_to_sci(1)

memo_data = str_to_hex("testingminting")
memo_type = str_to_hex("text")

mint_nft_on_xrpl(cold_wallet, hot_wallet, currency_code, issue_quantity, memo_data, memo_type)
sell_nft_after_minting(currency_code, cold_wallet, sell_quantity, hot_wallet)

buyer_wallet = generate_faucet_wallet(client, debug=True)

buy_nft_after_offer_create(buyer_wallet, currency_code, cold_wallet.classic_address, sell_quantity)
