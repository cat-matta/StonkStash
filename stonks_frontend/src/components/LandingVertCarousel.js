import {Component} from 'react';
//import { Row, Col, ButtonGroup, Button, Image} from 'react-bootstrap';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Image from 'react-bootstrap/Image';
//import '../css/landing.css';

import arrow_up from '../images/elevator_arrow_up.png';
import arrow_down from '../images/elevator_arrow_down.png';
import learn_phone from '../images/learn_phone.png';
import discover_phone from '../images/discover_phone.png';
import watch_phone from '../images/watch_phone.png';


/** The thing with the buttons that change the content of the section */
class LandingVertCarousel extends Component {
  render() {
      return(
          <Row id="frame_2_rect">
            <Col sm={4}>
              <ButtonGroup vertical className="elevator">
                <Button variant="" className="elevator_up_arrow">
                  <Image src={arrow_up} />
                </Button>
                <Button variant="" className="elevator_level_one light">
                  Learn
                </Button>
                <Button variant="" className="elevator_level_two light"> 
                  Discover
                </Button>
                <Button variant="" className="elevator_level_three light">
                  Watch
                </Button>
                <Button variant="" className="elevator_down_arrow">
                  <Image src={arrow_down} />
                </Button>
              </ButtonGroup>
            </Col>
            <Col sm={8}>
              <Image src={learn_phone}
                id="learn_phone"/>
            </Col>
          </Row>
      )
  }
}

export default LandingVertCarousel;