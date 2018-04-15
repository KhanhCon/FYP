import React from 'react';
import ReactDOM from 'react-dom';
// import './index.css';
import App from './App';
import Home from './Home'
import registerServiceWorker from './registerServiceWorker';
import Search from './Search'
import ProjectPage from './ProjectPage'
import { BrowserRouter as Router, Route } from 'react-router-dom';

import table from './store/TableStore'
import navbar from './store/NavBarStore'
import TopLibrariesPage from './TopLibrariesPage'
import TableStore from './store/TableStore'

ReactDOM.render(
    <Router>
        <div>
            <Route exact path='/' render={() => <Home/>}/>
            <Route exact path='/search' component={Search} />
            <Route exact path='/project/:projectid' component={ProjectPage} />
            <Route exact path='/top' component={TopLibrariesPage} />
            <Route exact path='/test' render = {() => <App tableProp={TableStore}/>} />


        </div>
        {/* both /roster and /roster/:number begin with /roster */}
        {/*<Route path='/roster' component={Roster}/>*/}
        {/*<Route path='/schedule' component={Schedule}/>*/}
    </Router>

    // <App tableProp = {table} navBarProp = {navbar} />
    , document.getElementById('root'));
registerServiceWorker();
