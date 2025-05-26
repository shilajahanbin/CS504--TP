import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Alert } from 'react-native';
import { BASE_URL } from '../constants';

export default function DuoAuthScreen({ route, navigation }) {
  const { username } = route.params;
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sendDuoAuth = async () => {
      try {
        const response = await fetch(`${BASE_URL}/duo-auth`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username })
        });

        const data = await response.json();

        if (response.status === 200 && data.message === '✅ Duo push approved') {
          navigation.replace('SuccessScreen');
        } else {
          Alert.alert("MFA Failed", data.error || "Duo authentication failed.");
          navigation.navigate('Login');
        }
      } catch (error) {
        Alert.alert("Connection Error", "Failed to reach MFA server.");
        navigation.navigate('Login');
      } finally {
        setLoading(false);
      }
    };

    sendDuoAuth();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Verifying MFA with Duo...</Text>
      {loading && <ActivityIndicator size="large" color="#4D73F8" />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F6FA',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20
  },
  text: {
    fontSize: 18,
    color: '#2C3A59',
    marginBottom: 20,
    textAlign: 'center'
  }
});
