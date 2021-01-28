import React, { Component } from 'react';
import { Redirect, Link } from 'react-router-dom';

/** Where the most regular authentication will come into play. Gateway to the site and its services. */
class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '', // user's email address they registered with.
      password: '', // "plaintext" user attempt at submitting the right password corresponding to the email given,
      success: false, // if true, redirect to Dashboard
      redirectToReferrer: false, // In the event someone 
      error: false, // if true, display this.state.errmsg to user,
      errmsg: '', // Contains any user appropriate error messages, local or otherwise
    }
  }

  // changes value of corresponding state element
  onChange = e => {
    this.setState({ [e.target.id]: e.target.value });
  }

  // packages field values and shoots an HTTP request to the backend
  onSubmit = e => {
    e.preventDefault();
  }

  render() {
    if (this.state.success === true) return <Redirect to="/dashboard" />;


    const { from } = this.props.location.state || {from: {pathname: '/'} };
    const { redirectToReferrer, failed } = this.state;

    if (redirectToReferrer) {
        return <Redirect to={from} />;
    }

    let err = "";
    if (failed) {
        err = <div className="alert alert-danger" role="alert">Login Failed</div>;
    }

    return(
      <h1>Login: Not yet available</h1>
    )
  }
}

export default Login;