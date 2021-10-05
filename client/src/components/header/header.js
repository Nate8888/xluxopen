import React from 'react'

import './header.css'

class Header extends React.Component {
    render() {
        return (
            <div className="header-container">
                <div className="header">
                    <p className="logo">Logo</p>
                    <div className="nav">
                        <a href="/">Explore</a>
                        <a href="/mint">Create</a>
                        <a className="special" href="/">Connect Wallet</a>
                    </div>
                </div>
            </div>
        )
    }
}

export default Header;