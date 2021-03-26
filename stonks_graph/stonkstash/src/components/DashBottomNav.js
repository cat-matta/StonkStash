import React, { Component } from 'react';
import { ToggleButtonGroup, ToggleButton, Image } from 'react-bootstrap';

// Our custom images
import PicksIcon from '../images/dash_picks_button.png';
import MarketIcon from '../images/dash_market_button.png';
import SearchIcon from '../images/dash_search_button.png';

/** Bottom control bar for the dashboard
 * @property  cb  {Function}  A callback function allowing the selected option to be
 * returned to the dashboard.
 */
class DashBottomNav extends Component {

    constructor(props) {
        super(props);

        this.state = {
            selection: "market"
        };
    }

    // Responds to changes in selected bottom bar choice
    onChange = val => {

        this.setState({ selection: val });
        this.props.cb(val);
    }

    render() {
        return(
            <ToggleButtonGroup name="bottom-bar-group" type="radio" value={this.state.selection} onChange={this.onChange} defaultValue={this.state.selection} >
                <ToggleButton value={"picks"} variant="" id="picks"><Image src={PicksIcon}></Image></ToggleButton>
                <ToggleButton value={"market"} variant="" id="market"><Image src={MarketIcon}></Image></ToggleButton>
                <ToggleButton value={"search"} variant="" id="search"><Image src={SearchIcon}></Image></ToggleButton>
            </ToggleButtonGroup>
            );
    }
}

export default DashBottomNav;