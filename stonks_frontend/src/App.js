import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';

import Landing from './pages/Landing';

export default class App extends Component {
  render() { ///This renders everything
    return (//This will be where you wanna display stuff, in between the divs
      <Router>
        <Switch>
          <Route exact path="/" component={Landing}/>
        </Switch>
      </Router>
    )
  }
}
