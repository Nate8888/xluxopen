import React from 'react'

import NFTSample from '../../assets/test-img.jpeg'

import './home.css'

class Home extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            // @warning: development only
            // uncomment for production since we'll be retrieving
            // NFTs from XRPL
            items: [
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 2
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 3
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 1
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 10
                },
                {
                    filePreview: NFTSample,
                    name: 'A Chihuahua',
                    description: 'Chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha chihuaha',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 5
                }
            ]
        }
    }
    render() {
        // Formatting items into our own Thumbnails
        let items = <p>Loading...</p>
        if (this.state.items && this.state.items.length > 0) {
            items = this.state.items.map((i, ix) => (
                <NFTThumbnail item={i} />
            ))
        }
        return (
            <div className="home-container">
                <div className="showcase-container">
                    <div className="showcase">
                        <div className="left">
                            <h1>A first-stop shop for <span className="gradient">exclusive</span> information</h1>
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

        return (
            <div className="thumbnail">
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
                </div>
            </div>
        )
    }
}

export default Home;
