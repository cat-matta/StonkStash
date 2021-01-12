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
                // Once authentication routes are made, submit stuff here.
                // ensure validation of email, password, username, etc and rejection if bad
                // TODO: determine requirements for each field.
                this.props.navigation.navigate('Login');
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