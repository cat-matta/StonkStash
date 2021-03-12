import React, { Component } from 'react';

import { ResponsiveLine } from '@nivo/line';

/* This component with display all graph stuff within the Dashboard page.
 * It will utilise the C3.js library to render graphs.
 * Surely the component to be most frequently updated out of all the dashboard components. */

const theme = {
    //"background": "#ffffff",
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
class DashGraphView extends Component {

    

    constructor(props) {
        super(props);

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
              ]
        }

        // state stuff
    }

    render() {
        return(
            <ResponsiveLine
                    data={this.state.data}
                    theme={theme}
                    margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
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
            );
    }
}

export default DashGraphView;