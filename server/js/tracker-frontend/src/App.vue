<template>
  <div id="app">
    <LoginScreen v-if="signup" v-on:authorized="signup=false"/>
    <Main v-else v-on:need_signup="signup=true"/>
  </div>
</template>

<script>
import 'flatpickr/dist/flatpickr.min.css'
import 'leaflet/dist/leaflet.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'leaflet-easybutton/src/easy-button.css'

import Main from './components/Main.vue'
import LoginScreen from './components/LoginScreen.vue'

export default {
  name: 'App',
  data() {
    return  { signup: false }
  },
  components: {
    Main,
    LoginScreen
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  height:100%;
}
</style>
