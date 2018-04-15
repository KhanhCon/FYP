import {Component} from 'react'
import React from 'react'

import {view, store} from 'react-easy-state'

class SearchItem extends Component {
    constructor (props) {
        super(props)
    }

    render () {

        return(
            <div class="well searchable" id="project_662124">
                <h2 class="title pull-left"><a title="phpunit-selenium2-samples" href={"project/"+this.props.project._key}>{this.props.project.fullname}</a></h2>
                <div class="pull-right">
                    <div class="compare">
                        <form class="sp_form styled form-inline" id="sp_form_phpunit-selenium2-samples" style={{minWidth: 94 + 'px'}}>
                            <span class="sp_label" title="Compare">Usages: {this.props.usage}</span>

                            <div class="clear_both"></div>
                        </form>
                    </div>
                    <div class="i_use_this">
                    </div>
                </div>
                <div class="clear"></div>

                <div class="tags">
                </div>
            </div>
        )
    }
}

export default view(SearchItem)


