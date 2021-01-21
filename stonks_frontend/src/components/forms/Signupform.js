import { StatusBar } from 'expo-status-bar';
import React, {Component} from 'react';
import {StyleSheet, Text, TextInput, View, Button, TouchableOpacity } from 'react-native';

const SignupValidation = require("../../utils/SignupValidation");


/** The component representing the form for user input in registering a new account.
 * @pre  The app is running and the backend can recieve requests
 * @post  If the information supplied is valid, a new User is created and the user is transported to the Login screen.
 * @props  navigation  An object taken from the navigation stack needed to redirect users
 * @return  The JSX needed to render the forms.
 */
class Signupform extends Component {

  state = { 
    username: "", 
    email: "", 
    email2: "", 
    password: "", 
    password2: "",
    success: false, // if true, time to move on
    error: false, // if an issue has arrisen in the signup process, this will be true
    errmsg: '' // will be filled and displayed if an error has occured
  };

  onChange = e => {
    this.setState({ [e.target.id]: e.target.value });
  }
  onSubmit = e => {
    e.preventDefault();
    try {
      // Once authentication routes are made, submit stuff here.
      // ensure validation of email, password, username, etc and rejection if bad
      // TODO: determine requirements for each field.

      // To send to Front End input validation helper function
      const newUser={
        username: this.state.username,
        email: this.state.email,
        email2: this.state.email2,
        password: this.state.password,
        password2: this.state.password2
      };

      const results = SignupValidation(newUser);
      if(!results.isValid) throw(results.errors);
      else {
        

        // Info transmission

        fetch("api/signup", { 
          method: 'POST',
          body: JSON.stringify({ newUser }),
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(data => {
          if(data.success === false) throw(data.errors);
          else this.setState({success: true});
        })
      }

      //this.props.navigation.navigate('Login'); 
      /* due to the change in nav from react to rn, unsure where to place. Here works but as Ive done before redirects are handled in the render
      function.*/
    }
    catch(err) {
      console.log(err);
      this.setState({error: true, errmsg: err});
      // display errors at the top of the signup form
    }
     

  }
  
  render(){
    let error_text = "";
    if(this.state.success) this.props.navigation.navigate('Login');
    if(this.state.error) error_text = Object.values(this.state.errmsg);
    return (
      <View style ={styles.container}>
        <Text style= {styles.errorText}>{error_text}</Text>
        <TextInput 
          id="username"
          placeholder="Username"
          placeholderTextColor='#FFF'
          textContentType="username"
          style ={styles.input}
          value ={this.state.username}
          onChangeText = { this.onChange} 
          />
        <TextInput
          id="email" 
          placeholder= "Email"
          placeholderTextColor= '#FFF'
          textContentType= "emailAddress"
          style ={styles.input}
          value = {this.state.email}
          onChangeText = { text => this.setState({email: text})} 
          />
        <TextInput 
          id="email2"
          placeholder= "Confirm Email"
          placeholderTextColor= '#FFF'
          textContentType= "emailAddress"
          style ={styles.input}
          value = {this.state.email2}
          onChangeText = { text => this.setState({email2: text})} 
          />
        <TextInput 
          id="password"
          placeholder= "Password"
          placeholderTextColor='#FFF'
          textContentType= "password"
          secureTextEntry= { true } 
          style ={styles.input}
          value = {this.state.password}
          onChangeText = { text => this.setState({password: text})} 
          />
        <TextInput 
          id="password2"
          placeholder= "Confirm Password"
          placeholderTextColor='#FFF'
          textContentType= "password"
          secureTextEntry= { true } 
          style ={styles.input}
          value = {this.state.password2}
          onChangeText = { text => this.setState({password2: text})} 
          />

        <TouchableOpacity style={styles.buttonContainer}>
          <Button style={styles.buttonText}
            onPress={this.submitSignup()}
            title="Submit"/>


       </TouchableOpacity>
      </View>
      
   
    );

  }
  
}

const styles = StyleSheet.create({
  container: {
      padding:20
  },
  input:{
      height:40,
      backgroundColor: '#55efc4',
      marginBottom:20, 
      paddingHorizontal: 10,
      textAlign: 'center'  

  },
  buttonContainer:{
      backgroundColor: '#1dd1a1',
      paddingVertical: 10, 
      textAlign:'center',
  },
  buttonText:{
      textAlign:'center', 
      color: '#FFFFFF'
  },
  errorText: {
    textAlign:'center',
    color: '#BB0000'
  }

});

export default Signupform;