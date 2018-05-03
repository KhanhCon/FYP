import {Component} from 'react'
import React from 'react'
import Highcharts from 'highcharts/highstock'
import HighchartsReact from 'highcharts-react-official'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import { ClimbingBoxLoader } from 'react-spinners';
import APIstore from './store/APIstore'

const LibrarySumary = ({library}) => {

    // console.log(library.maintainers)

    if(library.maintainers.lenght == 0){
        var maintainers = "None"}
    else{
        var maintainers = library.maintainers.map((maintainer) =><tr>
            <td valign="top">
                <span class="pull-left">
                    <img style={{width: 24+"px", height:24+"px", border:0 +" none"}} itemprop="image" alt="Iceweasel" src={maintainer.avatar_url}></img></span>
                <p class="pull-left proj-name">{maintainer.name}</p>
            </td>

        </tr>)}



    return  <div class="col-md-4 quick_reference_container">
        <div class="well">
            <h4 class="quick_reference_heading">Quick Reference</h4>
            <div class="col-xs-12">


                <div class="col-xs-4 text-left">
                    <p>Description</p>
                </div>
                <div class="col-xs-7 left" style={{marginBottom: .5 +"em"}}>
                    <p>{library.description}</p>
                </div>

                <div class="col-xs-4 text-left ">
                    <p>Repository</p>
                </div>

                <div class="col-xs-7 left" style={{marginBottom: .5 +"em"}}>
                    <a  target="_blank" href={'https://github.com/' + library.github_fullname}>{'https://github.com/' + library.github_fullname}</a>
                    <br/>
                </div>
                <div class="clearfix"></div>
                <div class="col-xs-4 text-left ">
                    <p>Maintainers</p>
                </div>
                <div class="col-xs-7" style={{marginBottom: .5+ "em"}}>
                    <div data-project-id="firefox" id="similar_projects"><table>
                        <tbody>
                        {maintainers}

                        </tbody></table>
                    </div>

                </div>


            </div>

        </div>
    </div>
};
export default view(LibrarySumary);



