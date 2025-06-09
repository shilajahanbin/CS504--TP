import React from 'react';
import { View, Image, StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export default function SuccessScreen() {
  return (
    <View style={styles.container}>
      <Image
        source={require('../assets/Success.png')}
        style={styles.fullscreenImage}
        resizeMode="cover"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  fullscreenImage: {
    width: width,
    height: height,
  },
});
