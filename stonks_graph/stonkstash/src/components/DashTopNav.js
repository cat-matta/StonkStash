import React, { Component } from 'react';
import {Navbar, Nav} from 'react-bootstrap';

/* The navbar at the top of the dashboard.
 * Width is end to end. 
 * Left corner has a button to activate some kind of side menu.
 * Center has our logo.
 * Right has a profile button, which will remain inactive until the dashboard is functional.
 */
class DashTopNav extends Component {

    
    render() {
        return(
        <Navbar expand="lg" variant="" bg="" className="navbar-top">
            <Navbar.Brand href="#">Navbar</Navbar.Brand>
        </Navbar>
        );
    }
}

export default DashTopNav;