import { StatusBar } from 'expo-status-bar';
import React, {Component} from 'react';
import {StyleSheet, Text, TextInput, View, TouchableOpacity } from 'react-native';

export default class Loginform extends Component {
  render(){
    return (
      <View style ={styles.container}>
       <TextInput 
       placeholder= "User"
       placeholderTextColor= '#FFF'
       style ={styles.input}
       />
        <TextInput 
        placeholder= "Password"
        placeholderTextColor='#FFF'
       style ={styles.input}
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
