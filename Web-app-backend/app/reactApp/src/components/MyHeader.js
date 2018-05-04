import {Component} from 'react'
import React from 'react'
import {view, store} from 'react-easy-state'

class MyHeader extends Component {
    constructor (props) {
        super(props)
    }

    render () {
        return (
            <header>
            <div class="navbar"></div>
                <div id="navbar-inner">
                    <div id="nav-top-bar">
                        <ul class="new_main_menu select_projects">
                            <li class="menu_item projects">
                                <a class="" href="https://www.openhub.net/explore/projects">Projects</a>
                            </li>
                            <li class="menu_item people">
                                <a class="" href="https://www.openhub.net/people">People</a>
                            </li>
                            <li class="menu_item organizations">
                                <a class="" href="https://www.openhub.net/explore/orgs">Organizations</a>
                            </li>
                            <li class="menu_item tools">
                                <a class="" href="https://www.openhub.net/tools">Tools</a>
                            </li>
                            <li class="menu_item blog">
                                <a href="http://blog.openhub.net/" target="_blank">Blog</a>
                            </li>
                            <form action="https://www.openhub.net/p" class="pull-right" id="quicksearch"
                                  style={{marginTop:-8+'px'}}>
                                <div class="dropdown">
                                    <div class="btn-group ux-dropdown">
                                        <a class="btn btn-small dropdown-toggle" data-toggle="dropdown">
                                            <span class="selection" val="p">Projects</span>
                                            <span class="caret"></span>
                                        </a>
                                        <ul class="dropdown-menu">
                                            <li>
                                                <a val="people">People</a>
                                            </li>
                                            <li>
                                                <a class="default" val="p">Projects</a>
                                            </li>
                                            <li>
                                                <a val="orgs">Organizations</a>
                                            </li>
                                            <li>
                                                <a val="posts">Forums</a>
                                            </li>
                                            <li>
                                                <a onclick="Forms.OhlohCodeSearch();" val="//code.openhub.net/search">
                                                    <i class="icon-share"><span class="translation_missing"
                                                                                title="translation missing: en.code">Code</span></i>
                                                </a>
                                            </li>
                                        </ul>
                                        <input autocomplete="off" class="search text global_top_search" name="query"
                                               placeholder="Search..." type="text" value="phpunit"></input>
                                            <input class="search hidden" id="search_type" name="search_type" type="hidden"
                                                   value="projects"></input>
                                                <button class="submit no_padding" type="submit">
                                                    <div class="icon-search global_top_search_icon"></div>
                                                </button>
                                    </div>
                                </div>
                            </form>

                        </ul>
                    </div>
                </div>

            </header>

    )
    }
    }

    export default view(MyHeader)
