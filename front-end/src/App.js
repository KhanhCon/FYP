import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import Table from "./components/Table"
import ReactTable from "react-table";
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';
import axios from "axios";

class App extends Component {

    // componentWillMount() {
    //     axios.get('http://127.0.0.1:5000/top?date=2015-08-02&numberof_libraries=5&collection=libraries&graph=github_test')
    //         .then(res => {
    //             this.setState({ table: res.data });
    //         });
    // }

    constructor(props) {
        super(props);
        this.state = {
            date: '',
            num: '',
            table: []
        };
    }

    getTop(date, num) {
        axios.get('http://127.0.0.1:5000/top?date=' + date + '&numberof_libraries=' + num + '&collection=libraries&graph=github_test')
            .then(res => {
                console.log(res.data);
                this.setState({table: res.data});
            });
    };

    dateChange(event) {
        this.setState({date: event.target.value});
    };

    numChange(event) {
        this.setState({num: event.target.value});
    };

    render() {
        var libraries = this.state["table"];
        return (
            <div className="App">

                Date <input onChange={this.dateChange.bind(this)} type="text"></input>
                number of libraries <input onChange={this.numChange.bind(this)} type="text"></input>
                <button onClick={() => this.getTop(this.state.date, this.state.num)}>Submit</button>

                <BootstrapTable data={libraries} striped={true} hover={true}>
                    <TableHeaderColumn dataField="count" dataSort={true}>count</TableHeaderColumn>
                    <TableHeaderColumn dataField="library" isKey={true} dataAlign="center"
                                       dataSort={true}>library</TableHeaderColumn>


                </BootstrapTable>

            </div>
        );
    }
}

export default App;
