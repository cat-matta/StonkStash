import { StatusBar } from 'expo-status-bar';
import React, { Component } from 'react';
import { StyleSheet, View, Image, Text, Button } from 'react-native';

/** The first page, before a user logs in to the site. 
 * @pre  The app has loaded successfully
 * @post The landing screen elements will be displayed to the user
 * @return  The JSX required to render the landing screen and connect to the authentication pages
*/
class Landing extends Component {
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

        <View styles = {styles.buttonContainer}>
          { /* Put buttons here */ }
          <Button
            styles = {styles.buttonText}
            onPress={ () => this.props.navigation.navigate('Signup')}
            title="Signup"
            accessibilityLabel="Signup Button"
            />
          <Button
            styles = {styles.buttonText}
            onPress={ () => this.props.navigation.navigate('Login')}
            title="Login"
            accessibilityLabel="Login Button"
            />


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

export default Landing;