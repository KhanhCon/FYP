import {Component} from 'react'
import React from 'react'
import {view, store} from 'react-easy-state'

class NavbarInner extends Component {
    constructor (props) {
        super(props)
        this.state = {
            searchQuery:this.props.searchQuery
        }
    }

    Search (event) {
        // this.props.tableProp.num = event.target.value
        this.setState({searchQuery: event.target.value})
        console.log(this.state.searchQuery)
    };


    render () {
        return (
            <div id="navbar-inner">
                <div id="nav-top-bar">
                    <ul class="new_main_menu">
                        <li class="menu_item projects ">
                            <a class="" href="/">Home</a>
                        </li>
                        <li class="menu_item projects">
                            <a class="" href="/top">Top</a>
                        </li>

                        <form action="" class="pull-right" id="quicksearch" style={{marginTop: -8 +'px'}}>
                            <div>
                                <div class="btn-group">
                                    {/*<a class="btn btn-small">*/}
                                        {/*<span class="selection" val="p">Projects</span>*/}

                                    {/*</a>*/}
                                    <form action={"/search?"}>
                                    <input placeholder="Search..." name={"query"}  type="text" onChange={this.Search.bind(this)}  value={this.state.searchQuery}></input>
                                        {/*<input class="search hidden" id="search_type" name="search_type" type="hidden" value="projects"></input>*/}
                                    <button class="submit no_padding">
                                        <div class="icon-search global_top_search_icon"></div>
                                    </button>
                                    </form>
                                        {/*<a class="" href={"/search?query="+this.state.searchQuery} >*/}
                                                {/*<img src={'https://png.icons8.com/search'}></img>*/}
                                            {/*</a>*/}
                                </div>
                            </div>
                        </form>

                    </ul>
                </div>
            </div>
        )
    }
}

export default view(NavbarInner)
