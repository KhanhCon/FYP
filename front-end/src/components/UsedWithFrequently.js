import {Component} from 'react'
import React from 'react'
import Highcharts from 'highcharts/highstock'
import HighchartsReact from 'highcharts-react-official'
import axios from 'axios'
import {view, store} from 'react-easy-state'


class UsedWithFrequently extends Component {
    constructor (props) {
        super(props)
    }

    componentWillMount () {
    };

    render () {
        if(this.props.relevantProjects.length == 0){
            var relevantProjects = ""
        }
        else{
            var relevantProjects = this.props.relevantProjects.map((p) => <a class="tag" itemprop="keywords" href={"/project/"+p.library._id.split('/')[1]}>{p.library.fullname}</a>);
        }


        return (
            <div class="col-md-4 project_summary_container">
                <div class="well">
                    <h4 class="text-left">Relevant libraries</h4>
                    <section id="project_summary" itemprop="description">
                        <p>Projects that use {this.props.project} usually use these libraries</p>
                    </section>
                    <section id="project_tags" itemscope="" itemtype="http://schema.org/CreativeWork">
                        <h4 class="title">Libraries</h4>
                        <p class="tags">
                            <span></span>
                            {relevantProjects}
                            {/*<a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=browser">browser</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=chrome">chrome</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=client">client</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=css">css</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=development">development</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=firefox">firefox</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=gecko">gecko</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=gtk">gtk</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=html">html</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=http">http</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=internet">internet</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=javascript">javascript</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=mozilla">mozilla</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=seamonkey">seamonkey</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=thunderbird">thunderbird</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=web">web</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=www">www</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=xhtml">xhtml</a> <a class="tag" itemprop="keywords" href="https://www.openhub.net/tags?names=xul">xul</a>*/}
                        </p>
                    </section>
                </div>
            </div>
        )
    }
}

export default view(UsedWithFrequently)

