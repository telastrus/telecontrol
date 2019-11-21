<template>
  <div class="cont">
    <b-button type="is-primary" @click="$parent.trigger(target)">{{text}}</b-button>
  </div>
</template>

<script>
export default {
  name: 'action',
  props: [
    "text",
    "target",
  ],
  data () {
    return {

    }
  }
}
</script>

<style>
.cont {
  margin: auto;
}
</style>