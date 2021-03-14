import React, { Component } from 'react';

/** This is where one can view their "favorited" ticker symbols
 * Elements are displayed in a vertical "list like" fashion,
 * the elements are displayed two wide, n/2 long.
 */
class WatchlistPanel extends Component {

    constructor(props) {
        super(props);

        this.state = {
            data: (this.props.data === null) ? undefined : this.props.data, // data provided from outside

        }
    }

    render() {

        if(this.state.data != undefined) {

          } 
        return(
            <ul>
                {stocks}
            </ul>
        )
    }
}

export default WatchlistPanel;