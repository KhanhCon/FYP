// import './ProjectPage.css'
import {Component} from 'react'
import React from 'react'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import MyHeader from './components/MyHeader'
// import Navbar from './components/Navbar'
// import Search from './components/Search'
import SearchItem from './components/SearchItem'
import NavbarInner from './components/NavbarInner'
import ReactHighstock from 'highcharts'

import Highcharts from 'highcharts/highstock'
import HighchartsReact from 'highcharts-react-official'
import MastHead from './components/Masthead'
import UsedWithFrequently from './components/UsedWithFrequently'
import UsageChart from './components/UsageChart'
// import 'react-day-picker/lib/style.css';
import DayPicker from 'react-day-picker'


class ProjectPage extends Component {
    constructor (props) {
        super(props)
        this.state = {
            urlRelevant: 'http://192.168.1.65:5000/relevant',
            urlUsage: 'http://192.168.1.65:5000/usageovertime',
            projectID: 'libraries/' + this.props.match.params.projectid,
            config: [],
            relevantProjects: []
        }
    }

    componentWillMount () {

        axios.get(this.state.urlRelevant, {
            params: {
                library: this.state.projectID
            }
        }).then(res => {
            this.setState({relevantProjects: res.data})
        });

        axios.get(this.state.urlUsage, {
            params: {
                library: this.state.projectID
            }
        }).then(res => {
            this.setState({config: res.data})
            console.log(res.data)

        })
    };

    render () {
        return (

            <div class="container-fluid" id="project_container">
                <header>
                    <div class="navbar"></div>
                    <NavbarInner/>
                </header>
                <div class="row" id="page-contents">
                    <div class="col-md-12" id="projects_show_page">
                        <MastHead project = {this.state.projectID.split("/")[1]} />
                        <div class="row mezzo"></div>
                        <div id="projects_show_page" itemscope="" itemtype="http://schema.org/ItemPage">
                            <div class="col-md-12">
                                <div id="page_contents">
                                    <div class="row row-eq-height margin_top_two project_row">
                                        <UsedWithFrequently relevantProjects={this.state.relevantProjects} project={this.state.projectID.split("/")[1]}/>
                                        <UsageChart projectid={this.state.projectID} config={this.state.config}/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        )
    }
}

export default view(ProjectPage)
