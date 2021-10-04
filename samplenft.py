import xrpl

# Connect to the xrpl testnet
xrpl_client = xrpl.Client('wss://test.xrp.xpring.io/sock')

# Get the current ledger sequence
ledger_sequence = xrpl_client.get_ledger_sequence()
print(ledger_sequence)

# Get the current fee
fee = xrpl_client.get_current_fee()
print(fee)


# Write a function that mints a NFT in the xrpl testnet
def mint_nft(address, secret, token_id, token_name, token_desc):
    # Create a payment transaction
    payment = xrpl.Payment(
        destination=address,
        amount=xrpl.drops_to_xrp(1),
        destination_tag=xrpl.random_uint32(),
        currency='XRP'
    )
    # Create a trustline transaction
    trustline = xrpl.TrustSet(
        account=address,
        currency='NFT',
        limit='0',
        quality_in='1',
        quality_out='1'
    )
    # Create a NFT token
    nft_token = xrpl.NFToken(
        token_id=token_id,
        token_name=token_name,
        token_desc=token_desc
    )
    # Create a transaction that includes the NFT
    transaction = xrpl.Transaction(
        source_address=address,
        sequence=xrpl.random_uint32(),
        fee=xrpl.drops_to_xrp(1),
        last_ledger_sequence=ledger_sequence,
        payment=payment,
        trustline=trustline,
        nft_token=nft_token
    )
    # Sign the transaction
    transaction.sign(secret)
    # Submit the transaction
    return xrpl_client.submit(transaction)

# Write a function that sends a payment with an NFT in the xrpl testnet
def send_nft_payment(address, secret, destination, token_id):
    # Create a payment transaction
    payment = xrpl.Payment(
        destination=destination,
        amount=xrpl.drops_to_xrp(1),
        destination_tag=xrpl.random_uint32(),
        currency='XRP'
    )
    # Create a transaction that includes the NFT
    transaction = xrpl.Transaction(
        source_address=address,
        sequence=xrpl.random_uint32(),
        fee=xrpl.drops_to_xrp(1),
        last_ledger_sequence=ledger_sequence,
        payment=payment,
        nft_set_token=xrpl.NFToken(
            token_id=token_id
        )
    )
    # Sign the transaction
    transaction.sign(secret)
    # Submit the transaction
    return xrpl_client.submit(transaction)


# Mint an NFT
nft_id = 'NFT' + str(xrpl.random_uint64())
nft_name = 'Nathan'
nft_desc = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
mint_nft(
    address='rPEPPER7kfTD9w2To4CQkQZBhjuhCpz9qt',
    secret='ssJcxvGXGn11pT7R3v7y2Xwf3m2iYaY0WVRpVvSJG5EaEqVFBcK',
    token_id=nft_id,
    token_name=nft_name,
    token_desc=nft_desc
)

# Send the NFT to a different address
send_nft_payment(
    address='rPEPPER7kfTD9w2To4CQkQZBhjuhCpz9qt',
    secret='ssJcxvGXGn11pT7R3v7y2Xwf3m2iYaY0WVRpVvSJG5EaEqVFBcK',
    destination='r4H3FsyfPcXCZL34iNMY6XqaiXfLz8U4e2Y',
    token_id=nft_id
)

# Get the NFT
nft = xrpl_client.get_nft(nft_id)
print(nft)

# Get the NFTs owned by a specific address
nfts = xrpl_client.get_nfts(address='r4H3FsyfPcXCZL34iNMY6XqaiXfLz8U4e2Y')
print(nfts)
