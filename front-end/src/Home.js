import {Component} from 'react'
import React from 'react'
// import logo from './logo.svg'
// import './App.css'
// import Table from './components/Table'
// import ReactTable from 'react-table'
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import TopRow from './components/TopRow'
import MostCommonProjects from './components/MostCommonProjects'
import table from './store/TableStore'
import homeStore from './store/HomeStore'
// import Navbar from './components/Navbar'
// import Search from './components/Search'

class Home extends Component {
    constructor (props) {
        super(props)
        this.state = {
            projectsPHP: []
        }
    }

    componentDidMount () {
        axios.get('http://127.0.0.1:5000/top?date=2018-02-01&numberof_libraries=10&collection=libraries&graph=github_test')
            .then(res => {
                // console.log(res.data)
                homeStore.PHP.mostPopularProjects = res.data;
                console.log(homeStore.PHP.mostPopularProjects);
                // this.setState(()=>(this.props.projectsPHP.table = res.data));
            })
    };

    render () {

        return (
            <div class="container" id="page">

                <div class="row" id="page-contents">
                    <div class="col-md-12" id="home_index_page">
                        <div class="showcase">
                            <div class="billboard">
                                <div class="row">
                                    <div class="col-md-12">
                                        <h1 class="discover_msg">
                                            Discover, Track and Compare Open Source
                                        </h1>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 billboard_search">
                                        <form action="https://www.openhub.net/p" class="search" id="search_form">
                                            <input name="ref" type="hidden" value="homepage"></input>
                                            <input class="for_search_all_code" id="text" name="query"
                                                   placeholder="Search Projects..." type="text"></input>
                                            <span class="image_icon"><img id="icon_text"
                                                                          src="./home_reduced_files/search_icon2-1726136a5b171fb9d66e992cbdcd4f6ccc4f81cb22b5f555fd5ac089e07a19b2.png"
                                                                          alt="Search icon2"></img></span>

                                            <p class="icon_search"></p>
                                        </form>
                                    </div>
                                </div>

                            </div>
                        </div>
                        <MostCommonProjects projects={homeStore.PHP}/>

                    </div>
                </div>
            </div>
        )
    }
}

export default view(Home)
