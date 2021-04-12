import React, {Component} from 'react';
import {Link, withRouter, Redirect} from 'react-router-dom';
import { signupCall } from '../utils/requestFunctions';


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
  onSubmit = async e => {
    e.preventDefault();

    const userData = {
      username: this.state.username,
      firstname: this.state.firstname,
      lastname: this.state.lastname,
      email: this.state.email,
      email2: this.state.email2,
      phonenumber: this.state.phonenumber,
      password: this.state.password,
      password2: this.state.password2,
    };

    const result = await signupCall(userData);

    if(result.success) {
      this.setState({
        success: true
      });
    } else if(result.error) {
      this.setState({
        error: true,
        errmsg: result.errmsg
      });
    }

  }

  
  render() {
    // There WILL be behavior changes here due to actions taken by the User

    // Like this
    let error_text = ""
    if (this.state.success) return <Redirect to="/login" />;
    if (this.state.error) error_text = Object.values(this.state.errmsg);
    return (
      <div>
          <div >
             
              <form>
              
                  <h1>Sign Up</h1>
                  <span>Conditions for Username and Password are shown when cursor is hovered over them.</span>   
                  <span >
                      {error_text}
                  </span>

                  <div className="form-group">
                      <input type="text" 
                      id="email"
                      onChange={this.onChange}
                      value={this.state.email}
                      placeholder="email address"/>
                  </div>

                  <div className="form-group">
                      <input type="text" 
                      id="username"
                      onChange={this.onChange}
                      value={this.state.name}
                      placeholder="Username"
                      data-toggle="tooltip"
                      title="Must be between 6 and 20 characters"/>
                  </div>

                  <div className="form-group">
                      <input type="password" 
                      id="password"
                      onChange={this.onChange}
                      value={this.state.password} 
                      placeholder="Password"
                      data-toggle="tooltip"
                      title="Must be between 8 and 30 characters, with one lowercase, one uppercase, and one numeric character"/>
                  </div>

                  <div className="form-group">
                      <input type="password" 
                      id="password2"
                      onChange={this.onChange}
                      value={this.state.password2}
                      placeholder="Confirm Password"/>
                  </div>

                  <div className="form-group">
                      <input type="number" 
                      id="phonenumber"
                      onChange={this.onChange}
                      value={this.state.phonenumber}
                      placeholder="Phone Number"/>
                  </div>

                  <button onClick={this.onSubmit} >Register</button>
                  <p>Already have an account? <Link to="/login"><strong>Login</strong></Link></p>


              </form>
          </div>
      </div>
  );
  }
}

export default withRouter(Signup);