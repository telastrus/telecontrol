<template>
  <div id="app">
    <h1>Telescope controller</h1>
    <b-button type="is-info" @click="auth" style="margin-bottom: 2em;">Authenticate</b-button>
    <section class="settings">
      <b-field label="Speed"><b-numberinput v-model="speed" min="0" max="255" /></b-field>
      <b-field label="Duration"><b-numberinput v-model="duration" step="0.01" min="0.01" /></b-field>
    </section>
    <div ref="panelbox" class="gridbox">
      <action text="⤿" target="ycw" style="grid-column: 1; grid-row: 2" />
      <action text="⤾" target="yccw" style="grid-column: 3; grid-row: 2" />
      <action text="⤸" target="xcw" style="grid-column: 2; grid-row: 1" />
      <action text="⤹" target="xccw" style="grid-column: 2; grid-row: 3" />

      <action text="▲" target="zf"  style="grid-column: 1000; grid-row: 1"/>
      <action text="▼" target="zb" style="grid-column: 1000; grid-row: 3" />
    </div>
  </div>
</template>

<script>
//import Axis from './Axis.vue';
import Action from './Action.vue'

export default {
  name: 'app',
  components: {
    Action,
  },
  data () {
    return {
      ok: true,
      loader: null,
      socket: null,
      speed: 128,
      duration: 1.0,
    }
  },
  mounted () {
    this.socket = new WebSocket("ws://localhost:11337");
    let self = this;
    this.socket.onmessage = (ev) => {
      let d = ev.data;
      if (d.startsWith('o')) self.end(true);
      else if (d.startsWith('b')) self.auth();
      else if (d.startsWith('e')) self.end(false);
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
    },
    trigger (msg) {
      this.socket.send("a" + JSON.stringify({
        "action": msg,
        "speed": this.speed,
        "duration": this.duration,
      }))
      this.loader = this.$buefy.loading.open({
        container: this.$refs.panelbox.$el,
      });
    },
    end (ok) {
      if (this.loader != null) this.loader.close();

      self.ok = ok;
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

.settings {
  margin: auto;
  width: 20em;
}

.gridbox {
  display: grid;
  border: dashed 1px;
  width: 16em;
  margin: auto;
  margin-top: 1em;
}
</style>
