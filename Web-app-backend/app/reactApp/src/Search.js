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
import Sort from './components/Sort'


class Search extends Component {
    constructor (props) {
        super(props)
        this.state = {
            searchResults: [],
            suggestions: [],
            searchQuery: queryString.parse(this.props.location.search).query,
            loading: "loading",
            sort: 'relevant',
            relevantStyle :  {fontWeight:"bold",textDecoration:"underline"},
            mostUsedStyle : {}

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
                // console.log(this.state)
            })
    };

    mostUsedClick(){
        this.setState({mostUsedStyle: {fontWeight:"bold",textDecoration:"underline"},relevantStyle:{}});
        this.state.searchResults.sort(function(a, b) {
            return b.count - a.count;
        });
    }
    relevantClick(){
        this.setState({relevantStyle: {fontWeight:"bold",textDecoration:"underline"},mostUsedStyle:{}});
        this.state.searchResults.sort(function(a, b) {
            return a.rank - b.rank;
        });
    }

    render () {



        if(this.state.loading == "loading"){
            var searchItems =
                <div style={{textAlign:"left"}}><ClipLoader
                color={'black'}
                loading={true}/></div>;
        }
        else if(this.state.searchResults.length > 0){
            // console.log(this.state.searchResults);

            var sortComponent =
                <div id="projects_index_header">
                    <h1 class="pull-left">Libraries</h1>
                        <div class="pull-right" style={{paddingBottom: 5+"px"}}> Sort:
                        <a onClick={this.relevantClick.bind(this)} style={this.state.relevantStyle}>relevance</a>
                        |
                        <a onClick={this.mostUsedClick.bind(this)} style={this.state.mostUsedStyle}>most used</a>
                    </div>
                </div>;

            var searchItems = this.state.searchResults.map((p) =>  <SearchItem project={p.library} usage={p.count}/> );
        }
        else if(this.state.searchResults.length == 0){
            var sortComponent = null;
            var suggestions = this.state.suggestions.map((p) => <a href={"/search?query=" + p}>   {p}   </a>) ;
            var suggestComponent = this.state.suggestions.length === 0 ? <p>No suggestions available </p> : <p>Did you mean: {suggestions}</p>;
            var searchItems = <div class="inset advanced_search_tips">
                <h4>Your search - <strong>{this.state.searchQuery}</strong> - did not match anything.</h4>

                {suggestComponent}

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

                        {sortComponent}

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

export default view(Search)
