import {Component} from 'react'
import React from 'react'
// import logo from './logo.svg'
// import './App.css'
// import Table from './components/Table'
// import ReactTable from 'react-table'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import MyHeader from './components/MyHeader'
import TopRow from './components/TopRow'
import MostCommonProjects from './components/MostCommonProjects'
import table from './store/TableStore'
import homeStore from './store/HomeStore'
// import Navbar from './components/Navbar'
// import Search from './components/Search'
// import './HomePage.css'
import NavbarInner from './components/NavbarInner'

class Home extends Component {
    constructor (props) {
        super(props)
        this.state = {
            projectsPHP: [],
            searchQuery: ""
        }
    }

    componentWillMount () {
        axios.get('http://127.0.0.1:5000/topcurrent?numberof_libraries=10')
            .then(res => {
                // console.log(res.data)
                homeStore.PHP.mostPopularProjects = res.data
                console.log(homeStore.PHP.mostPopularProjects)
                // this.setState(()=>(this.props.projectsPHP.table = res.data));
            })
    };

    Search (event) {
        // this.props.tableProp.num = event.target.value
        this.setState({searchQuery: event.target.value})
        console.log(this.state.searchQuery)
    };

    directToSearch(event){
        window.location = '/search?query='+this.state.searchQuery
    }

    _handleKeyPress = (e) => {
        if (e.key == 'Enter') {
            console.log("con");
            window.location = '/search?query='+this.state.searchQuery
        }
    }

    render () {

        return (
            <div class="container-fluid" id="page">
                <header>
                    <div class="navbar"></div>
                    <NavbarInner searchBar={false}/>
                </header>
                <div class="row" id="page-contents">
                    <div class="col-md-12" id="home_index_page">
                        <div class="showcase">
                            <div class="billboard">
                                <div class="row">
                                    <div class="col-md-12">
                                        <h1 class="discover_msg">
                                            Discover Open Source Libraries
                                        </h1>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 billboard_search">
                                        <form action={"/search?"} class="search" id="search_form">
                                            {/*<input name="ref" type="hidden" value="homepage"></input>*/}
                                            <input class="for_search_all_code" id="text" name="query"
                                                   placeholder="Search Libraries..." type="text" onChange={this.Search.bind(this)}  value={this.state.searchQuery}></input>
                                            <span onClick={this.directToSearch.bind(this)} href={"search?query="+this.state.searchQuery} class="image_icon"><img id="icon_text"
                                                                          src="https://png.icons8.com/search"
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
