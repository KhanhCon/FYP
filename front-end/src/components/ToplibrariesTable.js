// import './ProjectPage.css'
import {Component} from 'react'
import React from 'react'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import TopLibrariesStore from './store/TopLibrariesStore'
import ToplibrariesTableRow from './TopLibrariesTableRow'
import {ClipLoader} from 'react-spinners'

class ToplibrariesTable extends Component {
    constructor (props) {
        super(props)
    }

    render () {

        if (TopLibrariesStore.libraries.length === 0){
            var ranking_rows  =  <tr style={{textAlign:"center"}}><ClipLoader
                color={'#36D7B7'}
                loading={true}/>
            </tr>
        }
        else {
            console.log(TopLibrariesStore.libraries[0].lib)
            var ranking_rows =TopLibrariesStore.libraries.map((p, index) => <ToplibrariesTableRow data={p} rank={index + 1}/>);

        }

        if(TopLibrariesStore.date === '' || TopLibrariesStore.date.setHours(0,0,0,0) === (new Date()).setHours(0,0,0,0)){
            var date = 'today'
        }
        else{
            const options = { day: '2-digit', month: '2-digit', year: '2-digit' };
            var date = 'on ' + TopLibrariesStore.date.toLocaleDateString('et', options)
        }

        return (

            <div class="pull-right col-md-8 margin_top_20">
                <h2 class="pull-left">Most popular PHP libraries {date}</h2>
                <form action="" rel="sort_filter">

                </form>
                <div class="clearfix"></div>


                <table class="table table-striped center-block" id="hot_projects">
                    <tbody><tr>
                        <th width="5%">Rank</th>
                        <th width="5%"></th>
                        <th width="35%">library</th>
                        <th width="15%"> </th>
                        <th class="center" width="8%"></th>
                        <th class="center" width="12%">Usage</th>
                    </tr>

                    {ranking_rows}
                    </tbody></table>


                <div class="clearfix"></div>
            </div>

        )
    }
}

export default view(ToplibrariesTable)
