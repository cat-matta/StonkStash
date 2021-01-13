import { StatusBar } from 'expo-status-bar';
import React, { Component } from 'react';
import { StyleSheet, View, Image,Text } from 'react-native';
import Signupform from './../forms/Signupform';

/** Account creation, allowing a User to access the site's services and other pages. */

class Signup extends Component {
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
          <Signupform navigation = {this.props.navigation}/>
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

export default Signup;