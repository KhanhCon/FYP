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
import queryString from './query-string'

import './Search.css'
import {ClipLoader} from 'react-spinners'
class Home extends Component {
    constructor (props) {
        super(props)
        this.state = {
            searchResults: [],
            suggestions: [],
            searchQuery: queryString.parse(this.props.location.search).query,
            loading: "loading"

    }
    }

    componentWillMount () {
        var query = queryString.parse(this.props.location.search);
        axios.get('http://127.0.0.1:5000/search', {
            params: {
                query: query.query
            }
        })
            .then(res => {
                this.setState({searchResults: res.data.result, suggestions: res.data.suggestions , loading:"done"})
                console.log(this.state)
                // console.log(this.state.searchResults)
            })
    };

    render () {
        if(this.state.loading == "loading"){
            var searchItems =
                <div style={{textAlign:"left"}}><ClipLoader
                color={'black'}
                loading={true}/></div>;
        }
        else if(this.state.searchResults.length > 0){
            console.log(this.state.searchResults);
            var searchItems = this.state.searchResults.map((p) =>  <SearchItem project={p.library} usage={p.count}/> );
        }
        else if(this.state.searchResults.length == 0){

            var suggestions = this.state.suggestions.map((p) => <a href={"/search?query=" + p}>   {p}   </a>) ;


            var searchItems = <div class="inset advanced_search_tips">
                <h4>Your search - <strong>{this.state.searchQuery}</strong> - did not match anything.</h4>
                <p>Did you mean: {suggestions}</p>
            </div> ;

        }
        return (

            <div class="container" id="page" style={{marginTop: 0 +'px'}}>
                <header>
                    <div class="navbar"></div>
                    <NavbarInner searchQuery={this.state.searchQuery}/>
                </header>
                <div class="row" id="page-contents">
                    <div class="col-md-12" id="projects_index_page">

                        <div id="projects_index_header">
                            <h1 class="pull-left">Projects</h1>

                        </div>
                        <div class="clearfix">&nbsp;</div>


                        <div class="clear"></div>
                        <div id="projects_index_list">
                            {searchItems}
                            <div class="oh_pagination text-center"></div>
                        </div>

                    </div>
                </div>
            </div>

        )
    }
}

export default view(Home)
