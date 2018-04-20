import {Component} from 'react'
import React from 'react'
import Highcharts from 'highcharts/highstock'
import HighchartsReact from 'highcharts-react-official'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import { ClimbingBoxLoader } from 'react-spinners';

class UsageChart extends Component {
    constructor (props) {
        super(props)
        // this.state = {
        //     url: 'http://127.0.0.1:5000/usageovertime',
        //     config: []
        // }
    }

    componentDidMount () {
        const s = document.createElement('script');
        s.type = 'text/javascript';
        s.async = false;
        s.innerHTML = "document.getElementsByClassName('css-10amf0o')[0].classList.remove('css-10amf0o');";
        document.head.appendChild(s);
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
            var chart = <div style={{textAlign:"center"}}><ClimbingBoxLoader
                color={'blue'}
                loading={true}
            /></div>

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
                <h2 className="center">Usages over time</h2>
                        {chart}

            </div>
        )
    }
}

export default view(UsageChart)
