<template>
  <div id="app">
    <h1>Telescope controller</h1>
    <div class="circle-container">
      <b-checkbox-button v-model="chkgrp" native-value="1" class="btn deg30">
        1
      </b-checkbox-button>
      <b-checkbox-button v-model="chkgrp" native-value="2" class="btn deg150">
        2
      </b-checkbox-button>
      <b-checkbox-button v-model="chkgrp" native-value="3" class="btn deg270">
        3
      </b-checkbox-button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'app',
  components: {
  },
  data () {
    return {
      chkgrp: [],
      socket: null,
    }
  },
  mounted () {
    this.socket = new WebSocket("ws://localhost:11337");
  },
  watch: {
    chkgrp (msg) {
      this.socket.send(msg);
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

/* Modified from https://stackoverflow.com/questions/12813573/position-icons-into-circle */
.btn {
  width: 2em;
  height: 2em;
  margin: auto;
  display: block;
  position: absolute;
  top: 50%; left: 50%;
  margin: -1em;
}

.circle-container {
  position: relative;
  width: 24em;
  height: 24em;
  padding: 2.8em;
    /*2.8em = 2em*1.4 (2em = half the width of a link with img, 1.4 = sqrt(2))*/
  border: dashed 1px;
  border-radius: 50%;
  margin: 1.75em auto 0;
}
.deg0 { transform: translate(12em); } /* 12em = half the width of the wrapper */
.deg30 { transform: rotate(30deg) translate(12em) rotate(-30deg); }
.deg150 { transform: rotate(150deg) translate(12em) rotate(-150deg); }
.deg270 { transform: rotate(270deg) translate(12em) rotate(-270deg); }
</style>
