import React, { Component } from 'react';


/** Represents favorited stocks as rounded cards, almost. Wide bubbles, idk.
 * @param  symbol  {String} The ticker symbol of the given stock.
 * @param  price  {(non-neg) Number, fp} The current price of the given stock.
 * @param  change  {Number, fp} The price change since uh....
 * @param  percent  {Number, fp} The price change since uh...., represented as a percentage
 * 
 */ 
function WatchlistItem( { symbol, price, change, percent } ) {

    let performanceColor = ""
    if(change >= 0) performanceColor = "green-element";
    else if (change < 0) performanceColor = "red-element";
    else performanceColor = "grey"; // this is for some weird error case I cant exactly see but I see the shape of it in my thoughts and that worries me enough (something like NaN and that stuff)

}

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