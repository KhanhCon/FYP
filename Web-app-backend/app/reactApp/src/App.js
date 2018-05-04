import {Component} from 'react'
import React from 'react'
// import logo from './logo.svg'
// import './App.css'
// import Table from './components/Table'
// import ReactTable from 'react-table'
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table'
import axios from 'axios'
import { view, store } from 'react-easy-state'
import table from './store/TableStore'
import Navbar from './components/Navbar'
import Search from './components/Search'
import DayPicker from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';

class App extends Component {
    constructor (props) {
        super(props)
        // this.state = {
        //     date: '',
        //     num: '',
        //     table: []
        // }
    }

    getTop (date, num) {
        // console.log(date)
        // console.log(num)

        axios.get('http://127.0.0.1:5000/top?date=' + date + '&numberof_libraries=' + num + '&collection=libraries&graph=github_test')
            .then(res => {
                // console.log(res.data)
                this.props.tableProp.table = res.data
                // this.setState({table: res.data})
            })
    };

    dateChange (event) {
        // this.props.tableProp.date = event.target.value
        console.log(this.props.tableProp.date)
        // this.setState({date: event.target.value})
    };

    numChange (event) {
        this.props.tableProp.num = event.target.value
        // this.setState({num: event.target.value})
    };

    render () {
        var libraries = this.props.tableProp.table
        console.log(this.props.navBarProp)
        // var libraries = this.state['table']
        return (
            <div className="App">
                <DayPicker/>
                {/*<Navbar items={this.props.navBarProp}/>*/}
                <Search/>
                Date <input onChange={this.dateChange.bind(this)} type="text"></input>
                number of libraries <input onChange={this.numChange.bind(this)} type="text"></input>
                <button onClick={() => this.getTop(this.props.tableProp.date, this.props.tableProp.num)}>Submit</button>

                <BootstrapTable data={libraries} striped={true} hover={true}>
                    <TableHeaderColumn dataField="count" dataSort={true}>count</TableHeaderColumn>
                    <TableHeaderColumn dataField="library" isKey={true} dataAlign="center"
                                       dataSort={true}>library</TableHeaderColumn>

                </BootstrapTable>

            </div>
        )
    }
}

export default view(App)
