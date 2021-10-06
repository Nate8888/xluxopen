import React from 'react'
import { navigate } from '@reach/router'
import Loading from '../loading'

import NFTSample from '../../assets/test-img.jpeg'

import './detail.css'

class Detail extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true
        }
        this.buy = this.buy.bind(this)
    }

    componentDidMount() {
        setTimeout(() => {
            this.setState({ loading: false })
        }, 2500)
    }

    buy() {
        this.setState({ loading: true })
        setTimeout(() => {
            navigate("/")
        }, 2500)
    }

    render() {
        const item = this.props.location.state
        console.log(this.props.location)

        return (
            <div className="detail-container">
                {this.state.loading && <Loading />}
                <div className="detail auto">
                    <div className="nft-preview-wrapper">
                        <img src={item.filePreview} alt="NFT Preview" />
                    </div>

                    <div className="right-detail">
                        <div className="name">{item.name}</div>
                        <div className="d">{item.description}</div>
                        <div className="price">XRP {item.price}</div>
                        <div className="available">{item.available} Available</div>
                        <div className="owner">
                            <img src={NFTSample} alt="NFT Owner" />
                            <p>{item.ownerAddr}</p>
                        </div>
                        <div className="history">
                            <p>Minted on October 5th</p>
                            <small>This token does not have prior history of purchases</small>
                        </div>
                        <button className="buy-btn" onClick={this.buy}>Purchase now</button>
                    </div>
                </div>
            </div>
        )
    }
}

export default Detail;
