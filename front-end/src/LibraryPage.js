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
import LibrarySumary from './components/LibrarySumary'
// import 'react-day-picker/lib/style.css';
import DayPicker from 'react-day-picker'
import {ClipLoader} from 'react-spinners'


class LibraryPage extends Component {
    constructor (props) {
        super(props)
        this.state = {
            urlLibrary: 'http://127.0.0.1:5000/getLibrary',
            urlRelevant: 'http://127.0.0.1:5000/relevant',
            urlUsage: 'http://127.0.0.1:5000/usageovertime',
            libraryID: 'libraries/' + this.props.match.params.projectid,
            library: '',
            config: [],
            relevantLibrariesLoading: 'loading',
            relevantLibraries: []
        }
    }

    componentWillMount () {

        axios.get(this.state.urlLibrary, {
            params: {
                libraryID: this.state.libraryID
            }
        }).then(res => {

            this.setState({library: res.data})
            // console.log(this.state.library)
        });

        axios.get(this.state.urlRelevant, {
            params: {
                library: this.state.libraryID
            }
        }).then(res => {
            this.setState({relevantLibraries: res.data, relevantLibrariesLoading: "done"})
        });

        axios.get(this.state.urlUsage, {
            params: {
                library: this.state.libraryID
            }
        }).then(res => {
            this.setState({config: res.data});
            // console.log(res.data)

        })
    };

    render () {

        if(this.state.library===""){
            var librarySumary = <div style={{textAlign:"left"}}><ClipLoader
                color={'blue'}
                loading={true}/>
            </div>;
        }
        else {
            var librarySumary = <LibrarySumary library={this.state.library}/>
        }
        return (

            <div class="container-fluid" id="project_container">
                <header>
                    <div class="navbar"></div>
                    <NavbarInner/>
                </header>
                <div class="row" id="page-contents">
                    <div class="col-md-12" id="projects_show_page">
                        <MastHead library = {this.state.library} />
                        <div class="row mezzo"></div>
                        <div id="projects_show_page" itemscope="" itemtype="http://schema.org/ItemPage">
                            <div class="col-md-12">
                                <div id="page_contents">
                                    <div class="row row-eq-height margin_top_two project_row">
                                        <UsedWithFrequently loading = {this.state.relevantLibrariesLoading} relevantLibraries={this.state.relevantLibraries} library={this.state.library}/>
                                        <UsageChart config={this.state.config}/>
                                        {librarySumary}
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

export default view(LibraryPage)
