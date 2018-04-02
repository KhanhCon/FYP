import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Home from './Home'
import registerServiceWorker from './registerServiceWorker';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import table from './store/TableStore'
import navbar from './store/NavBarStore'

ReactDOM.render(
    <Router>
        <Route exact path='/' render={() => <Home/>}/>
        {/* both /roster and /roster/:number begin with /roster */}
        {/*<Route path='/roster' component={Roster}/>*/}
        {/*<Route path='/schedule' component={Schedule}/>*/}
    </Router>

    // <App tableProp = {table} navBarProp = {navbar} />
    , document.getElementById('root'));
registerServiceWorker();
