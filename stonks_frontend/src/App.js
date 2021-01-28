import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';

import Landing from './pages/Landing';
import Signup from './pages/Signup';
import Login from './pages/Login';

import Dashboard from './pages/Dashboard';

export default class App extends Component {
  render() { ///This renders everything
    return (//This will be where you wanna display stuff, in between the divs
      <Router>
        <Switch>
          <Route exact path="/" component={Landing}/>
          <Route path="/signup" component={Signup}/>
          <Route path="/login" component={Login}/>
          <Route path="/dashboard" component={Dashboard}/>
        </Switch>
      </Router>
    )
  }
}
