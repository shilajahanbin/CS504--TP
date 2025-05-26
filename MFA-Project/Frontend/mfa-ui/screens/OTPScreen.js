import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { BASE_URL } from '../constants';


export default function OTPScreen({ route, navigation }) {
  const { username } = route.params;
  const [otp, setOtp] = useState('');

  const handleVerify = async () => {
    if (!otp) {
      Alert.alert("Missing OTP", "Please enter the OTP.");
      return;
    }

    try {
        const response = await fetch(`${BASE_URL}/verify-otp`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, otp })
      });

      const data = await response.json();

      if (response.status === 200) {
        Alert.alert("✅ Success", "Login verified successfully!");
        navigation.navigate('SuccessScreen');
      } else {
        Alert.alert("❌ Error", data.error || "Verification failed.");
      }

    } catch (error) {
      Alert.alert("Connection Error", "Cannot connect to backend.");
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Enter OTP</Text>
      <TextInput
        placeholder="6-digit code"
        style={styles.input}
        keyboardType="numeric"
        maxLength={6}
        onChangeText={setOtp}
        value={otp}
      />
      <TouchableOpacity style={styles.button} onPress={handleVerify}>
        <Text style={styles.buttonText}>Verify</Text>
      </TouchableOpacity>
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F6FA',
    justifyContent: 'flex-start',
    paddingTop: 100,
    paddingHorizontal: 30,
  },
  title: {
    fontSize: 24,
    marginBottom: 30,
    fontWeight: '600',
    color: '#2C3A59',
    textAlign: 'center'
  },
  input: {
    height: 50,
    borderColor: '#dfe4ea',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 15,
    backgroundColor: '#fff',
    fontSize: 18,
    color: '#2f3542',
    marginBottom: 20
  },
  button: {
    backgroundColor: '#4D73F8',
    paddingVertical: 14,
    borderRadius: 10
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center'
  }
});
