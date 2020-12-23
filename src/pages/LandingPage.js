import React, { Component } from 'react';
import {Button, Container, Col, Row} from 'react-bootstrap';

/** The home page for those not logged in. */

class LandingPage extends Component {

    constructor(props) {
        super(props)
    } // test

    render() {
        return(
            <Container>
                <Row className="justify-content-center">
                    <Col className="center-align">
                        <Button variant="primary" size="lg" href="/register">Register</Button>
                        <Button variant="secondary" size="lg" href="/login">Login</Button>
                    </Col>
                </Row> 
            </Container>
        )
    }
}

export default LandingPage;