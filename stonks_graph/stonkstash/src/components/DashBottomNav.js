import React, { Component } from 'react';
import { ButtonGroup, Button, Image } from 'react-bootstrap';

// Our custom images
import PicksIcon from '../images/dash_picks_button.png';
import MarketIcon from '../images/dash_market_button.png';
import SearchIcon from '../images/dash_search_button.png';

/* Bottom Navigational Bar for the Dashboard
 * Has 3 options, packed in the center:
 * 1) Your Picks
 * 2) Market
 * 3) Search
 * This will likely influence behavior of all components on the dashboard besides the
 * Top Navigational bar. */
class DashBottomNav extends Component {

    render() {
        return(
            <ButtonGroup>
                <Button variant=""><Image src={PicksIcon}></Image></Button>
                <Button variant=""><Image src={MarketIcon}></Image></Button>
                <Button variant=""><Image src={SearchIcon}></Image></Button>
            </ButtonGroup>
            );
    }
}

export default DashBottomNav;