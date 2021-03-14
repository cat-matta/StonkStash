import React, { Component } from 'react';
import { ToggleButton, ToggleButtonGroup } from 'react-bootstrap';
import { Line } from '@nivo/line';
import AutoSizer from "react-virtualized-auto-sizer"; // cause nivo's responsive components dont play nice within flexbox or css flex components

/* This component with display all graph stuff within the Dashboard page.
 * It will utilise the C3.js library to render graphs.
 * Surely the component to be most frequently updated out of all the dashboard components. */

// Required to remove grids, axis ticks, and the such from displaying.
const top_theme = {
    "textColor": "#054939",
    "fontSize": 14,
    "axis": {
        "domain": {
            "line": {
                "stroke": "#94cfc1",
                "strokeWidth": 3
            }
        },
        "ticks": {
            "line": {
                "stroke": "#777777",
                "strokeWidth": 0
            }
        }
    },
    "grid": {
        "line": {
            "stroke": "#dddddd",
            "strokeWidth": 1
        }
    }
}
// ditto
const bottom_theme = {
    "textColor": "#054939",
    "fontSize": 14,
    "axis": {
        "domain": {
            "line": {
                "stroke": "#94cfc1",
                "strokeWidth": 3
            }
        },
        "ticks": {
            "line": {
                "stroke": "#777777",
                "strokeWidth": 0
            }
        }
    },
    "grid": {
        "line": {
            "stroke": "#dddddd",
            "strokeWidth": 1
        }
    }
}


/** This is an attempt at documenting the inputs of our DashGraphView component, which will display all
 * graphs on the Dashboard page. This can be one line graph at a time per a given, or two line graphs.
 * This will likely be determined by some outward forces/inputs.
 * 
 * There is also the matter of different control bars being displayed for the graph view depending on, again, those outward forces/inputs.
 * The graphs size/resize themselves well so lets hope introducing some more things doesn't cause it to shit the bed.
 * 
 * ALSO THE graph(s) should always come with a radiobox button group to switch between time series's.
 * 
 * The data itself, I'll try to make sense of here.
 * @property  priceData  Data of a stocks price over some time series
 * @property  otherData  Data for the blue and red graph (will be properly named once info is provided)
 */
class DashGraphView extends Component {

    

    constructor(props) {
        super(props);

        // the data will likely be updated based upon activity outside of the current component,
        // which will then likely be handed in via props. Should have some documentation on how
        // the data must be formatted when it arrives.

        // data seems to require being in some form like [{},...{}] (an array of objects)
        // These objects it seems need to have an "id" property {string}, and a "data" property {array of objects}.
        // Now THAT property, "data", is where the plottable stuff is. Seems everything must be formatted in an
        // { 
        // "x": {number},
        // "y": {number}
        // }
        // manner. The "color" {string} property doesn't matter. Nivo uses color palettes spec'd in the graph component declaration.
        this.state = {
            data: this.props.priceData, // single line info
            data2: this.props.otherData, // double line info
            time_choice: "1D"
        };

    }

        // Responds to changes in selected time series choice
        onChange = val => {

            this.setState({ time_choice: val });
            this.props.cb(val);
        }

    render() {
        /** The addition of the AutoSizer wrapper was neccesary due to the <ResponsiveLine> graph component
         * refusing to play nicely within a flexbox component (bootstrap containers, rows, cols, etc). Specifically
         * when the second graph was added. Wouldn't adjust to the height constraints of their parent. This works good so far.
         * 
         * NOTES:
         * 1) Graphs are splitting the height of their parent component 2/3 : 1/3 (top and bottom, respectively). Seems as close to the doc I can get
         * while remaining "responsive".
         */
        return(
            <AutoSizer> 
                {({ height, width }) => (
                    <div>
                        <ToggleButtonGroup name="graph-time-bar" className ="graph-time-group" type="radio" value={this.state.selection} onChange={this.onChange} defaultValue={this.state.selection} >
                            <ToggleButton value={"1D"} variant="" id="1D" className="graph-time-button">1D</ToggleButton>
                            <ToggleButton value={"1W"} variant="" id="1W" className="graph-time-button">1W</ToggleButton>
                            <ToggleButton value={"1M"} variant="" id="1M" className="graph-time-button">1M</ToggleButton>
                            <ToggleButton value={"6M"} variant="" id="6M" className="graph-time-button">6M</ToggleButton>
                            <ToggleButton value={"1YR"} variant="" id="1YR" className="graph-time-button">1YR</ToggleButton>
                            <ToggleButton value={"5YR"} variant="" id="5YR" className="graph-time-button">5YR</ToggleButton>
                        </ToggleButtonGroup>
                        <Line
                            data={this.state.data}
                            theme={top_theme}
                            height={height*0.66}
                            width={width}
                            margin={{ top: 50, right: 110, bottom: 0, left: 60 }}
                            xScale={{ type: 'linear' }}
                            yScale={{ type: 'linear', min: 'auto', max: 'auto', reverse: false }}
                            yFormat=" >-.2f"
                            axisTop={null}
                            axisRight={null}
                            axisBottom={{
                                orient: 'bottom',
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: 0,
                                legendOffset: 36,
                                legendPosition: 'middle'
                            }}
                            axisLeft={{
                                orient: 'left',
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: 0,
                                legendOffset: -40,
                                legendPosition: 'middle'
                            }}
                            enableGridX={false}
                            enableGridY={false}
                            colors={"#94cfc1"}
                            pointSize={0}
                            pointColor={{ theme: 'background' }}
                            pointBorderWidth={2}
                            pointBorderColor={{ from: 'serieColor' }}
                            pointLabelYOffset={-12}
                            useMesh={true}
                        />
                        <Line
                            data={this.state.data2}
                            theme={top_theme}
                            height={height*0.33}
                            width={width}
                            margin={{ top: 0, right: 110, bottom: 30, left: 60 }}
                            xScale={{ type: 'linear', min: 'auto', max: 'auto', reverse: false }}
                            yScale={{ type: 'linear', min: 'auto', max: 'auto', reverse: false }}
                            yFormat=" >-.2f"
                            axisTop={null}
                            axisRight={null}
                            axisBottom={{
                                orient: 'bottom',
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: 0,
                                legendOffset: 36,
                                legendPosition: 'middle'
                            }}
                            axisLeft={{
                                orient: 'left',
                                tickSize: 5,
                                tickPadding: 5,
                                tickRotation: 0,
                                legendOffset: -40,
                                legendPosition: 'middle'
                            }}
                            enableGridX={false}
                            enableGridY={false}
                            colors={["#2841D1", "#D12C21"]}
                            pointSize={0}
                            pointColor={{ theme: 'background' }}
                            pointBorderWidth={2}
                            pointBorderColor={{ from: 'serieColor' }}
                            pointLabelYOffset={-12}
                            useMesh={true}
                        />
                </div>
                )}  
            </AutoSizer>  
            );
    }
}

export default DashGraphView;