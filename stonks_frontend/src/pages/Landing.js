import React, {Component} from 'react';
import {Button, Container, Col, Row} from 'react-bootstrap';
import '../css/landing.css';

import LandingNavbar from '../components/LandingNavbar';
import LandingSplash from '../components/LandingSplash';
import LandingVertCarousel from '../components/LandingVertCarousel';

require('bootstrap');

/** The main page/first page of the site, for new users and onlookers. */

class Landing extends Component {

  render() {
    // No logic regarding changes in UI is expected here but space is reserved if so.
    return(
      <Container fluid id="background">
        <LandingNavbar/>
        <LandingSplash/>
        <Row id="mission_rect">
          <div id="mission_title" className="light">Mission</div>
          <p id="mission_text" className="light">Investing in the stock market has been localized with free platforms like Robinhood and WeBull therefore, this advancement 
removed any barrier of entry into the stockmarket “no matter how much experience you have (or don’t have)” (Robinhood). This may 
sound idealistic however, we emphasize the economic principle of intentions versus effects. A staggering 90% of hopeful and 
seasoned investors lose money in the stock market; these apps removing any barrier to entry have only exacerbated that statistic. 
Investing is no get rich quick scheme but can ensure a prosperous future if approached with the correct mindset and strategy. 
Investing in the stock market is not hard; like most things, it entails a learning curve. Stonkstache is here to walk you through the 
learning curve and serve as your educational tool to understanding the principles and mindset of successful investors.</p>
        </Row>
        <LandingVertCarousel/>
      </Container>
    )
  }
}


export default Landing;