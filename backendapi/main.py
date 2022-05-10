import time
import json
import math
import xrpl
import string
import random
import requests
import datetime
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from flask_cors import CORS, cross_origin
from xrpl.wallet import generate_faucet_wallet
from flask import Flask, render_template, request, jsonify, redirect

cred = credentials.Certificate('ripplecred.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# When an NFT is being sold, we add it to the database in order to display them
def add_nft_sale(transaction_hash, name, desc, sellprice, amt, url, issuer, currencycode, sciamt, memodata, memotype):
    doc_ref = db.collection('nfts').document(transaction_hash)
    doc_ref.set({
        'name': name,
        'description': desc,
        'sellprice': sellprice,
        'amount': 1,
        'url': url,
        'transactionhash': transaction_hash,
        'issuer': issuer,
        'currencycode':currencycode,
        'scientificamount': sciamt,
        'memodata' : memodata,
        'memotype' : memotype
    })

# When a NFT is sold, we remove it from our records
def delete_nft_from_sale(transaction_hash):
    doc_ref = db.collection("nfts").document(transaction_hash)
    doc_ref.delete()

# List all NFTs to show in our "front page"
def query_for_all_nfts():
    all_nfts = db.collection('nfts').stream()
    list_of_all_nfts = []
    for nft in all_nfts:
        data = nft.to_dict()
        list_of_all_nfts.append(data)
    return list_of_all_nfts

# Connection Setup
testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)
faucet_url = "https://faucet.altnet.rippletest.net/accounts"

def get_unix_time(days=0, hours=0, minutes=0, seconds=0):
    return int(time.time())

# Creates a random string with letters and numbers with default length of 8.
def randomStringDigits(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

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
    #print(response)

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
    #print(response)


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
    #print(response)


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

    nft_minting_transaction_hash = response.result.get("hash") # Going to send this back to the json
    #print(response)

    # Check balances ---------------------------------------------------------------
    print("Getting hot address balances...")
    response = client.request(xrpl.models.requests.AccountLines(
        account=hot_wallet.classic_address,
        ledger_index="validated",
    ))
    #print(response)

    print("Getting cold address balances...")
    response = client.request(xrpl.models.requests.GatewayBalances(
        account=cold_wallet.classic_address,
        ledger_index="validated",
        hotwallet=[hot_wallet.classic_address]
    ))
    #print(response)

    return nft_minting_transaction_hash

def sell_nft_after_minting(currency_code, cold_wallet, amt_for_sale, hot_wallet, price_in_XRPs, memo_data, memo_type):

    sell_nft = xrpl.models.transactions.OfferCreate(
        account=hot_wallet.classic_address,
        taker_pays = str(int(price_in_XRPs * 1_000_000) ), #normalize XRP value
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
    return [response.result.get("hash"), response.result.get("TakerGets").get("value")]

def buy_nft_after_offer_create(buyer, currency_code, nft_issuer_classic_address, amt_for_sale, price_in_XRPs, memo_data, memo_type):
    buy_nft = xrpl.models.transactions.OfferCreate(
        account=buyer.classic_address,
        taker_gets = str(int(price_in_XRPs * 1_000_000) ),
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
    return response.result.get("hash")

def reset_cold_wallet():
    global cold_wallet
    cold_wallet = generate_faucet_wallet(client, debug=True)

def reset_hot_wallet():
    global hot_wallet
    hot_wallet = generate_faucet_wallet(client, debug=True)

def reset_buyer_wallet():
    global buyer_wallet
    buyer_wallet = generate_faucet_wallet(client, debug=True)

def str_to_hex(string):
    return ''.join([hex(ord(c))[2:].zfill(2) for c in string])

# 0.000000000000000000000000000000000000000000000000000000000000000000000000000000031 = 31
def nftval_to_sci(amt):
    return str(amt/1000000000000000000000000000000000000000000000000000000000000000000000000000000000)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Wallets that are currently stored in memory for the sake of the demo
cold_wallet = None # Issuer
hot_wallet = None # Distributor
buyer_wallet = None # Wallet Buying the asset

@app.route('/mint', methods=['POST'])
@cross_origin()
def mint():
    base_xrpl_url = "https://explorer-testnet.xrplf.org/tx/"
    name = request.form.get('name')
    desc = request.form.get('description')
    amount_in_xrp = request.form.get('sellprice')
    sell_amt = request.form.get('amount') # Only Integer values
    URL = request.form.get('url')

    # Prepare request
    hex_currency_code = str_to_hex(name)

    # Creates a HEX currency code based on the name given on the request
    # Adds zeroes at the end if the str is less than 40
    currency_code = (hex_currency_code + hex_currency_code.zfill(40).split(hex_currency_code)[0]).upper()

    # Transforms the amount of NFTs to mint into scientific notation based on NFT proposal on GitHub
    issue_quantity = nftval_to_sci(int(sell_amt))

    # Creates the memo of the NFT
    memo_data = str_to_hex(desc + "\nurl: " + URL) # Adds description to one of the memo fields
    memo_type = str_to_hex("text")

    # If the cold_wallet or hot_wallet are not available, we shall reset them.
    if cold_wallet == None or hot_wallet == None:
        reset_hot_wallet()
        reset_cold_wallet()

    total_price_in_xrp = int(sell_amt) * float(amount_in_xrp)

    # Issuer is going to Issue the NFT minting to the hot_wallet.
    # Hot wallet will hold a balance of the respective NFT in the ledger
    tx_hash  = mint_nft_on_xrpl(cold_wallet, hot_wallet, currency_code, issue_quantity, memo_data, memo_type)
    final_transaction_url_on_ledger = base_xrpl_url + tx_hash

    # Now after we minted the asset, we will automatically list it for sale using OfferCreate
    sell_hash, normalized_quantity = sell_nft_after_minting(currency_code, cold_wallet, issue_quantity, hot_wallet, total_price_in_xrp, memo_data, memo_type)
    final_sale_on_ledger = base_xrpl_url + sell_hash


    # Add the NFT to the database so we can list them in the website later
    add_nft_sale(sell_hash, name, desc, amount_in_xrp, sell_amt, URL, cold_wallet.classic_address, currency_code, normalized_quantity, memo_data, memo_type)

    res = {'mintingTransaction':final_transaction_url_on_ledger, 'NFTOwnerAccount': hot_wallet.classic_address, 'saleTransaction':final_sale_on_ledger}
    return jsonify(res)

# Buys the specified NFT
@app.route('/buy', methods=['POST'])
@cross_origin()
def simulate_buying():
    base_xrpl_url = "https://explorer-testnet.xrplf.org/tx/"
    transactionhash = request.form.get('transactionhash')
    nft_issuer_classic_address = request.form.get('issueraddress')
    currency_code = request.form.get('currencycode')
    amt_for_sale = request.form.get('amount')
    price_in_XRPs = float(request.form.get('sellprice'))
    memo_data = request.form.get('memodata')
    memo_type = request.form.get('memotype')

    if buyer_wallet == None:
        reset_buyer_wallet()

    print("Starting Buying Transaction: ")
    print(buyer_wallet, currency_code, nft_issuer_classic_address, amt_for_sale, price_in_XRPs, memo_data, memo_type)
    buying_transaction_hash = buy_nft_after_offer_create(buyer_wallet, currency_code, nft_issuer_classic_address, amt_for_sale, price_in_XRPs, memo_data, memo_type)
    final_transaction_url_of_nft_buy = base_xrpl_url + buying_transaction_hash

    # When we finish buying the NFT, we remove from the database because someone else owns it now.
    delete_nft_from_sale(transactionhash)
    res = {'buyingTransaction':final_transaction_url_of_nft_buy, 'buyerAddress': buyer_wallet.classic_address}
    return jsonify(res)


@app.route('/resetwallets', methods=['POST'])
@cross_origin()
def something_bugged():
    reset_hot_wallet()
    reset_cold_wallet()
    reset_buyer_wallet()
    res = {'status':'OK'}
    return jsonify(res)

@app.route('/getwallets', methods=['POST'])
@cross_origin()
def getwalletvals():
    if cold_wallet == None or hot_wallet == None or buyer_wallet == None:
        reset_hot_wallet()
        reset_cold_wallet()
        reset_buyer_wallet()

    res = {'issuer':cold_wallet.classic_address, 'distributor':hot_wallet.classic_address, 'buyer':buyer_wallet.classic_address}
    return jsonify(res)

@app.route('/nftsforsale', methods=['POST'])
@cross_origin()
def get_nfts_for_sale():
    all_nfts = query_for_all_nfts()
    res = {'data':all_nfts}
    return jsonify(res)

# Start Flask backend
if __name__ == '__main__':
    if cold_wallet == None or hot_wallet == None or buyer_wallet == None:
        reset_hot_wallet()
        reset_cold_wallet()
        reset_buyer_wallet()
    app.run(host='127.0.0.1', port=8080, debug=True)
