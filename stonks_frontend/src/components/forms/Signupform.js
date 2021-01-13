import { StatusBar } from 'expo-status-bar';
import React, {Component} from 'react';
import {StyleSheet, Text, TextInput, View, Button, TouchableOpacity } from 'react-native';

class Signupform extends Component {

  state = { username: "", email: "", email2: "", password: "", password2: ""};
  
  render(){
    return (
      <View style ={styles.container}>
        <TextInput 
          placeholder="Username"
          placeholderTextColor='#FFF'
          textContentType="username"
          style ={styles.input}
          value ={this.state.username}
          onChangeText = { text => this.setState({username: text})} 
          />
        <TextInput 
          placeholder= "Email"
          placeholderTextColor= '#FFF'
          textContentType= "emailAddress"
          style ={styles.input}
          value = {this.state.email}
          onChangeText = { text => this.setState({email: text})} 
          />
        <TextInput 
          placeholder= "Confirm Email"
          placeholderTextColor= '#FFF'
          textContentType= "emailAddress"
          style ={styles.input}
          value = {this.state.email2}
          onChangeText = { text => this.setState({email2: text})} 
          />
        <TextInput 
          placeholder= "Password"
          placeholderTextColor='#FFF'
          textContentType= "password"
          secureTextEntry= { true } 
          style ={styles.input}
          value = {this.state.password}
          onChangeText = { text => this.setState({password: text})} 
          />
        <TextInput 
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
            onPress={ () => {

                try {
                  // Once authentication routes are made, submit stuff here.
                  // ensure validation of email, password, username, etc and rejection if bad
                  // TODO: determine requirements for each field.

                  // To send to Front End input validation helper function
                  const newUserFields={
                    username: username,
                    email: email,
                    email2: email2,
                    password: password,
                    password2: password2
                  };

                  // Proposed Field validations
                  /** Username => min len, maxlen, no special characters (Im guessing it might be like a display name, idk) */

                  /** Email => must be in email form, if we get to fr deployment, actually check that the email exists */

                  /** Email2 => If email 1 passes validation, email2 === email */

                  /** Password => min len, max len, perhaps {1 capital, 1 lowercase, 1 num, 1 special char} */

                  /** Password2 => if password1 passes, password2 === password */

                  // If all fields pass validation, send it off to the backend to register new user.
                    // If success, move on to the login screen
                    // else throw error and explain reason (local validation error, not serverside shit)

                  this.props.navigation.navigate('Login');
                }
                catch(err) {
                  console.err(err);
                }
                
            } }
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
  }

});

export default Signupform;