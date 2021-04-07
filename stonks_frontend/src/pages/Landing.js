import React, {Component} from 'react';
import {Container, Col, Row, Button, Form, Image} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import '../css/landing.css';

import LandingNavbar from '../components/LandingNavbar';
import LandingSplash from '../components/LandingSplash';
import LandingVertCarousel from '../components/LandingVertCarousel';

import bottom_stache from '../images/bottom_stache.png';

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
seasoned investors lose money in the stock market; these apps removing any barrier to entry have only exacerbated that statistic. {this.data}
Investing is no get rich quick scheme but can ensure a prosperous future if approached with the correct mindset and strategy. 
Investing in the stock market is not hard; like most things, it entails a learning curve. Stonkstache is here to walk you through the 
learning curve and serve as your educational tool to understanding the principles and mindset of successful investors.</p>
        </Row>
        <LandingVertCarousel/>
        <Row id="closing_rect">
          <div id="closing_header" className="light">When You Make it Over the Learning Curve: Delete Us!</div>
          <p id="closing_text" className="light">Or hold on to this tool for its no-nonsense display of volatility and balance sheets and to reinforce the basic but nonetheless essential pillars to successful long-term investing.</p>
          <p id="closing_disclaimer">Stonkstache is for information and educational purposes only. It is not intended to be an investment advice. Please consider the risk involved and your personal financial situation before investing or seek a duly licensed professional for investment advice.</p>
        </Row>
        <Row id="footer_rect">
          <Col sm={3}>
            <Link id="terms_link" className="light" to="#terms">Terms & Conditions</Link>
            <Link id="disclaimers_link" className="light" to="#disclaimers">Disclaimers</Link>
            <Link id="privacy_link" className="light" to="#privacy">Privacy</Link>
          </Col>
          <Col sm={9}>
            
            <Form.Group controlId="formBasicEmail">
              <Form.Label id="newsletter_text" className="light">Join our monthly newsletter for early access to any information regarding the launch!</Form.Label>
              <Form.Control id="newsletter_input_field" className="light" type="email" placeholder="Email..."/>
              <Button id="newsletter_submit_button" className="light" variant="">Join!</Button>
            </Form.Group>
         </Col>
        </Row>
        <Row>
          <Image id="bottom_stache" src={bottom_stache}/>
          <div id="all_rights_text" className="dark">2021 Stonkstache. All Rights Reserved.</div>
        </Row>
      </Container>
    )
  }
}

/**prints ratios info to console**/
fetch('/info?symbol=aapl').then(function (response) {
          return response.json();
      }).then(function (text) {
          console.log(text);
      });

/**prints stock candles to console**/
/**see main.py in stonks_backend for correct values to put for these params**/
fetch('/stock?symbol=aapl&start=2019-12-25&interval=D').then(function (response) {
          return response.json();
      }).then(function (text) {
          console.log(text);
      });

export default Landing;