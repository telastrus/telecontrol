<template>
    <div id="axis">
        <b-radio-button v-model="state"
            native-value="forward">
            ↑
        </b-radio-button>
        <b-radio-button v-model="state"
            native-value="stop">
            o
        </b-radio-button>
        <b-radio-button v-model="state"
            native-value="back">
            ↓
        </b-radio-button>
    </div>
</template>
<script>
export default {
    name: 'axis',
    props: [
        "index",
        "status",
    ],
    data () {
        return {
            state: "stop"
        }
    }
}
</script>