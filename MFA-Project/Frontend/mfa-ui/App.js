import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import LoginScreen from './screens/LoginScreen'; 
import { Text, View } from 'react-native'; 

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        
        {}
        <Stack.Screen name="OTPScreen" component={() => (
          <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text>OTP Screen Placeholder</Text>
          </View>
        )} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
