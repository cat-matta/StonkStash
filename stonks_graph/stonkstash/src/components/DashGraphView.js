import React, { Component } from 'react';
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
 * The data itself, I'll try to make sense of here.
 * @property  price_data  Data of a stocks price over some time series
 * @property  
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
            data: [
                {
                  "id": "stonk",
                  "color": "#94CFC1",
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
              ],
              data2: [
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
              ]
        }
        

        // state stuff
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
                    <div >
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