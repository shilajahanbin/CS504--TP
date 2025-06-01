import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { View, Text, StyleSheet } from 'react-native';

import LoginScreen from './screens/LoginScreen';
import DuoAuthScreen from './screens/DuoAuthScreen';
import OTPCodeScreen from './screens/OTPCodeScreen';
import RegisterScreen from './screens/RegisterScreen'; 

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Register">
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="OTPCodeScreen" component={OTPCodeScreen} />
        <Stack.Screen name="SuccessScreen" component={SuccessScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

function SuccessScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.successText}>🎉 Login Successful!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F6FA',
    justifyContent: 'center',
    alignItems: 'center'
  },
  successText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2ecc71'
  }
});
