import React, { Component } from 'react';
import {ListGroup} from 'react-bootstrap';


/** Formats the data of a given stock within the state's array of stocks, into a viewable list item.
 * @param  symbol  {String} The ticker symbol of the given stock.
 * @param  price  {(non-neg) Number, fp} The current price of the given stock.
 * @param  change  {Number, fp} The price change since uh....
 * @param  percent  {Number, fp} The price change since uh...., represented as a percentage
 * 
 */ 
function MarketListItem( {symbol, price, change, percent }) {

    let performanceColor = ""
    if(change >= 0) performanceColor = "green-text";
    else if (change < 0) performanceColor = "red-text";
    else performanceColor = "grey"; // this is for some weird error case I cant exactly see but I see the shape of it in my thoughts and that worries me enough (something like NaN and that stuff)
  
    return (
        <ListGroup.Item className={performanceColor}>{symbol} {price} {change}({percent}%)</ListGroup.Item>
   );
}

/** Will display stock prices and such of search results or whatever is supplied. 
 * A variant of content for the Dashboard SidePanel.
 * SHOULD BE *scrollable* if the data displayed exceeds the space allotted
 * @property data {Array<{
 *                      @member symbol {String}, Ticker Symbol
 *                      @member price {(non-neg) Number}, Current Price
 *                      @member change {Number, fp} , price change since <WHENEVER>
 *                      @member percent  {Number, fp}, price change in percentage since <WHENEVER>
 *                      } }
 * @pre  The User is on the Dashboard page
 * @post  Stocks will be displayed along with their Ticker Symbol, price, and performance, from within a list
*/
class MarketListPanel extends Component {

    constructor(props) {
        super(props);
        
        this.state = {
            data: (!this.props.data) ? undefined : this.props.data, // data provided from outside
            error: (!this.props.data) ? true : false

        }
    }

    render() {

        let stocks = "";
        if(this.state.data !== undefined) {
            stocks = this.state.data.map((stock, ii) => {
              return(
                <MarketListItem 
                  symbol={stock.symbol}
                  price={stock.price}
                  change={stock.change}
                  percent={stock.percent}
                  key={ii}
                  />
              );
            })
          } else stocks = (<li>"Can't Fetch Data"</li>); //TODO(Hashem forgive me for uttering such): get the error case item to have red or warning colored text


        return(
            <ListGroup>
                {stocks}
            </ListGroup>
        )
    }
}

export default MarketListPanel;