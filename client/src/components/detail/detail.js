import React from 'react'
import NFTSample from '../../assets/test-img.jpeg'

import './detail.css'

class Detail extends React.Component {
    render() {
        const item = this.props.location.state
        console.log(this.props.location)

        return (
            <div className="detail-container">
                <div className="detail auto">
                    <div className="nft-preview-wrapper">
                        <img src={NFTSample} alt="NFT Preview" />
                    </div>

                    <div className="name">{item.name}</div>
                    <div className="d">{item.description}</div>
                    <div className="price">{item.price}</div>
                    <div className="available">{item.available}</div>
                    <div className="owner">
                        <img src={NFTSample} alt="NFT Owner" />
                        <p>{item.ownerAddr}</p>
                    </div>
                </div>
            </div>
        )
    }
}

export default Detail;
