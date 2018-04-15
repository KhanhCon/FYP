// import './ProjectPage.css'
import {Component} from 'react'
import React from 'react'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import TopLibrariesStore from './store/TopLibrariesStore'

class ToplibrariesTableRow extends Component {
    constructor (props) {
        super(props)
    }

    render () {
        return (

            <tr>
                <td class="center">
                    {this.props.rank}
                </td>
                <td>
                    {/*<img style="width:32px; height:32px; border:0 none;" itemprop="image" alt="Nextcloud" src="https://s3.amazonaws.com/cloud.ohloh.net/attachments/90185/19211038_small.">*/}
                </td>
                <td>
                    <a href={"/project/"+this.props.data.library._key}>{this.props.data.library.fullname}</a>
                </td>
                <td class="center">

                </td>
                <td class="pai">
                    {/*<a class="twentyfive_project_activity_level_very_high" href="http://blog.openhub.net/about-project-activity-icons/" target="_blank" title="Very High Activity"></a>*/}
                </td>
                <td class="center">
                    {this.props.data.count}
                </td>
            </tr>

        )
    }
}

export default view(ToplibrariesTableRow)
