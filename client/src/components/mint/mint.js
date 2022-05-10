import React from 'react';
import axios from 'axios'
import { navigate } from '@reach/router'

import Loading from '../loading/loading'
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
            uploadedFile: '',
            loading: true
        }

        this.XRPL_USD_RATE = 1.10;

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
        const sampleFile = "https://firebasestorage.googleapis.com/v0/b/xrpl-nate.appspot.com/o/makeup.gif?alt=media&token=ad8b9933-1e42-4d3f-80c9-a343580e8ede"
        setTimeout(() => {
            this.setState({ uploadedFile: sampleFile })
        }, 1500)
    }

    async create() {
        if (this.state.nft_price <= 0) return;
        if (this.state.nft_period <= 0) return;
        if (this.state.nft_quantity <= 0) return;

        const tokenInfo = {
            name: this.state.nft_name,
            description: this.state.nft_description,
            price: this.state.nft_price,
            valid_for_days: this.state.nft_period,
            quantity: this.state.nft_quantity,
            image: this.state.nft_file_link,
        }

        this.setState({ loading: true })

        const apiURL = "https://xlux.herokuapp.com/mint"

        // Adding to db
        addNFTToDB
        .then(url => {
            const bodyFormData = new FormData();
            bodyFormData.append("file_url_raw", url);

            // API call here (to submit file URL)
            axios({
                method: "post",
                url: apiURL,
                data: bodyFormData,
                headers: { "Content-Type": "multipart/form-data" },
            })
            .then(response => {
                // handle success
                console.log(response);
                setTimeout(() => {
                    // To prevent multiple subsequent requests to our API.
                    this.setState({ loading: false })
                }, 2000)
            })
            .catch(error => {
                // handle error
                console.log(error);
                setTimeout(() => {
                    // To prevent multiple subsequent requests to our API.
                    this.setState({ loading: false })
                }, 2000)
            });

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
        let iwclassname = "image-wrapper"
        iwclassname += this.state.uploadedFile ? '' : ' not'
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
                            <div className={iwclassname}>
                                {this.state.uploadedFile ? (
                                    <img
                                        src={this.state.uploadedFile}
                                        alt='Loading...'
                                        className="nft-img"
                                    />
                                ) : (
                                    <img
                                        src={this.state.nft_file || NFTSample}
                                        alt='Loading...'
                                        className="nft-img"
                                    />
                                )}
                            </div>
                            <p className='name'>{this.state.nft_name || 'A ticket to paradise'}</p>
                            <p className='desc'>{this.state.nft_description || 'Never-before-seen behind the scenes of the Big Bang Theory'}</p>
                            <p className='price'>{this.state.nft_price ? this.state.nft_price +  ' XRP' : '15 XRP'}</p>
                            <p className='owner'>
                                <img src={NFTSample} alt="Owner" />
                                <span>{this.state.creator_addr}</span>
                            </p>
                            <p className='quantity'>{this.state.nft_quantity || '30'} tokens available</p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Mint;
