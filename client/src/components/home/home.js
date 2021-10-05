import React from 'react'
import { navigate } from '@reach/router'

import NFTSample from '../../assets/test-img.jpeg'
import DavidChang from '../../assets/david-chang.png'
import DanielS from '../../assets/ds.png'
import LBJames from '../../assets/lbj.png'
import MRBeast from '../../assets/mr-beast.png'
import TBLee from '../../assets/tim-berners-lee.png'
import WBuffett from '../../assets/wb.png'
import SBlakely from '../../assets/sara-blakely.png'

import './home.css'

class Home extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            // @warning: development only
            // uncomment for production since we'll be retrieving
            // NFTs from XRPL
            title: 'information',
            titleIx: 0,
            items: [
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 2,
                    price: 0.5
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 3,
                    price: 219
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 1,
                    price: 100
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 10,
                    price: 120
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 5,
                    price: 600
                }
            ]
        }
    }

    componentDidMount() {
        setInterval(() => {
            const words = ["techniques", "strategies", "experiences", "theories", "information"]
            const ix = (this.state.titleIx + 1) % words.length;
            this.setState({ titleIx: ix, title: words[ix] })
        }, 2000)
    }

    render() {
        // Formatting items into our own Thumbnails
        let items = <p>Loading...</p>
        if (this.state.items && this.state.items.length > 0) {
            items = this.state.items.map((i, ix) => (
                <NFTThumbnail item={i} key={ix} />
            ))
        }

        return (
            <div className="home-container">
                <div className="showcase-container">
                    <div className="showcase">
                        <div className="left">
                            <h1>A one-stop shop for <span className="gradient">exclusive</span> {this.state.title}</h1>
                            <p>From never-before-seen behind the scenes to award winning investing and basketball
                            techniques, at X you will be Y.</p>
                        </div>
                        <div className="right">
                            <p>video here</p>
                        </div>
                    </div>
                </div>
                <div className="home auto">
                    <div className="search-by">
                        <h2>Select a category</h2>
                        <div className="cats">
                            <div className="checkbox">Behind The Scenes</div>
                            <div className="checkbox">VIP Experience with Influencers</div>
                            <div className="checkbox">Investing</div>
                            <div className="checkbox">Art</div>
                            <div className="checkbox">Sports</div>
                            <div className="checkbox">Math and Physics</div>
                            <div className="checkbox">Music</div>
                            <div className="checkbox">Programming</div>
                        </div>
                    </div>
                    <div className="pics">
                        <h2>Browse partners</h2>
                        <div className="partners">
                            <div>
                                <img src={DavidChang} alt="partner" />
                                <p>Cooking Live with David Chang</p>
                            </div>
                            <div>
                                <img src={DanielS} alt="partner" />
                                <p>Technical Interview questions with Daniel Shiffman</p>
                            </div>
                            <div>
                                <img src={SBlakely} alt="partner" />
                                <p>Sara Blakely's process to make millions</p>
                            </div>
                            <div>
                                <img src={LBJames} alt="partner" />
                                <p>Basketball Techniques with LeBron James</p>
                            </div>
                            <div>
                                <img src={MRBeast} alt="partner" />
                                <p>Inside MrBeast's brain and house with MrBeast</p>
                            </div>
                            <div>
                                <img src={TBLee} alt="partner" />
                                <p>Early Internet Specs with Tim-Berners Lee</p>
                            </div>
                            <div>
                                <img src={WBuffett} alt="partner" />
                                <p>Exclusive Investing techniques with Warren Buffett</p>
                            </div>
                        </div>
                    </div>
                    <div className="marketplace">
                        <h2>Browse <span className="gradient">Never-before-seen</span> Techniques and Experiences</h2>
                        <div className="mp">
                            {items}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

class NFTThumbnail extends React.Component {
    render() {
        const { item } = this.props
        const state = { ...item }

        return (
            <div className="thumbnail" onClick={() => navigate('/nft/3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy/725308942', { state })}>
                <div className="img-wrapper">
                    <img src={item.filePreview} alt="NFT Thumbnail"/>
                </div>
                <div className="info">
                    <p className="name">{item.name}</p>
                    <p className="d">{item.description}</p>
                    <footer>
                        <div className="left">
                            <img src={item.ownerImg} />
                            <p>{item.ownerAddr}</p>
                        </div>
                        <div className="right">
                            <p>{item.available} avail.</p>
                        </div>
                    </footer>
                    <p className="price">XRP {item.price}</p>
                </div>
            </div>
        )
    }
}

export default Home;
