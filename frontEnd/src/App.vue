<template>
  <div id="app">

        <menuBar :changer=menuChanger :mypage="this.page" />
        <div class="desktop">
          <homePage v-if="page=='home'" />
          <playlist v-if="page=='playlist'"/>
          <scenes v-if="page=='scenes'"/>
          <segments v-if="page=='segments'"/>
          <fileupload v-if="page=='fileupload'"/>
<!--        <img class="logo" alt="pinboard logo" src="./assets/pinboardLogo.png"> -->
        </div>
  </div>
</template>

<script>
//import axios from 'axios'
//import VueAxios from 'vue-axios'
import menuBar from './components/menuBar.vue'
import homePage from './components/homePage.vue'
import playlist from './components/playlist.vue'
import scenes from './components/scenes.vue'
import segments from './components/segments.vue'
import fileupload from './components/fileupload.vue'
export default {
  name: 'app',
  data:  function () {
    return {
    page:"home"
  }
  },
  components: {
    menuBar,
    homePage,
    playlist,
    scenes,
    segments,
    fileupload,

  },
    methods: {
    menuChanger: function(name){
      this.page = name;
    }
  }

}
</script>

<style>
@font-face {
  font-family: 'PrintChar21';
  src: url('./assets/PrintChar21.ttf');
      font-smooth: never;
    -webkit-font-smoothing: none;
}
@font-face {
  font-family: 'Shaston320';
  src: url('./assets/Shaston320.ttf');
      font-smooth: never;
    -webkit-font-smoothing: none;
}
@font-face {
  font-family: '16segments';
  src: url('./assets/led16sgmnt-Regular.ttf');
  font-smooth: never;
  -webkit-font-smoothing: none;
}

body{
  margin: 0;
  padding: 0;
      font-smooth: never;
    -webkit-font-smoothing: none;
}
h3{
  font-family:PrintChar21;
  font-size:16px;
      font-smooth: never;
    -webkit-font-smoothing: none;
}
.desktop{
  min-height: 94vh;
}
.logo{
    background-color: #eff9e7;
    padding: 10px;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  background-color: #eff9e7;
  background-image: url('./assets/bgsmall.gif');
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #000;
  margin:  0;
  padding: 0;
}
.btt,
.btt2 {
  font-family: 'PrintChar21';
  font-smooth: never;
  -webkit-font-smoothing: none;
  border: unset;
  border-radius: unset;
  padding-bottom: 30px;
  height: 30px;
  margin-left: 10px;
  background-color: black;

}

.btt2 {
  width: 10%;
  height: 30px;

  margin: 0;
  background-color: black;
}

</style>
