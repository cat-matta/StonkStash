import React, {Component} from 'react';
import {Button, Container, Col, Row} from 'react-bootstrap';
import '../css/landing.css';
//import '../css/embeelanding.css'
import LandingNavbar from '../components/LandingNavbar';
import LandingSplash from '../components/LandingSplash';
import LandingVertCarousel from '../components/LandingVertCarousel';

require('bootstrap');

/** The main page/first page of the site, for new users and onlookers. */

class Landing extends Component {

  render() {
    // No logic regarding changes in UI is expected here but space is reserved if so.
    return(
     
     <div class="container">
       <div class="center"><h1 class="alignmiddle">
      <h1 class="text-focus-in"><h1 class="alignmiddle"><font color="white">Hello World</font></h1>
      //<font color="White">Under Construction</font></h1></h1>

     </div></div>
    )
  }
}


export default Landing;