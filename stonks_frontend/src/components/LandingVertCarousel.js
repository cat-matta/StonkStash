import {Component} from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Image from 'react-bootstrap/Image';
import { ToggleButtonGroup, ToggleButton } from 'react-bootstrap';

// Our resources
import arrow_up from '../images/elevator_arrow_up.png';
import arrow_down from '../images/elevator_arrow_down.png';
import learn_phone from '../images/learn_phone.png';
import discover_phone from '../images/discover_phone.png';
import watch_phone from '../images/watch_phone.png';
import loc from '../locate/en/translate.json'; // testing/prep for localization/translation


function LVCContent( {img_src, heading, text} ) {

  return(
    <div>
      <div className="light vc_header">{ heading }</div>
      <div className="light vc_text">{ text }</div>
    </div>
  )

}

/** The thing with the buttons that change the content of the section */
class LandingVertCarousel extends Component {

  constructor(props) {
    super(props);

    this.state = {
      selection: "learn"
    };
  };

  //TODO: Set up functionality for arrows
  onChange = val => {

    if(val === "+") {
      // this thing
      const up_dict = {
        "learn": "watch",
        "discover": "learn",
        "watch": "discover"
      };

      val = up_dict[this.state.selection];

    } else if(val === "-") {
      // that thing
      const down_dict = {
        "learn": "discover",
        "discover": "watch",
        "watch": "learn"
      };

      val = down_dict[this.state.selection];
    }
    this.setState({ selection: val});
  };

  render() {

      const lv_content = loc.landing[this.state.selection];


      const phone_dict = {
        "learn": learn_phone,
        "discover": discover_phone,
        "watch": watch_phone
      }
      const phone_img_src = phone_dict[this.state.selection];

      return(
          <Row id="frame_2_rect">
            <Col sm={4}>
              <ToggleButtonGroup vertical name="landing-vert-group" value={this.state.selection} onChange={this.onChange}  className="elevator">
               
                <ToggleButton value="+" variant="" className="elevator_up_arrow">
                  <Image src={arrow_up} />
                </ToggleButton>

                <ToggleButton value="learn" variant="" className="elevator_level_one light">
                  Learn
                </ToggleButton>
                <ToggleButton value="discover" variant="" className="elevator_level_two light"> 
                  Discover
                </ToggleButton>
                <ToggleButton value="watch" variant="" className="elevator_level_three light">
                  Watch
                </ToggleButton>

                <ToggleButton value="-" variant="" className="elevator_down_arrow">
                  <Image src={arrow_down} />
                </ToggleButton>
              </ToggleButtonGroup>
            </Col>
            <Col sm={4}>
              <Image src={phone_img_src}
                id="learn_phone"/>
            </Col>
            <Col sm={4}>
              <LVCContent heading={lv_content.heading} text={lv_content.text}/>
            </Col> 
          </Row>
      )
  }
}

export default LandingVertCarousel;