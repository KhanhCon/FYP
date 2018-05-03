import {Component} from 'react'
import React from 'react'
import {view, store} from 'react-easy-state'
import TopRow from './TopRow'
import { ClipLoader } from 'react-spinners';

class MostCommonProjects extends Component {
    constructor (props) {
        super(props)
    }

    render () {
        if (this.props.projects.mostPopularProjects.length == 0) {
            var projectsItems = <div style={{textAlign:"center"}}><ClipLoader
                color={'#36D7B7'}
                loading={true}
            /></div>
        }
        else {
            // var mostCommonProjects = <MostCommonProjects projects={this.props.projects}/>;
            const projects = this.props.projects.mostPopularProjects;
            var total_count = projects.reduce( function(total, item){
                return total + item.count;
            }, 0);
            console.log(total_count);
            var projectsItems = projects.map((p) => <TopRow projects={p} total={total_count} />);
            // var projectsPHP =
        }

        // console.log(projects)

        return(
            <div class="landing col-md-12 last_section">
                <div class="col-md-6 top_ten">
                    <h3 class="most_popular_projects common">Most Popular {this.props.projects.language} libraries</h3>
                    {projectsItems}
                </div>
            </div>
        )
    }
}

export default view(MostCommonProjects)
