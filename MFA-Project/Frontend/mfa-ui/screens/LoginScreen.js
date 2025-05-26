import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { BASE_URL } from '../constants';

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert("Missing Info", "Please enter both username and password.");
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/login`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.status === 200) {
        const sendSMS = await fetch(`${BASE_URL}/send-sms`, {
          method: 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username })
        });

        const smsResponse = await sendSMS.json();

        if (sendSMS.status === 200) {
          Alert.alert("📲 SMS Sent", "Please enter the OTP sent to your phone.");
          navigation.navigate('OTPCodeScreen', { username });
        } else {
          Alert.alert("Error", smsResponse.error || "Failed to send SMS.");
        }

      } else {
        Alert.alert("Login Failed", data.error || "Invalid username or password.");
      }

    } catch (error) {
      Alert.alert("Connection Error", "Could not connect to backend.");
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to MFA</Text>
      <Text style={styles.subtitle}>Secure Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        placeholderTextColor="#999"
        value={username}
        onChangeText={setUsername}
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        placeholderTextColor="#999"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F6FA',
    justifyContent: 'flex-start',
    paddingHorizontal: 30,
    paddingTop: 100 
  },
  title: {
    fontSize: 28,
    fontWeight: '600',
    textAlign: 'center',
    color: '#2C3A59',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#8395A7',
    textAlign: 'center',
    marginBottom: 40,
  },
  input: {
    height: 50,
    borderColor: '#dfe4ea',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 15,
    backgroundColor: '#fff',
    marginBottom: 15,
    fontSize: 16,
    color: '#2f3542'
  },
  button: {
    backgroundColor: '#4D73F8',
    paddingVertical: 14,
    borderRadius: 10,
    marginTop: 10
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center'
  }
});
