import {Component} from 'react'
import React from 'react'

import {view, store} from 'react-easy-state'

class TopRow extends Component {
    constructor (props) {
        super(props)
    }

    render () {
        return(
            <div class="top_ten_row">
                <a class="top_ten_icon" href="https://www.openhub.net/p/firefox"></a>
                <div class="top_ten_main">
                    <div class="top_ten_link">
                        <a href={"project/"+this.props.projects.library._key}>{this.props.projects.library.fullname}</a>
                    </div>
                    <div class="popular pull-left top_ten_bar" style={{width:this.props.projects.count*200/this.props.total +"%"}}>
                        &nbsp;
                    </div>
                    <div class="top_ten_label pull-left">
                        {this.props.projects.count} usages
                    </div>
                </div>
                <div class="clearfix"></div>
            </div>
        )
    }
}

export default view(TopRow)
