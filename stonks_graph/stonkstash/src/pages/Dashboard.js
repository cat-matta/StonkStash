import React, { Component } from 'react';
import { Container, Row, Col } from 'react-bootstrap';

// The components which will form the interface
import DashTopNav from '../components/DashTopNav';
import DashBottomNav from '../components/DashBottomNav';
import DashGraphView from '../components/DashGraphView';
import DashSidePanel from '../components/DashSidePanel';

import MarketListPanel from '../components/MarketListPanel'; // as shown in "Macbook - 14"
import BalanceSheetVolPanel from '../components/BalanceSheetVolPanel'; // as shown in "Macbook - 13"

// Function to get stock data from backend. Should be placed into requestFunctions.js when integrated into front end main
import { getStockInfo } from '../utils/stockDataRequests';



import "../css/Dashboard.css";
require('bootstrap');

/* Unimplemented*/
let WatchlistPanel = null; // The 2 wide, n/2 deep panel; from "Macbook - 12"

const DEMO_PRICE_DATA = [
    {
      "id": "stonk",
      "data": [
        {
          "x": 0,
          "y": 256
        },
        {
          "x": 1,
          "y": 218
        },
        {
          "x": 2,
          "y": 9
        },
        {
          "x": 3,
          "y": 274
        },
        {
          "x": 4,
          "y": 54
        },
        {
          "x": 5,
          "y": 270
        },
        {
          "x": 6,
          "y": 263
        },
        {
          "x": 7,
          "y": 75
        },
        {
          "x": 8,
          "y": 46
        },
        {
          "x": 9,
          "y": 181
        },
        {
          "x": 10,
          "y": 200
        },
        {
          "x": 11,
          "y": 140
        }
      ]
    }
  ];

  const DEMO_MACD_DATA = [
    {
      "id": "blue",
      "data": [
        {
          "x": 0,
          "y": 80
        },
        {
          "x": 1,
          "y": 76
        },
        {
          "x": 2,
          "y": 70
        },
        {
          "x": 3,
          "y": 95
        },
        {
          "x": 4,
          "y": 55
        },
        {
          "x": 5,
          "y": 96
        },
        {
          "x": 6,
          "y": 90
        },
        {
          "x": 7,
          "y": 35
        },
        {
          "x": 8,
          "y": 75
        },
        {
          "x": 9,
          "y": 65
        },
        {
          "x": 10,
          "y": 85
        },
        {
          "x": 11,
          "y": 30
        }
      ]
    },
    {
        "id": "red",
        "data": [
          {
            "x": 0,
            "y": 40
          },
          {
            "x": 1,
            "y": 48
          },
          {
            "x": 2,
            "y": 5
          },
          {
            "x": 3,
            "y": 45
          },
          {
            "x": 4,
            "y": 4
          },
          {
            "x": 5,
            "y": 10
          },
          {
            "x": 6,
            "y": 25
          },
          {
            "x": 7,
            "y": 34
          },
          {
            "x": 8,
            "y": 50
          },
          {
            "x": 9,
            "y": 35
          },
          {
            "x": 10,
            "y": 15
          },
          {
            "x": 11,
            "y": 20
          }
        ]
      }
  ];

  const DEMO_MARKET_DATA = [
    {"symbol": "AAPL", "price": 137.05, "change": 5.02, "percent": 3.80},
    {"symbol": "MSFT", "price": 225.00, "change": 0.66, "percent": 0.29},
    {"symbol": "AMZN", "price": 3304.08, "change": 40.70, "percent": 1.25},
    {"symbol": "TSLA", "price": 842.77, "change": -7.68, "percent": -0.90},
    {"symbol": "FB", "price": 273.20, "change": 5.72, "percent": 2.14},
    {"symbol": "GOOG", "price": 1891.00, "change": 13.93, "percent": 0.74},
    {"symbol": "AAPL", "price": 800, "change": 1.3, "percent": 1.2},
    {"symbol": "BBSL", "price": 305, "change": -51.3, "percent": -1.2},
    {"symbol": "AAPL", "price": 800, "change": 1.3, "percent": 1.2},
    {"symbol": "BBSL", "price": 305, "change": -51.3, "percent": -1.2},
    {"symbol": "AAPL", "price": 800, "change": 1.3, "percent": 1.2},
    {"symbol": "BBSL", "price": 305, "change": -51.3, "percent": -1.2},
    {"symbol": "AAPL", "price": 800, "change": 1.3, "percent": 1.2},
    {"symbol": "BBSL", "price": 305, "change": -51.3, "percent": -1.2},
    {"symbol": "AAPL", "price": 800, "change": 1.3, "percent": 1.2},
    {"symbol": "BBSL", "price": 305, "change": -51.3, "percent": -1.2}];

    
    const DEMO_CURRENT_STOCK = "AAPL"; // for querying stock info.

/* Post Login Page. Has graphs, navs to other pages, etc. Lots of action will occur here
 * insofar as api data being displayed and what not. Docs will get fleshed as we come closer to
 * what we want to achieve.  */
class Dashboard extends Component {


    constructor(props) {
        super(props);
        this.state = {
            focused_stock_ticker: (DEMO_CURRENT_STOCK === null) ? undefined : DEMO_CURRENT_STOCK, // an "infocus" stock is the one being displayed in the graph
            time_range_state: "1D", // assuming whatever api we are using requires a time range for a query

            price_data: DEMO_PRICE_DATA, // can be updated or replaced by other sub component's actions
            macd_data: (DEMO_MACD_DATA === null) ? undefined : DEMO_MACD_DATA, // ditto. named as such until clarity of the red blue graph is provided

            market_list_data: (DEMO_MARKET_DATA === null) ? undefined : DEMO_MARKET_DATA,

            bar_state: "market", // used to choose which side menu panel to display, based upon status of BottomBar and Sidebar itself(?)
        }

            const stockinfo = getStockInfo('AAPL', '1', "2021-03-16", 'w');
            console.log(stockinfo);
        
    
      }

    
    /** Allows Dashboard to switch between sidepanel elements based on the DashBottomNav's current status
     * @param  selection  {String}  The id of the button pressed in the DashBottomNav's button group.
     * @post  A different side panel element, corresponding to the user's choice, will be displayed.
     */
    barStateCallback = (selection)  => {
        this.setState({bar_state: selection});
        console.log(selection)
    }

    /** To allow the dashboard to acquire data within a different time period based on user input.
     * @param  selection  {String}  The id of the time period selected within the DashGraphView's interface.
     * @post  A call to the API will be made using the time period the user has selected.
     */
    graphTimeCallback = (selection) => {
        // using <current stock symbol>, the chosen time range by the user, and whatever else needed,
        // make a call to get new price data for the currently displayed/chosen stock
        // Change the state to hold this new data,
        // then of course pass in new data during render().
    }

    render(){

        // To quickly change SidePanel element based on current state of user input
        const barStateToComponent = {
            "picks": () => {return <BalanceSheetVolPanel />}, /*{return WatchlistPanel}*/ 
            "balance": () => {return <BalanceSheetVolPanel />},
            "market": () => {return(<MarketListPanel data={this.state.market_list_data} />)},
        }

        const sideMenuComponent = barStateToComponent[this.state.bar_state](); // always make sure to add your round brackets for what I did with that dict tfu

        return(
            <Container fluid>
                <DashTopNav />
                <Row>  
                    <Col xs={7} className="graph-parent">
                        <DashGraphView priceData={this.state.price_data} macdData={this.state.macd_data} />
                    </Col>
                    <Col className="right-menu"> {sideMenuComponent} </Col>
                </Row>
                <Row className="bottom-menu-bar">
                    <DashBottomNav cb={this.barStateCallback} />
                </Row>

            </Container>)
    }
}

export default Dashboard;