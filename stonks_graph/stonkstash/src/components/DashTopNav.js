import React, { Component } from 'react';
import {Navbar, Nav} from 'react-bootstrap';

import LessonMenuIcon from '../images/dash_lesson_menu_button.png';
import BrandStacheIcon from '../images/dash_nav_stache.png';
import ProfileButtonIcon from '../images/dash_profile_button.png';

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
            <Nav>
                <Nav.Link href="#">
                    <img
                        src={LessonMenuIcon}>

                        </img>
                </Nav.Link>
            </Nav>
            <Navbar.Brand href="#">
                <img
                    src={BrandStacheIcon}>

                    </img>
            </Navbar.Brand>
            <Nav>
                <Nav.Link href="#">
                    <img
                        src={ProfileButtonIcon}>
                            
                        </img>
                </Nav.Link>
            </Nav>
        </Navbar>
        );
    }
}

export default DashTopNav;