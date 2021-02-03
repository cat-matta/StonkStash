import React, {Component} from 'react';
import {Button, Container, Col, Row} from 'react-bootstrap';
import '../css/landing.css';

import LandingNavbar from '../components/LandingNavbar';

/** The main page/first page of the site, for new users and onlookers. */

class Landing extends Component {

  render() {
    // No logic regarding changes in UI is expected here but space is reserved if so.
    return(
      <Container fluid id="background">
        <LandingNavbar></LandingNavbar>
      </Container>
    )
  }
}


export default Landing;