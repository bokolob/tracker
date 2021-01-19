<template>
<div>
    <h2 class="accordion-header" :id="'heading_' + device.imei">
        <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse_'+ device.imei" aria-expanded="true" :aria-controls="'collapse_' + device.imei">
            {{device.name}}
        </button>
    </h2>
    <div :id="'collapse_' + device.imei" class="accordion-collapse collapse" :aria-labelledby="'heading_' + device.imei" data-bs-parent="#tracker_list">
        <div class="accordion-body">
            <div class="container-fluid">
                <div class="row row-cols-2 mt-3"> 
                    <div class="col justify-content-start"> 
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" :id="device.imei + '_enabled'" v-model="settings.enabled">
                        </div>
                    </div>
                    <div class="col justify-content-start">  
                            <label class="form-check-label" :for="device.imei + '_enabled'">Show on map</label>
                    </div>
                </div>
                
                <div class="row row-cols-2 mt-3">  
                    <div class="col justify-content-start"> 
                        <div class="form-check">
                            <input type="color" class="form-control form-control-color" :id="device.imei+'_color'" v-model="settings.color">
                        </div>
                    </div>
                    <div class="col justify-content-start">
                            <label class="form-check-label" :for="device.imei+'_color'">Color</label>
                    </div>
                </div>
                <div class="row mt-3 justify-content-end"> 
                    <div class="col-md-auto"> 
                        <button type="button" class="btn btn-danger btn-sm">Remove</button>
                    </div>
                </div>
                <div class="row mt-3 justify-content-end"> 
                    <div class="col-md-auto">
                        <a class="btn btn-secondary btn-sm" data-bs-toggle="collapse" :href="'#_'+device.imei+'_settings'" role="button" aria-expanded="false" :aria-controls="'_'+device.imei+'_settings'">
                            Settings
                            </a>
                    </div>
                    <div class="collapse mt-4" :id="'_'+device.imei+'_settings'">
                        <div class="card card-body">
                            <div class="container-fluid">
                                <div class="row row-cols-2 mt-1" v-for="setting in current_device_settings" :key="setting.name">
                                    <div class="col col-sm-4">{{setting.key}}</div>
                                    <div class="col col-sm">
                                            <input type="text" :class="'form-control'" v-model.trim.lazy="setting.value" required>
                                    </div>
                                </div>
                                <div class="row mt-3 justify-content-end"> 
                                    <div class="col-md-auto"> 
                                        <button type="button" class="btn btn-primary btn-sm" v-on:click="save">Save</button>
                                    </div>
                                    <div class="col-md-auto"> 
                                        <button type="button" class="btn btn-danger btn-sm" v-on:click="cancel">Cancel</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        </div>
                </div> 
            </div>
        </div>
    </div>
</div>
</template>

<script>
function clone(obj) {
    return JSON.parse(JSON.stringify(obj));
}


export default {
     name: "DeviceItem",
     props: ["device", "settings", "device_settings_model"],
                data() {
                    return { current_device_settings: clone(this.device.settings) }
                },
                methods: {
                    cancel() {
                        this.current_device_settings = clone(this.device.settings)
                    },
                    save() {
                        this.device_settings_model.save(this.device.imei, this.current_device_settings); 
                    }
                },
                watch: {
                    'settings.enabled': {
                        handler: function(newValue) {
                            this.$emit('state_changed', this.device.imei, newValue);
                        },
                        immediate: true,
                    },
                    'settings.color': {
                        handler: function(newValue) {
                            this.$emit('color_changed', this.device.imei, newValue);
                        },
                        immediate: true,
                    },
                }
}
</script>