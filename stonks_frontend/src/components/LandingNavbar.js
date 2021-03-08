import React, {Component} from 'react';
import {Navbar, Nav} from 'react-bootstrap';
import '../css/landing.css';
import logo from '../images/logo.png';

/** A component that manifests the navbar at the top of the landing page. */
class LandingNavbar extends Component {

  render() {
    return(
      
      <Navbar>
        <Navbar.Brand href="/" 
          id="stonkstash_title"
          className="light">
          Stonkstash{' '}
          <img alt="sinister moustache man"
          id="stonkstash_logo"
          src={logo}
          className="d-inline align-top" 
          />
        </Navbar.Brand>
        <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
          <Nav>
            <Nav.Link href="#mission" id="mission_button" className="light navbar_text">Mission</Nav.Link>
            <Nav.Link href="#learn" id="learn_button" className="light navbar_text">Learn</Nav.Link>
            <Nav.Link href="#discover" id="discover_button" className="light navbar_text">Discover</Nav.Link>
            <Nav.Link href="#watch" id="watch_button" className="light navbar_text">Watch</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    )
  }
}

export default LandingNavbar;