import {Component} from 'react'
import React from 'react'
import Highcharts from 'highcharts/highstock'
import HighchartsReact from 'highcharts-react-official'
import axios from 'axios'
import {view, store} from 'react-easy-state'


class Masthead extends Component {
    constructor (props) {
        super(props)
    }

    componentWillMount () {
    };

    render () {


        return (
            <div id="project_masthead">
                <div class="col-md-1 no_padding" id="project_icon">

                </div>
                <div class="col-md-11" id="project_header">
                    <div class="pull-left project_title">
                        <h1 class="float_left" itemprop="name">
                            <a style={{color: + 'black'}} itemprop="url" href={"/project/"+this.props.project}>{this.props.project}</a>
                        </h1>

                    </div>

                </div>
            </div>
        )
    }
}

export default view(Masthead)

