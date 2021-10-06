import React from 'react'
import { navigate } from '@reach/router'

import XLUXLogo from '../../assets/xlux.svg'

import './header.css'

class Header extends React.Component {
    render() {
        return (
            <div className="header-container">
                <div className="header">
                    <p className="logo" onClick={() => navigate("/")}>
                        <img src={XLUXLogo} alt={"xLux: Exclusive NFTs"} />
                    </p>
                    <div className="nav">
                        <a href="/">Explore</a>
                        <a href="/mint">Create</a>
                        <a className="special" href="/">✅  Wallet Connected</a>
                    </div>
                </div>
            </div>
        )
    }
}

export default Header;
