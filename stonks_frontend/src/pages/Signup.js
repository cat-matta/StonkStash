import React, {Component} from 'react';
import {Link, withRouter, Redirect} from 'react-router-dom';


/** The Registration page for the app.
 * 
 */
class Signup extends Component {
  constructor(props){
    super(props);
    this.state = { 
      username: '', // Probably going to be a display name if there is a social component
      firstname: '', // As of now first and last name fields are being considered, not final
      lastname: '',
      email: '',  // Likely to be the login field
      email2: '', // email verification
      phonenumber: '', // expecting to store phone numbers as we charge for services
      password: '', // We must come up with conditions for a valid email
      password2: '', // standard password verification
      success: false, // if true, redirect to Login page
      error: false, // if true, depict errors in this.state.errmsg
      errmsg: ''  // Loaded with error text if something goes wrong locally or otherwise
    };
  }

  // Responds to changes in any given field, updates specific state items
  onChange = e => {
    this.setState({ [e.target.id]: e.target.value });
  }

  // Packages the information given by the User and makes an HTTP request to the backend to register.
  onSubmit = e => {
    e.preventDefault();

    // Two schools of thought brewing
    // 1. Do HTTP request here
    // 2. or create file with functions doing the requests and import

  }
  render() {
    // There WILL be behavior changes here due to actions taken by the User

    // Like this
    let error_text = ""
    if (this.state.success) return <Redirect to="/login" />;
    if (this.state.error) error_text = Object.values(this.state.errmsg);
    return(
      <h1>Signup: Work in Progress</h1> 
    )
  }
}

export default withRouter(Signup);