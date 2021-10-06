import React from 'react';
import { navigate } from '@reach/router'
import Loading from '../loading'
import { addNFTToDB } from '../../firebase'

import NFTSample from '../../assets/test-img.jpeg'

import './mint.css'

class Mint extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            creator_addr: '0x8920',
            creator_uid: '',
            nft_name: '',
            nft_description: '',
            nft_price: '',
            nft_period: '',
            nft_quantity: '',
            nft_file: '',
            noun: 'community',
            dollars: 0,
            loading: true
        }

        this.XRPL_USD_RATE = 2000;

        this.create = this.create.bind(this)
        this.onChangeNFTName = this.onChangeNFTName.bind(this)
        this.onChangeNFTFile = this.onChangeNFTFile.bind(this)
        this.onChangeNFTPrice = this.onChangeNFTPrice.bind(this)
        this.onChangeNFTPeriod = this.onChangeNFTPeriod.bind(this)
        this.onChangeNFTQuantity = this.onChangeNFTQuantity.bind(this)
        this.onChangeNFTDescription = this.onChangeNFTDescription.bind(this)
    }

    componentDidMount() {
        // const nouns = ['fans', 'listeners', 'viewers', 'community']
        // let ix = 0
        // setInterval(() => {
        //     this.setState({ noun: nouns[ix] }, () => {
        //         ix = ++ix % nouns.length
        //     })
        // }, 2000)
        setTimeout(() => {
            this.setState({ loading: false })
        }, 2000)
    }

    onChangeNFTName(e) {
        this.setState({ nft_name: e.target.value })
    }

    onChangeNFTDescription(e) {
        this.setState({ nft_description: e.target.value })
    }

    onChangeNFTPrice(e) {
        const val = e.target.value
        this.setState({ nft_price: val, dollars: (val * this.XRPL_USD_RATE).toFixed(2) })
    }

    onChangeNFTPeriod(e) {
        this.setState({ nft_period: e.target.value })
    }

    onChangeNFTQuantity(e) {
        // For testing purposes, let's limit the max num
        // of tokens to be created at once (i.e. in a batch) to be 5.
        let val = e.target.value
        if (val > 5) val = 5
        this.setState({ nft_quantity: val })
    }

    onChangeNFTFile(e) {
        this.setState({ nft_file: e.target.value })
    }

    async create() {
        // if (this.state.nft_price <= 0) return;
        // if (this.state.nft_period <= 0) return;
        // if (this.state.nft_quantity <= 0) return;

        const tokenInfo = {
            name: this.state.nft_name,
            description: this.state.nft_description,
            price: this.state.nft_price,
            valid_for_days: this.state.nft_period,
            quantity: this.state.nft_quantity,
            // image: this.state.nft_file_link,
            // @warning: dev purposes only (comment before pushing to production):
            image: 'https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/chi.jpeg?alt=media&token=6559c4da-fbe9-410f-b779-3ce03172da1b'
        }

        this.setState({ loading: true })
        addNFTToDB
        .then(url => {
            // API call here (to submit file URL)

            // To prevent multiple requests.
            setTimeout(() => {
                navigate("/")
            }, 2500)
        })
        .catch(error => {
            console.log("Error uploading file:")
            console.log(error)
        })
    }

    render() {
        return (
            <div className='mint-container'>
                {this.state.loading && <Loading />}
                <div className="showcase-container">
                    <div className="showcase">
                        <h2 className='create-title'>Let's create <span className='gimme-border'>your token</span></h2>
                        <p className='sub-title'>A description bla bla bla yuca yuca yuca yca ya y a 😊</p>
                    </div>
                </div>
                <div className='mint auto'>
                    <div className='left'>
                        <div className='block'>
                            <label>What is your token name? Be truthful and creative!</label>
                            <input
                                value={this.state.nft_name}
                                onChange={this.onChangeNFTName}
                                type='text'
                                placeholder='nft nameee...'
                            />
                        </div>

                        <div className='block'>
                            <label>Could you give your buyers a short description about what's contained in your NFT?</label>
                            <input
                                value={this.state.nft_description}
                                onChange={this.onChangeNFTDescription}
                                type='text'
                                placeholder='nft description...'
                            />
                        </div>

                        <div className='block'>
                            <label>How much are you selling your token for?</label>
                            <div className='price-info'>
                                <input
                                    value={this.state.nft_price}
                                    onChange={this.onChangeNFTPrice}
                                    type='number'
                                    placeholder='12 XRP'
                                />
                                <span className='eth-symbol'>XRP</span>
                                {this.state.nft_price !== 0 && (
                                    <span className='dollars'>(~ ${this.state.dollars})</span>
                                )}
                            </div>
                        </div>

                        <div className='block'>
                            <label>How many tokens would you like to create?</label>
                            <input
                                value={this.state.nft_quantity}
                                onChange={this.onChangeNFTQuantity}
                                type='number'
                                placeholder='5 tokens for now'
                            />
                        </div>

                        <div className='block'>
                            <label>Upload your token file</label>
                            <div className="file-input-wrapper">
                                Upload file
                                <input
                                    onChange={this.onChangeNFTFile}
                                    type='file'
                                    placeholder='https://somewhere.com/token.jpg'
                                />
                            </div>
                        </div>

                        <button onClick={this.create} className='create-btn'>Mint NFT</button>
                    </div>
                    <div className='right'>
                        <p className='preview-title'>Your NFT 👇</p>
                        <div className='item'>
                            <div className='image-wrapper'>
                                <img
                                    src={this.state.nft_file || 'https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/test-img.jpeg?alt=media&token=1a6d4d4d-8337-43c0-9c09-29f85b5c38a4'}
                                    alt='Token preview'
                                    className="nft-img"
                                />
                            </div>
                            <p className='name'>{this.state.nft_name || 'A ticket to paradise'}</p>
                            <p className='desc'>{this.state.nft_description || 'Never-before-seen behind the scenes of the Big Bang Theory'}</p>
                            <p className='price'>{this.state.nft_price ? this.state.nft_price +  ' XRP' : '15 XRP'}</p>
                            <p className='owner'>
                                <img src={NFTSample} alt="Owner" />
                                <span>{this.state.creator_addr}</span>
                            </p>
                            <p className='quantity'>{this.state.nft_quantity || '30'} tickets available</p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Mint;
