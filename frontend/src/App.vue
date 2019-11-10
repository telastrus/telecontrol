<template>
  <div id="app">
    <h1>Telescope controller</h1>
    <button @Click="auth">Auth</button>
    <div class="circle-container">
      <axis v-bind:index="1" class="btn deg30" />
      <axis v-bind:index="2" class="btn deg150" />
      <axis v-bind:index="3" class="btn deg270" />
    </div>
  </div>
</template>

<script>
import Axis from './Axis.vue';

export default {
  name: 'app',
  components: {
    Axis,
  },
  data () {
    return {
      status: [false, false, false],
      socket: null,
    }
  },
  mounted () {
    this.socket = new WebSocket("ws://localhost:11337");
    let self = this;
    this.socket.onmessage = (ev) => {
      let d = ev.data;
      if (d.startsWith('e')) {
        self.status[Number(d.charAt(1))];
      }
      else if (d.startsWith('b')) self.auth();
    };

    this.auth();
  },
  methods: {
    auth () {
      let self = this;
      this.$buefy.dialog.prompt({
        message: 'Enter password:',
        inputAttrs: {
          type: 'password'
        },
        trapFocus: true,
        onConfirm: (value) => self.socket.send('p' + value)
      })
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
