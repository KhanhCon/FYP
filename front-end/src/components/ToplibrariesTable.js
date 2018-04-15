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
        this.state = {
            date:''
        }
    }

    componentWillMount () {


    };

    render () {

        if (TopLibrariesStore.libraries.length === 0){
            var ranking  =  <tr style={{textAlign:"center"}}><ClipLoader
                color={'#36D7B7'}
                loading={true}/>
            </tr>
        }
        else {
            // var rows =

            var ranking =TopLibrariesStore.libraries.map((p, index) => <ToplibrariesTableRow data={p} rank={index + 1}/>);

        }

        return (

            <div class="pull-right col-md-8 margin_top_20">
                <h2 class="pull-left">Most popular PHP libraries</h2>
                <form action="" rel="sort_filter">

                </form>
                <div class="clearfix"></div>


                <table class="table table-striped center-block" id="hot_projects">
                    <tbody><tr>
                        <th width="5%">Rank</th>
                        <th width="5%"></th>
                        <th width="35%"></th>
                        <th width="15%"> language</th>
                        <th class="center" width="8%"></th>
                        <th class="center" width="12%">
                            <a class="meta" target="_blank" href="http://blog.openhub.net/2014/01/about-the-ohloh-hotness-score">Usage</a>
                        </th>
                    </tr>

                    {ranking}
                    </tbody></table>


                <div class="clearfix"></div>
            </div>

        )
    }
}

export default view(ToplibrariesTable)
