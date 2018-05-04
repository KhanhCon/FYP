// import './ProjectPage.css'
import {Component} from 'react'
import React from 'react'
import axios from 'axios'
import {view, store} from 'react-easy-state'
import TopLibrariesStore from './store/TopLibrariesStore'
import moment from 'moment';
import DatePickerLib from 'react-datepicker';
// import 'react-datepicker/dist/react-datepicker.css';
import DayPicker from 'react-day-picker';
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';
import {ClipLoader} from 'react-spinners'


class DatePicker extends Component {
    constructor (props) {
        super(props)
    }

    componentWillMount(){
        axios.get('http://127.0.0.1:5000/firstShaDate').then(res => {
            // console.log(res.data);
            TopLibrariesStore.firstShaDate = res.data.date

        })
    };

    dateChange (event) {
        TopLibrariesStore.date = event.target.value
        // this.setState({num: event.target.value})
        // console.log(TopLibrariesStore)
    };

    getLibraries(){
        TopLibrariesStore.libraries = [];
        axios.get(TopLibrariesStore.urlTopLibraries, {
            params: {
                date: TopLibrariesStore.date,
                numberof_libraries:100
            }
        }).then(res => {
            // console.log(res.data)
            TopLibrariesStore.libraries = res.data

        })
    };

    handleDayChange(day, {  disabled, today, selected }){
        if(disabled || selected){}
        else if(today){
            TopLibrariesStore.tableLoading = 'loading';
            TopLibrariesStore.date = day;
            TopLibrariesStore.libraries = [];
            axios.get('http://127.0.0.1:5000/topcurrent', {
                params: {
                    numberof_libraries:100
                }
            }).then(res => {
                // console.log(res.data)
                TopLibrariesStore.libraries = res.data
            })
        }
        else{

            TopLibrariesStore.date = day;
            TopLibrariesStore.libraries = [];
            axios.get(TopLibrariesStore.urlTopLibraries, {
                params: {
                    date: TopLibrariesStore.date,
                    numberof_libraries:100
                }
            }).then(res => {
                // console.log(res.data)
                TopLibrariesStore.libraries = res.data


            });
        }
    };

    render () {
        const disableDays = {
            after: new Date(),
            before:new Date(TopLibrariesStore.firstShaDate)
        };

        if(TopLibrariesStore.firstShaDate){
            var dayPicker = <DayPicker selectedDays={TopLibrariesStore.date} disabledDays={disableDays} onDayClick={this.handleDayChange} />
        }
        else{
            var dayPicker = <ClipLoader
                color={'#36D7B7'}
                loading={true}/>
        }

        return (



            <div class=" col-md-3 margin_left_10 margin_top_20" id="explore_sidebar">
                <div>
                    <h3></h3>
                    <div>
                        {dayPicker}
                    </div>
                </div>
            </div>

        )
    }
}

export default view(DatePicker)
