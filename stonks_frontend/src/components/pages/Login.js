import { StatusBar } from 'expo-status-bar';
import React, { Component } from 'react';
import { StyleSheet, View, Image,Text } from 'react-native';
import Loginform from './../forms/Loginform';

/** The Login page, allowing the User access to the main site and it's services.
 * @pre  The backend is online and ready to recieve routing requests from the front end
 * @post  Just renders the login page. All action occurs in the Loginform component
 * @return  The JSX required to render the login screen.
 */
class Login extends Component {
  render() {
    return (
      <View styles = {styles.container}>
        <View style = {styles.logoContainer}>
          <Image 
          style = {styles.logo}
          source ={require('../../images/icon.png')}
          />
          <Text style = {styles.title}>Welcome to StonkStache</Text>


        </View>

        <View styles = {styles.formContainer}>
          <Loginform/>
        </View>
       
      </View>//styles container
      
     
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent:'center'
  },

  logoContainer:{
    flexGrow:1000,
    alignItems: 'center', 
    justifyContent: 'center',
  },

  logo:{
    width: 100, 
    height: 100
  }

  
});

export default Login;