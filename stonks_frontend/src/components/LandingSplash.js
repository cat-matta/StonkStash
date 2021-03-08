import {Component} from 'react';
import {Row, Col, Image} from 'react-bootstrap';

import pitch_phone from '../images/pitch_phone.png';

/** The whole "Welcome to STONKSTASH" block */
class LandingSplash extends Component {
  render() {
      return(
      <Row id="splash">
        <Col>
          <div id="welcome_text" className="light">Welcome to StonkStash</div>
          <Image id="pitch_phone" src={pitch_phone} />
          <p className="light">Our mission is to help YOU use the free investing resources of today to your benefit rather than your detriment.</p>
        </Col>
      </Row>
      )
  }
}

export default LandingSplash;