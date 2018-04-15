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

class DatePicker extends Component {
    constructor (props) {
        super(props)
    }

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
            console.log(res.data)
            TopLibrariesStore.libraries = res.data

        })
    };

    handleDayChange(day){
        TopLibrariesStore.date = day;
        TopLibrariesStore.libraries = [];
        axios.get(TopLibrariesStore.urlTopLibraries, {
            params: {
                date: TopLibrariesStore.date,
                numberof_libraries:100
            }
        }).then(res => {
            console.log(res.data)
            TopLibrariesStore.libraries = res.data

        })
    };

    render () {                        <DayPicker />

        return (

            <div class=" col-md-3 margin_left_10 margin_top_20" id="explore_sidebar">
                <div>
                    <h3></h3>
                    <div>
                        <DayPicker onDayClick={this.handleDayChange} />
                        {/*<DayPickerInput onDayClick={this.handleDayChange} />*/}
                    </div>
                </div>
            </div>

        )
    }
}

export default view(DatePicker)
