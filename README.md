## xLux - Decentralized Knowledge Exchange


<!-- Description -->

##### xLux is a decentralized knowledge exchange platform that enables creators and communities to grow, engage, and improve by providing an easy way to exchange “Knowledge NFTs” containing exclusive content such as techniques, strategies, theories, and experiences.

<hr>

## Table of Contents
  - [Features](#features)
  - [Getting Started](#getting-started)
  - [Reset Wallets](#reset-wallets)
  - [Mint NFT](#mint-nft)
  - [Sell NFT](#sell-nft)
  - [Buy NFT](#buy-nft)
  - [Accept Buy Offer](#accept-buy-offer)
  - [Accept Sell Offer](#accept-sell-offer)
  - [Cancel Buy Offer](#cancel-buy-offer)
  - [Cancel Sell Offer](#cancel-sell-offer)
  - [Get NFT Data from IPFS](#get-nft-data-from-ipfs)
  - [List Account NFTs](#list-account-nfts)
  - [List Account NFT Offers](#list-account-nft-offers)
  - [List Account NFT Buy Offers](#list-account-nft-buy-offers)
  - [List All xLux Accounts](#list-all-xlux-accounts)
  - [List All NFTs in xLux](#list-all-nfts-in-xlux)
  - [List All NFT Offers in xLux](#list-all-nft-offers-in-xlux)
  - [Append Address to Database](#append-address-to-database)

<hr>

## Features
- Mint, Sell, Purchase, Cancel and Exchange NFTs in the Ripple Ledger using the latest XLS-20 standard
- Check the latest offers and bids for NFTs with all addresses registered
- Sign & Submit transactions asyncronously
- Decentralized file storage system using IPFS & NFT.Storage
- Simulate Account Generation and Transaction Execution
- Easy to use API for implementing the XLS-20 standard in a python script
<hr>

## Getting Started

#### To first get started with the functional demo, you need to clone the project using git.
<br>

```
1. git clone https://github.com/Nate8888/xluxopen.git
```

#### Now go inside the project folder `xluxopen` and run the following command to install the dependencies (python 3+ required)
<br>

```
2. pip install -r requirements.txt
```

#### Now you have to create an NFT.Storage account and put the API Key in the `.env` file.
<br>

```
3. IPFS_KEY=KEY_HERE
```

#### Now you can run the following command to fire up the demo.
<br>

```
4. python3 xluxApiDemo.py
```

#### A request creator tool like CURL, Postman, or Swagger can be used to experiment with the API.
<hr>

# API

<!-- Make an API table -->
## Reset Wallets

All API requests interact with NFT-Devnet wallets that are currently stored in memory. You are able to change the default wallets in the API and you are also able to generate complete new ones throughout the demo.

<br>

Sets the account for the NFT issuer:
```http
POST /set_seller_account
```

Body Parameter:

```json
{
    "secret": "NFT-Devnet-Secret"
    "sequence": "NFT-Devnet-Sequence"
    "address": "NFT-Devnet-Address"
}
```

<br>

Sets the account for the NFT Buyer:
```http
POST /set_buyer_account
```

Body Parameter:

```json
{
    "secret": "NFT-Devnet-Secret"
    "sequence": "NFT-Devnet-Sequence"
    "address": "NFT-Devnet-Address"
}
```

<br>

Generate two random accounts to act as the NFT issuer and buyer:

```http
POST /generate_accounts
```

<hr>

## Mint NFT

Mint an NFT to the NFT issuer's account.

<br>

```http
POST /mint
```

Form Parameter:

```json
    "name": "NFT-Name"
    "description": "NFT-Description"
    "sellprice": "NFT-Sell-Price"
```

<br>

File Parameter:

```json
    "files[]": "NFT-Image"
```

<hr>




## Sell NFT

Sell an NFT to the NFT buyer's account.

<br>

```http
POST /sell-nft
```

Form Parameter:

```json
    "NFTokenID": "NFT-Token-ID"
    "sellprice_in_xrp": "NFT-Sell-Price"
```

<hr>




## Buy NFT

Buy an NFT from the NFT issuer's account.

<br>

```http
POST /buy-nft
```

Form Parameter:

```json
{
    "NFTokenID": "NFT-Token-ID",
    "buyprice_in_xrp": "NFT-Buy-Price"
}
```

<hr>


## Accept Buy Offer

Accept a buy offer for an NFT.

<br>

```http
POST /accept_buy_offer
```

Form Parameter:

```json
{
    "buy_offer_index": "NFT-Buy-Offer-Index"
}
```

<hr>




## Accept Sell Offer

Accept a sell offer for an NFT.

<br>

```http
POST /accept_sell_offer
```

Form Parameter:

```json
{
    "sell_offer_index": "NFT-Sell-Offer-Index"
}
```

<hr>




## Cancel Buy Offer

Cancel a buy offer for an NFT.

<br>

```http
POST /cancel_buy_offer
```

Form Parameter:

```json
{
    "buy_offer_index": "NFT-Buy-Offer-Index"
}
```

<hr>




## Cancel Sell Offer

Cancel a sell offer for an NFT.

<br>

```http
POST /cancel_sell_offer
```

Form Parameter:

```json
{
    "sell_offer_index": "NFT-Sell-Offer-Index"
}
```

<hr>




## Get NFT Data from IPFS

Get NFT data from IPFS.

<br>

```http
GET /get-nft-data-ipfs
```

Query Parameter:

```json
{
    "url": "ipfs.io/ipfs/<hash>/metadata.json"
}
```

<hr>




## List Account NFTs

List all NFTs in an account.

<br>

```http
GET /list-acc-nfts
```

<hr>




## List Account NFT Offers

List all sell offers in a NFT.

<br>

```http
GET /list-acc-sell-nft-offers
```

Form Parameter:

```json
{
    "NFTokenID": "NFT-Token-ID"
}
```

<hr>




## List Account NFT Buy Offers

List all NFT buy offers in an account.

<br>

```http
GET /list-acc-nft-buy-offers
```

Form Parameter:

```json
{
    "NFTokenID": "NFT-Token-ID"
}
```

<hr>




## List All xLux Accounts

List all accounts registered in the xLux platform.

<br>

```http
GET /list-all-xlux-accs
```

<hr>




## List All NFTs in xLux

List all NFTs in the xLux platform.

<br>

```http
GET /list-all-nfts-in-xlux
```

<hr>




## List All NFT Offers in xLux

List all NFT offers in the xLux platform.

<br>

```http
GET /list-all-nft-offers-in-xlux
```

<hr>




## Append Address to Database

Append an address to the database.

<br>

```http
POST /append-add-to-db
```

Body Parameter:

```json
{
    "address": "NFT-Devnet-Address"
}
```

<hr>