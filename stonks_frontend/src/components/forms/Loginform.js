import { StatusBar } from 'expo-status-bar';
import React, {Component} from 'react';
import {StyleSheet, Text, TextInput, View, TouchableOpacity } from 'react-native';

/** A component to render and handle the input of user data for the purpose of logging into the system
 * @pre  The app is running and the backend is capable of recieving requests.
 * @post  Should the information be correct, the user is transported to the Dashboard page.
 * @props  navigation  An object taken from the navigation stack needed to redirect users
 * @return  The JSX required for the form needed to facilitate logging in
 */
class Loginform extends Component {

  state = { 
    email: "", 
    password: "",
    success: false,
    error: false,
    errmsg: ''};

  onChange = e => {
    this.setState({ [e.target.id]: e.target.value });
  }
  
  onSubmit = e => {
    e.preventDefault();


    try {
      // Data packaged for transport
      const loginData = {
        email: this.state.email,
        password: this.state.password
      };


      

      // Info transmission
      fetch("api/login", { 
        method: 'POST',
        body: JSON.stringify({ loginData }),
        headers: {
          'Content-Type': 'application/json',
        }
      })
      .then(data => {
        if(data.success === false) throw(data.errors);
        else this.setState({success: true});
      })
    

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
    let error_text = '';
    if(this.state.success) {
      // some more auth shit should go on here but we are still learning the nuances of react native and other stuff
      // auth shit going on at least at some point between when the data is transmitted and when the user gets redirected.
      // for now we will just redirect
      this.props.navigation.navigate('Dashboard');
    }
    if(this.state.error) {
      error_text = this.state.errmsg;
    }
    return (
      <View style ={styles.container}>
        <Text style= {styles.errorText}>{error_text}</Text>
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
          id="password"
          placeholder= "Password"
          placeholderTextColor='#FFF'
          textContentType= "password"
          secureTextEntry= { true } 
          style ={styles.input}
          value = {this.state.password}
          onChangeText = { text => this.setState({password: text})} 
          />

       <TouchableOpacity style = {styles.buttonContainer}>
           <Text style = {styles.buttonText}>LOGIN</Text>


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

export default Loginform;