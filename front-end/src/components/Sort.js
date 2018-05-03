import {Component} from 'react'
import React from 'react'

import {view, store} from 'react-easy-state'
import SearchStore from './store/SeachStore'
// import TopLibrariesStore from './store/TopLibrariesStore'

class Sort extends Component {
    constructor (props) {
        super(props)
        this.state = {

    }
    }

    render () {

        return(
            <div class="pull-right" style={{paddingBottom: 5+"px"}}> Sort:
                <span style={this.state.relevantStyle}>relevance</span>
                |
                <span style={this.state.mostUsedStyle}>most used</span>
            </div>
        )
    }
}

export default view(Sort)
