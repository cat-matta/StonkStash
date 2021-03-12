import React, { Component } from 'react';
import { Container, Row, Col } from 'react-bootstrap';

// The components which will form the interface
import DashTopNav from '../components/DashTopNav';
import DashBottomNav from '../components/DashBottomNav';
import DashGraphView from '../components/DashGraphView';
import DashSidePanel from '../components/DashSidePanel';

import "../css/Dashboard.css";
require('bootstrap');

/* Post Login Page. Has graphs, navs to other pages, etc. Lots of action will occur here
 * insofar as api data being displayed and what not. Docs will get fleshed as we come closer to
 * what we want to achieve.  */
class Dashboard extends Component {
    constructor(props) {
        super(props);
    
        // Stately affairs
      }

    render(){
        return(
        <Container fluid>
            <DashTopNav />
            <Row>
                <Col xs={7} className="graph-parent">
                    <DashGraphView />
                </Col>
                <Col>sidemenu</Col>
            </Row>

        </Container>)
    }
}

export default Dashboard;