<template>
    <div>
      <Tracker v-for="item in devices" :key="item.imei" 
                    :imei="item.imei" 
                    :settings="devices_settings[item.imei]" 
                    :map_object="map_object" 
                    :socket="socket" 
                    :map_settings="map_settings"
                    :device_id="item.id"
                    v-on:tracker_added="tracker_added"
                    v-on:tracker_removed="tracker_removed"
                    v-on:tracker_position="tracker_position"
                    />
    </div>
</template>

<script>
import * as L from 'leaflet';
import Tracker from './Tracker.vue';

export default {
    props: ['devices', 'devices_settings', 'socket', 'map_settings', 'map_object'],
    components: {Tracker},
    data() {
        return {
            feature_group: L.featureGroup([])
        }
    },
    methods: {
        emit_bounds() {
            let bounds = this.feature_group.getBounds();
            if (bounds.isValid()) {
                this.$emit('bounds_changed', bounds);
            } 
        },
        tracker_added(tracker) {
            this.feature_group.addLayer(tracker.get_marker());
            this.emit_bounds();
        },
        tracker_removed(tracker) {
            this.feature_group.removeLayer(tracker.get_marker());
            this.emit_bounds();
        },
        tracker_position() {
            this.emit_bounds();
        }
    }
}
</script>
