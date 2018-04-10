import {Component} from 'react'
import React from 'react'
// import logo from './logo.svg'
// import './App.css'
// import Table from './components/Table'
// import ReactTable from 'react-table'
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import MyHeader from './components/MyHeader'
import TopRow from './components/TopRow'
import MostCommonProjects from './components/MostCommonProjects'
import table from './store/TableStore'
import homeStore from './store/HomeStore'
// import Navbar from './components/Navbar'
// import Search from './components/Search'
import SearchItem from './components/SearchItem'
import NavbarInner from './components/NavbarInner'

import './Search.css'

class Home extends Component {
    constructor (props) {
        super(props)
        this.state = {
            projectsPHP: []
        }
    }

    componentDidMount () {
    };

    render () {

        return (

            <div class="container" id="page" style={{marginTop: 0 +'px'}}>
                <header>
                    <div class="navbar"></div>
                    <NavbarInner/>
                </header>
                <div class="row" id="page-contents">
                    <div class="col-md-12" id="projects_index_page">

                        <meta content="NOINDEX, NOFOLLOW" name="ROBOTS"></meta>
                        <div id="projects_index_header">
                            <h1 class="pull-left">Projects</h1>

                        </div>
                        <div class="clearfix">&nbsp;</div>


                        <div class="clear"></div>
                        <div id="projects_index_list">

                            <div class="oh_pagination text-center"></div>
                        </div>

                    </div>
                </div>
            </div>

        )
    }
}

export default view(Home)
