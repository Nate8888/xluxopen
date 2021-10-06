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
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/painting.gif?alt=media&token=e5dc45d2-e861-4d3e-b36a-335db72fe1e3",
                    name: 'Creating $1M NFTs from scratch with Beeple',
                    description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x8920',
                    available: 2,
                    price: 0.5
                },
                {
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/basketball_nft.gif?alt=media&token=c0a871cb-def7-440f-902f-d4d2004f22b1",
                    name: 'Basketball Techniques with LeBron James',
                    description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x11e9',
                    available: 3,
                    price: 219
                },
                {
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/bts.gif?alt=media&token=836d4497-4a73-404d-80f4-ab6cc2d584e1",
                    name: 'Exclusive behind the scenes from TBBT',
                    description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x7812',
                    available: 1,
                    price: 100
                },
                {
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/cooking.gif?alt=media&token=581a3605-0c38-4294-86f3-adb879173200",
                    name: 'Cooking side by side with Daniel Chang',
                    description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x2911',
                    available: 10,
                    price: 120
                },
                {
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/prog.gif?alt=media&token=b19ffa74-2b2d-474c-9890-f065e9a310df",
                    name: 'Early Internet Specs and Ideas with TBerners Lee',
                    description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x1ef4',
                    available: 5,
                    price: 600
                },
                {
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/xrpl-nate.appspot.com/o/makeup.gif?alt=media&token=ad8b9933-1e42-4d3f-80c9-a343580e8ede",
                    name: 'Oscar-Winning Make-Up Technique with S. Howard',
                    description: 'Ut enim ad minima veniam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x2911',
                    available: 10,
                    price: 120
                },
                {
                    filePreview: "https://firebasestorage.googleapis.com/v0/b/xrpl-nate.appspot.com/o/mrbeast.gif?alt=media&token=465b1dcf-7509-46f0-80eb-b80c8bc4e862",
                    name: 'Million dollar insights with Mr. Beast',
                    description: 'Ut enim ad minima veniam, quis nostrum exercitationem ullam',
                    ownerImg: NFTSample,
                    ownerAddr: '0x2911',
                    available: 10,
                    price: 120
                },
            ]
        }

        this.videoRef = React.createRef()
    }

    componentDidMount() {
        window.addEventListener("click", () => {
            if (this.videoRef && this.videoRef.current) this.videoRef.current.play()
        })

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
                            <video ref={this.videoRef} loop src="https://firebasestorage.googleapis.com/v0/b/test-385af.appspot.com/o/main_xrpl.mp4?alt=media&token=87554c8f-fff3-402d-9e46-1b3604cd0fb9">
                            </video>
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
                    <img src={item.filePreview} alt="NFT Thumbnail" />
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
