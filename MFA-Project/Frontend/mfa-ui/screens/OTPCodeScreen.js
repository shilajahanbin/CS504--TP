import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert, StyleSheet, KeyboardAvoidingView, Platform } from 'react-native';
import { BASE_URL } from '../constants';

export default function OTPCodeScreen({ route, navigation }) {
  const { username } = route.params;
  const [code, setCode] = useState('');

  const handleVerifyCode = async () => {
    if (!code) {
      Alert.alert("Missing Code", "Please enter the code you received via SMS.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/verify-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, code })
      });

      const data = await response.json();

      if (response.status === 200) {
        navigation.replace('SuccessScreen');
      } else {
        Alert.alert("Invalid Code", data.error || "Verification failed.");
      }

    } catch (error) {
      Alert.alert("Connection Error", "Could not verify code.");
      console.log(error);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <Text style={styles.title}>Enter the code from Duo Mobile</Text>

      <TextInput
        style={styles.input}
        placeholder="Enter the code"
        placeholderTextColor="#999"
        keyboardType="numeric"
        value={code}
        onChangeText={setCode}
        maxLength={10} 
      />

      <TouchableOpacity style={styles.button} onPress={handleVerifyCode}>
        <Text style={styles.buttonText}>Verify</Text>
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F6FA',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 30
  },
  title: {
    fontSize: 20,
    fontWeight: '600',
    color: '#2C3A59',
    marginBottom: 30,
    textAlign: 'center'
  },
  input: {
    width: '100%',
    height: 50,
    borderColor: '#dfe4ea',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 15,
    backgroundColor: '#fff',
    marginBottom: 20,
    fontSize: 18,
    color: '#2f3542',
    textAlign: 'center'
  },
  button: {
    backgroundColor: '#4D73F8',
    paddingVertical: 14,
    paddingHorizontal: 40,
    borderRadius: 10
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center'
  }
});
