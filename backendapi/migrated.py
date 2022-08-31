from dataclasses import fields
import time
import json
import math
import xrpl
import string
import random
import requests
import datetime
import os
from flask_cors import CORS, cross_origin
from xrpl.wallet import generate_faucet_wallet
from flask import Flask, render_template, request, jsonify, redirect
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
upload_key = os.environ.get('IPFS_KEY', None)
client = xrpl.clients.JsonRpcClient("http://xls20-sandbox.rippletest.net:51234")

# testing & simulation purposes
acc_1 = {
    "address": "rw1fvZvrM4EBgUAVtmMpmxJ5bmfYDiFsH2",
    "secret": "sssUsQ7GTybcCb1TKycZpnxZJnra6",
    "sequence": 5206156,
}
acc_2 = {
    "address": "rs8RkpmzcyQT4kGfuDVbNUHkhFXU518KW3",
    "secret": "shXFfK4392ycL8oK6jiga4e4uWgzQ",
    "sequence": 5206177,
}

def append_new_user(address):
    # append new user to registered_users.json
    registered_users = []
    with open('registered_users.json', 'r') as f:
        registered_users = json.load(f)
    if address in registered_users:
        return False
    with open('registered_users.json', 'w') as f:
        registered_users.append(address)
        json.dump(registered_users, f)
    return True

def create_nft_mint(uri):
    sender_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    hex_uri = xrpl.utils.str_to_hex(uri)
    nft_object = xrpl.models.transactions.NFTokenMint(
        account=sender_wallet.classic_address,
        uri=hex_uri,
        flags=8,
        transfer_fee=0,
        nftoken_taxon=0
    )
    return nft_object, sender_wallet

def create_nft_sell_offer(NFTokenID, amount):
    sender_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    nft_create_sell_offer = xrpl.models.transactions.NFTokenCreateOffer(
        account=sender_wallet.classic_address,
        nftoken_id=NFTokenID,
        amount=amount,
        flags=1,

    )
    return nft_create_sell_offer, sender_wallet

def create_nft_buy_offer(NFTokenID, amount):
    buyer_wallet = xrpl.wallet.Wallet(seed=acc_2['secret'], sequence=acc_2['sequence'])
    seller_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    nft_create_buy_offer = xrpl.models.transactions.NFTokenCreateOffer(
        account=buyer_wallet.classic_address,
        owner=seller_wallet.classic_address,
        nftoken_id=NFTokenID,
        amount=amount
    )
    return nft_create_buy_offer, buyer_wallet

def create_nft_accept_buy_offer(offer_id):
    buyer_wallet = xrpl.wallet.Wallet(seed=acc_2['secret'], sequence=acc_2['sequence'])
    seller_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    nft_accept_buy_offer = xrpl.models.transactions.NFTokenAcceptOffer(
        account=seller_wallet.classic_address,
        nftoken_buy_offer=offer_id,
    )
    return nft_accept_buy_offer, seller_wallet

def create_nft_accept_sell_offer(offer_id):
    seller_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    buyer_wallet = xrpl.wallet.Wallet(seed=acc_2['secret'], sequence=acc_2['sequence'])
    nft_accept_sell_offer = xrpl.models.transactions.NFTokenAcceptOffer(
        account=buyer_wallet.classic_address,
        nftoken_sell_offer=offer_id,
    )
    return nft_accept_sell_offer, buyer_wallet

def create_nft_cancel_buy_offer(offer_id):
    buyer_wallet = xrpl.wallet.Wallet(seed=acc_2['secret'], sequence=acc_2['sequence'])
    seller_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    nft_cancel_buy_offer = xrpl.models.transactions.NFTokenCancelOffer(
        account=buyer_wallet.classic_address,
        nftoken_offers=[offer_id],
    )
    return nft_cancel_buy_offer, buyer_wallet

def create_nft_cancel_sell_offer(offer_id):
    seller_wallet = xrpl.wallet.Wallet(seed=acc_1['secret'], sequence=acc_1['sequence'])
    buyer_wallet = xrpl.wallet.Wallet(seed=acc_2['secret'], sequence=acc_2['sequence'])
    nft_cancel_sell_offer = xrpl.models.transactions.NFTokenCancelOffer(
        account=seller_wallet.classic_address,
        nftoken_offers=[offer_id],
    )
    return nft_cancel_sell_offer, seller_wallet

def get_account_nfts(add=acc_1['address']):
    nft_request = xrpl.models.requests.AccountNFTs(
        account=add,
    )
    acct_nfts = client.request(nft_request).result
    return acct_nfts

def get_account_nft_offers(NFTokenID):
    nft_request = xrpl.models.requests.NFTSellOffers(
        nft_id=NFTokenID,
    )
    nft_offers = client.request(nft_request).result
    return nft_offers

def get_account_nft_buy_offers(NFTokenID):
    nft_request = xrpl.models.requests.NFTBuyOffers(
        nft_id=NFTokenID,
    )
    nft_offers = client.request(nft_request).result
    return nft_offers

def tx_sign_submit(tx, sender_wallet):
    signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(tx, sender_wallet, client)
    max_ledger = signed_tx.last_ledger_sequence
    tx_id = signed_tx.get_hash()
    try:
        tx_response = xrpl.transaction.send_reliable_submission(signed_tx, client)
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        exit(f"Submit failed: {e}")
    print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    print(f"Explorer link: https://nft-devnet.xrpl.org/transactions/{tx_id}")
    metadata = tx_response.result.get("meta", {})
    sequence = tx_response.result.get("Sequence", None)
    if metadata.get("TransactionResult"):
        print("Result code:", metadata["TransactionResult"])
    if metadata.get("delivered_amount"):
        print("XRP delivered:", xrpl.utils.drops_to_xrp(
                    metadata["delivered_amount"]))
    return tx_response.result

def ipfs_upload(file_obj, nft_metadata):
    url = "https://api.nft.storage/store"
    data = {
        'meta': json.dumps(nft_metadata)
    }
    xlux_file = [
        ('image',(
                    file_obj.get('file_name'),
                    file_obj.get('file_data'),
                    file_obj.get('file_type')
                )
        )
    ]
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(upload_key)
    }
    response = requests.request("POST", url, headers=headers, data=data, files=xlux_file).json()
    print(response)
    if response.get('ok'):
        return response.get('value').get('url')
    else:
        raise Exception("Upload failed")

# gets the metadata from ipfs and returns it
def return_ipfs_metadata(url):
    response = requests.get(url)
    return response.json()

# Used to simulate seller-account in the devnet
@app.route('/set_seller_account', methods=['POST'])
def set_seller_account():
    global acc_1
    if not request.get_json() or not all(k in request.get_json() for k in ['secret', 'sequence', 'address']):
        return jsonify({'error': 'Missing parameters'}), 400
    acc_1 = request.get_json()
    return jsonify(acc_1)

# Used to simulate buyer-account in the devnet
@app.route('/set_buyer_account', methods=['POST'])
def set_buyer_account():
    global acc_2
    if not request.get_json() or not all(k in request.get_json() for k in ['secret', 'sequence', 'address']):
        return jsonify({'error': 'Missing parameters'}), 400
    acc_2 = request.get_json()
    return jsonify(acc_2)

# Used to simulate two accounts in the devnet
@app.route('/generate_accounts', methods=['POST'])
def generate_accounts():
    # Generate two accounts from the faucet and then save them in acc_1 and acc_2
    global acc_1, acc_2
    temp_1 = xrpl.wallet.generate_faucet_wallet(client=client)
    temp_2 = xrpl.wallet.generate_faucet_wallet(client=client)

    acc_1 = {
        'secret': temp_1.seed,
        'sequence': temp_1.sequence,
        'address': temp_1.classic_address,
    }

    acc_2 = {
        'secret': temp_2.seed,
        'sequence': temp_2.sequence,
        'address': temp_2.classic_address,
    }

    return jsonify({'account_1': acc_1, 'account_2': acc_2})


@app.route('/mint', methods=['POST'])
def mint_nft():
    fields = ['name', 'description', 'sellprice']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    if len(request.files) == 0:
        return jsonify({'error': 'Missing file'}), 400
    nft_meta = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'sellprice': request.form.get('sellprice'),
        'image': 'undefined', # needed for ipfs/nftstorage
    }
    file_uploaded = request.files['files[]']
    file_obj = {
        'file_name': file_uploaded.filename,
        'file_data': file_uploaded.read(),
        'file_type': file_uploaded.content_type,
    }
    try:
        ipfs_meta_url = ipfs_upload(file_obj, nft_meta)
        ipfs_meta_url = ipfs_meta_url.replace('ipfs://', 'ipfs.io/ipfs/')
        nft_object, sender_wallet = create_nft_mint(ipfs_meta_url)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'url': ipfs_meta_url, 'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sell-nft', methods=['POST'])
def sell_nft():
    fields = ['NFTokenID', 'sellprice_in_xrp']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    NFTokenID = request.form.get('NFTokenID')
    sellprice_in_xrp = xrpl.utils.xrp_to_drops(int(request.form.get('sellprice_in_xrp')))
    try:
        nft_object, sender_wallet = create_nft_sell_offer(NFTokenID, sellprice_in_xrp)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/buy-nft', methods=['POST'])
def buy_nft():
    fields = ['NFTokenID', 'buyprice_in_xrp']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    NFTokenID = request.form.get('NFTokenID')
    buyprice_in_xrp = xrpl.utils.xrp_to_drops(int(request.form.get('buyprice_in_xrp')))
    try:
        nft_object, sender_wallet = create_nft_buy_offer(NFTokenID, buyprice_in_xrp)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/accept_buy_offer', methods=['POST'])
def accept_buy_offer():
    fields = ['buy_offer_index']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    buy_offer_index = request.form.get('buy_offer_index')
    try:
        nft_object, sender_wallet = create_nft_accept_buy_offer(buy_offer_index)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/accept_sell_offer', methods=['POST'])
def accept_sell_offer():
    fields = ['sell_offer_index']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    sell_offer_index = request.form.get('sell_offer_index')
    try:
        nft_object, sender_wallet = create_nft_accept_sell_offer(sell_offer_index)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cancel_buy_offer', methods=['POST'])
def cancel_buy_offer():
    fields = ['buy_offer_index']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    buy_offer_index = request.form.get('buy_offer_index')
    try:
        nft_object, sender_wallet = create_nft_cancel_buy_offer(buy_offer_index)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cancel_sell_offer', methods=['POST'])
def cancel_sell_offer():
    fields = ['sell_offer_index']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    sell_offer_index = request.form.get('sell_offer_index')
    try:
        nft_object, sender_wallet = create_nft_cancel_sell_offer(sell_offer_index)
        try:
            tx_res = tx_sign_submit(nft_object, sender_wallet)
            tx_explorer = "https://nft-devnet.xrpl.org/transactions/" + tx_res.get('hash')
            acc_explorer = "https://nft-devnet.xrpl.org/accounts/" + tx_res['Account']
            return jsonify({'tx_exp':tx_explorer, 'acc_explorer':acc_explorer}), 200
        except xrpl.transaction.XRPLReliableSubmissionException as e:
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-nft-data-ipfs', methods=['GET'])
def get_nft_data_ipfs():
    fields = ['url']
    for f in fields:
        if f not in request.args or request.args[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    url = request.args.get('url')
    # if url is not a valid ipfs url, return error
    if url.startswith('ipfs://') == True:
        url = url.replace('ipfs://', 'http://ipfs.io/ipfs/')
    if url.startswith('http://ipfs.io/ipfs/') == False:
        try:
            url = xrpl.utils.hex_to_str(url)
            if url.startswith('ipfs://') == True:
                url = url.replace('ipfs://', 'http://ipfs.io/ipfs/')
            if url.startswith('http://ipfs.io/ipfs/') == False:
                return jsonify({'error': 'Invalid ipfs url'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    try:
        nft_data = return_ipfs_metadata(url)
        return jsonify({'nft_data':nft_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list-acc-nfts', methods=['GET'])
def list_acc_nfts():
    acc_nfts = get_account_nfts()
    return jsonify(acc_nfts), 200

@app.route('/list-acc-sell-nft-offers', methods=['GET'])
def list_acc_nft_offers():
    fields = ['NFTokenID']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    NFTokenID = request.form.get('NFTokenID')
    acc_nft_offers = get_account_nft_offers(NFTokenID)
    return jsonify(acc_nft_offers), 200

@app.route('/list-acc-buy-nft-offers', methods=['GET'])
def list_acc_nft_buy_offers():
    fields = ['NFTokenID']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    NFTokenID = request.form.get('NFTokenID')
    acc_nft_offers = get_account_nft_buy_offers(NFTokenID)
    return jsonify(acc_nft_offers), 200

# Simulated mode to show all accs registered
# this shows how we are doing it in the web platform
@app.route('/list-all-xlux-accs', methods=['GET'])
def list_all_xlux_accs():
    registered_users = []
    with open('registered_users.json') as f:
        registered_users = json.load(f)
    return jsonify(registered_users), 200

@app.route('/list-all-nfts-in-xlux', methods=['GET'])
def list_all_nfts_in_xlux():
    # get all registered_users
    registered_users = []
    with open('registered_users.json') as f:
        registered_users = json.load(f)
    # get all nfts in each user's account
    nfts = []
    for address in registered_users:
        nfts.extend(get_account_nfts(address).get('account_nfts'))
    return jsonify(nfts), 200

@app.route('/list-all-nft-offers-in-xlux', methods=['GET'])
def list_all_nft_offers_in_xlux():
    # get all registered_users
    registered_users = []
    with open('registered_users.json') as f:
        registered_users = json.load(f)
    # get all nfts in each user's account
    nfts = []
    for address in registered_users:
        nfts.extend(get_account_nfts(address).get('account_nfts'))
    
    nft_sell_offers = []
    nft_buy_offers = []
    for nft in nfts:
        if 'NFTokenID' in nft:
            res_arr = get_account_nft_offers(nft.get('NFTokenID'))
            res_arr2 = get_account_nft_buy_offers(nft.get('NFTokenID'))
            print(res_arr, res_arr2)
            if res_arr and res_arr.get('offers'):
                nft_sell_offers.extend(res_arr.get('offers'))
            if res_arr2 and res_arr2.get('offers'):
                nft_buy_offers.extend(res_arr2.get('offers'))
    return jsonify({'nft_sell_offers':nft_sell_offers, 'nft_buy_offers':nft_buy_offers}), 200


@app.route('/append-add-to-db', methods=['POST'])
def append_add_to_db():
    fields = ['address']
    for f in fields:
        if f not in request.form or request.form[f] == '':
            return jsonify({'error': 'Missing one or more fields'}), 400
    address = request.form.get('address')
    res = append_new_user(address)
    return jsonify({'success': str(res)}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)