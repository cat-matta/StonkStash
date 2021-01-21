import { StatusBar } from 'expo-status-bar';
import React, { Component } from 'react';
import { StyleSheet, View, Image,Text } from 'react-native';
import Signupform from './../forms/Signupform';

/** Account creation, allowing a User to access the site's services and other pages. 
 * @pre  The app has loaded correctly and the backend is able to recieve routing requests.
 * @post  If the details provided by the user are valid, they will be transported to the Login page
 * @return  The JSX necessary to render the signup page.
*/
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
          <Signupform navigation = {this.props.navigation /* All the input action happens in the form component */}/> 
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