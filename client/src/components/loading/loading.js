import React from 'react'
import './loading.css'

class Loading extends React.Component {
    render() {
        return (
            <div className="loading-container">
                <div className="loading"></div>
                <p className="ld">Loading...</p>
            </div>
        )
    }
}

export default Loading;
