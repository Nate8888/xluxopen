import React from 'react'
import { navigate } from '@reach/router'

import './header.css'

class Header extends React.Component {
    render() {
        return (
            <div className="header-container">
                <div className="header">
                    <p className="logo" onClick={() => navigate("/")}>xlux</p>
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
