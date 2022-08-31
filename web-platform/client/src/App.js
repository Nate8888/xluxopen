import React from 'react'
import { Router } from '@reach/router'

import Home from './components/home/home'
import Mint from './components/mint/mint'
import Detail from './components/detail/detail'
import Header from './components/header/header'

import './App.css'

class App extends React.Component {
    render() {
        return (
            <div className="App">
                <Header />
                <Router>
                    <Home path="/" />
                    <Mint path="/mint" />
                    <Detail path="/nft/:wallet/:tokenid" />
                </Router>
            </div>
        )
    }
}

export default App;
