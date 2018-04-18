// import './ProjectPage.css'
import {Component} from 'react'
import React from 'react'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import MyHeader from './components/MyHeader'

import ToplibrariesTable from './components/ToplibrariesTable'
import './TopLibrariesPage.css'
import TopLibrariesStore from './components/store/TopLibrariesStore'
import NavbarInner from './components/NavbarInner'


import DatePicker from './components/DatePicker'
import homeStore from './store/HomeStore'

class TopLibrariesPage extends Component {
    constructor (props) {
        super(props)
        
    }

    componentWillMount () {



        axios.get('http://127.0.0.1:5000/topcurrent', {
            params: {
                numberof_libraries:100
            }
        }).then(res => {
            console.log(res.data)
            TopLibrariesStore.libraries = res.data
        })

    };

    render () {
        return (

            <div class="container" id="page">
                <header>
                    <div class="navbar"></div>
                    <NavbarInner/>
                </header>
                <div class="row" id="page-contents">
                    <div class="col-md-12" id="explore_projects_page">

                        <h1 class="margin_top_15">Libraries</h1>
                        <DatePicker/>
                        <ToplibrariesTable/>
                    </div>
                </div>
            </div>

        )
    }
}

export default view(TopLibrariesPage)
