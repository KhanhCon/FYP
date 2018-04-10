import {Component} from 'react'
import React from 'react'
import Highcharts from 'highcharts/highstock'
import HighchartsReact from 'highcharts-react-official'
import axios from 'axios'
import {view, store} from 'react-easy-state'

class UsageChart extends Component {
    constructor (props) {
        super(props)
        // this.state = {
        //     url: 'http://127.0.0.1:5000/usageovertime',
        //     config: []
        // }
    }

    componentWillMount () {
        // var libraryID = this.props.projectid
        // console.log(libraryID)
        // axios.get(this.state.url, {
        //     params: {
        //         library: libraryID
        //     }
        // }).then(res => {
        //     this.setState({config: res.data})
        //     console.log(res.data)
        // })
    };

    render () {
        if (this.props.config.length == 0) {
            var chart = <div></div>
        }
        else {
            var chart = <HighchartsReact
                highcharts={Highcharts}
                constructorType={'stockChart'}
                options={this.props.config}
            />
        }

        return (
            <div class="col-md-4 right_border top_section" itemscope="" itemtype="http://schema.org/Language">
                <h2 class="center">Usages over time</h2>
                <div class="col-md-12 manage_padding chart_container">
                    <div class="col-md-12 manage_padding chart-holder">
                        {chart}
                    </div>
                </div>

            </div>
        )
    }
}

export default view(UsageChart)

