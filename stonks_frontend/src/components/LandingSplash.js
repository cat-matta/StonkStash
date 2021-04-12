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
          <div class="Retanglearoundphone"></div>

          <div class="firstphone"></div>
          <h1 class= "detail1">
            The only tool you need to become a successful stock market investor.
          </h1>
          <div class="missionstatement">
            <h1 class="missiondetail">
              Our mission is to help YOU use the free investing resources of today to your benefit rather than your detrimate.
            </h1>
          </div>
          
          <button class="informbutton">
            <font face="Coda"><font color="White"><font weight="1"><font align="Center">
              <font size="5">
                <font color="94CFC1">
                Inform Me!
                </font>
              </font>
            </font>

             </font>
              </font></font></button>
        </Col>
      </Row>
      )
  }
}

export default LandingSplash;