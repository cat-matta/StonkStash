import React, { Component, useContext } from 'react';
import { Tabs, Tab, Accordion, Card, AccordionContext } from 'react-bootstrap';
import { useAccordionToggle } from 'react-bootstrap/AccordionToggle';


// import AccordionGraph from wherever // for the graph that appears when you click a list element.

// space complexity impl
import rightArrowGreen from '../images/right_arrow_green.png';
import downArrowGreen from '../images/down_arrow_green.png';
import rightArrowRed from '../images/right_arrow_red.png';
import downArrowRed from '../images/down_arrow_red.png';

// time complexity impl (sort of)
// Turns out one cannot simply change the hue or color of an img element.
import rightArrow from '../images/right_arrow.png';
import downArrow from '../images/down_arrow.png';


/** Sort of jacked from the React-Bootstrap docs.
 * @param  children  whatever html elements or text is within the corresponding Accordion.Collapse element
 * @param  eventKey  {Number}  The key value assigned to the element, setting it apart from others currently displayed (to the Accordion element).
 * @param  callback  Guessing this is a callback function but I'm not entirely sure what it is.
 */
function ContextAwareToggle({ children, eventKey, callback}) {
    const currentEventKey = useContext(AccordionContext);

    const decoratedOnClick = useAccordionToggle(
        eventKey,
        () => callback && callback(eventKey),
    );

    const isCurrentEventKey = currentEventKey === eventKey;

    const isFlag = false; // for now, will be determined by api data or our calculations.

    let textColor;
    let imageSrc;

    if (!isFlag) {
        textColor = "green-text";
        imageSrc = isCurrentEventKey ? downArrowGreen : rightArrowGreen;
    } else {
        textColor = "red-text";
        imageSrc = isCurrentEventKey ? downArrowRed : rightArrowRed;
    }


    return( 
        <div
            type="button"
            className={ textColor }
            onClick={decoratedOnClick}
            >
                {children} <img src={ imageSrc } />
            </div>
    );
}


/** A component for the BalanceSheet/Volitility interface in the Dashboard.
 * Each option in a tab isn't a control or value to be set, rather a collapsed display of data. 
 * The collapsed form gives it to the user with brevity, while the expanded form of a row option
 * (denoted by a downard arrow like 'v' but wider ofc) has a number line scale with a more verbose description to
 * explain what exactly the user is looking at and what judgements they should draw from that data.
 */
class BalanceSheetVolPanel extends Component {
    
    constructor(props) {
        super(props);
        this.state = { 
            balance_data: (this.props.balanceData) ? this.props.balanceData : undefined,
            volitility_data: (this.props.volitilityData) ? this.props.volitilityData : undefined 
        }
    }

    render() {
        return(
            <Tabs defaultActiveKey="balance-sheet">
                <Tab eventKey="balance-sheet" title="Balance Sheet">
                    <Accordion>
                        <Card>
                        <Card.Header>
                            <ContextAwareToggle eventKey="0">Current Working Capital Ratio</ContextAwareToggle>
                        </Card.Header>
                            <Accordion.Collapse eventKey="0">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                        <Card>
                            <Card.Header>
                                <ContextAwareToggle eventKey="1">Quick Ratio</ContextAwareToggle>
                            </Card.Header>
                            <Accordion.Collapse eventKey="1">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                        <Card>
                            <Card.Header>
                                <ContextAwareToggle eventKey="2">Working Capital/Assets</ContextAwareToggle>
                            </Card.Header>
                            <Accordion.Collapse eventKey="2">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                        <Card>
                            <Card.Header>
                                <ContextAwareToggle eventKey="3">Debt Worth Ratio</ContextAwareToggle>
                            </Card.Header>
                            <Accordion.Collapse eventKey="3">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                        <Card>
                            <Card.Header>
                                <ContextAwareToggle eventKey="4">Flow to Income</ContextAwareToggle>
                            </Card.Header>
                            <Accordion.Collapse eventKey="4">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                        <Card>
                            <Card.Header>
                                <ContextAwareToggle eventKey="5">Conservative (Just Cash)</ContextAwareToggle>
                            </Card.Header>
                            <Accordion.Collapse eventKey="5">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                        <Card>
                            <Card.Header>
                                <ContextAwareToggle eventKey="6">Cash and Short Term Investments</ContextAwareToggle>
                            </Card.Header>
                            <Accordion.Collapse eventKey="6">
                                <Card.Body>sup</Card.Body>
                            </Accordion.Collapse>
                        </Card>
                    </Accordion>
                </Tab>
                <Tab eventKey="volitility" title="Volitility">
                </Tab>
            </Tabs>
        )
    }
};

export default BalanceSheetVolPanel;