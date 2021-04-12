import {React, Component} from 'react';
import {downloadFileCall} from '../utils/requestFunctions';

class DownloadLink extends Component {
    
  constructor(props) {
    super(props);
  }

  onClick = e => {
    // This is actually being called, dont rely on the terminal console, check the browser's
    e.preventDefault();
    const result = downloadFileCall(this.props.filename);
  }

  render() {
    return(
      <button id={this.props.id}
        className={this.props.className} 
        target="_blank" 
        href="#dl"  
        onClick={this.onClick}
        >{this.props.text}</button>
    )
  }
}

export default DownloadLink;