import {Component} from 'react'
import React from 'react'
import {view, store} from 'react-easy-state'

class NavbarInner extends Component {
    constructor (props) {
        super(props)
    }

    render () {
        return (
            <div id="navbar-inner">
                <div id="nav-top-bar">
                    <ul class="new_main_menu select_projects">
                        <li class="menu_item projects">
                            <a class="" href="https://www.openhub.net/explore/projects">Projects</a>
                        </li>

                        <form action="" class="pull-right" id="quicksearch" style={{marginTop: -8 +'px'}}>
                            <div>
                                <div class="btn-group">
                                    <a class="btn btn-small">
                                        <span class="selection" val="p">Projects</span>

                                    </a>

                                    <input autocomplete="off" class="search text global_top_search" name="query" placeholder="Search..." type="text" value=""></input>
                                        <input class="search hidden" id="search_type" name="search_type" type="hidden" value="projects"></input>
                                            <button class="submit no_padding" type="submit">
                                                <div class="icon-search global_top_search_icon"></div>
                                            </button>
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
