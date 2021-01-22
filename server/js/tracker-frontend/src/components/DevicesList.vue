<template>
<div>
    <div class="container">
        <hr/>
        <div class="row">
            <div class="col-md-4">Name</div>
            <div class="col-md-1">Put on map</div>
            <div class="col-md-3">Color</div>
            <div class="col-md-3">Settings</div>
        </div>
        <hr/>
    </div>

    <div class="accordion" id="tracker_list">
        <div class="accordion-item" v-for="item in devices" :key="item.imei">
            <DeviceItem :device="item" :settings="devices_settings[item.imei]" v-on:state_changed="state_changed" v-on:color_changed="color_changed"></DeviceItem>
        </div>
    </div>
    </div>
</template>

<script>
    import DeviceItem from './DeviceItem.vue'

    export default {
        name: 'DevicesList',
        props: ['devices', 'devices_settings'],
        components: {DeviceItem},
        methods: {
            state_changed(imei, newValue) {
                this.$emit('value_updated', {'event': 'state_changed', 'imei': imei, 'state': newValue});
            },
            color_changed(imei, newValue) {
                this.$emit('value_updated', {'event': 'color_changed', 'imei': imei, 'color': newValue});
            },
        }
    }
</script>
