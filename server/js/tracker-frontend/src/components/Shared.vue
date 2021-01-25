<template>
    <div class="container">
        <AjaxForm inline-template v-on:process="share_device" :additional_data="my_devices">
            <div class="container">
                <div class="alert alert-success" v-if="success"  role="alert">
                    Success!                
                </div>
                <div class="alert alert-danger" v-else-if="failed" role="alert">
                    Failed :(
                </div>
            <form  id="share_device_form" class="needs-validation" @submit.prevent="processForm" novalidate>
                <div class="mb-3 position-relative">
                    <label for="device_for_sharing" class="form-label">Device for sharing</label>
                    <select :class="(errors['name']) ? 'form-select is-invalid': 'form-select is-valid'" aria-label="Available devices" name="device_id" id="device_for_sharing" v-model.trim="requestFields['device_id']" >
                        <option v-for="item in additional_data" :value="item.id" :key="item.imei">{{item.name}}</option>
                    </select>
                    <div class="invalid-tooltip" v-if="errors['device_id']">{{errors['device_id']}}</div>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Get sharing link</button>
                </div>
            </form> 
            </div>
        </AjaxForm>
    <hr>
    <div class="container-fluid mt-3" id="friends_requests">
        <div class="card">
            <div class="card-header">
                <div class="container-fluid">
                    Shared devices and requests
                </div>
            </div>
                <div class="card-body">
                        <div class="row row-cols-3 mt-3" v-for="item in shared_devices" :key="item.imei">
                        <div class="col justify-content-start">{{item.device_name}}</div>
                        <div class="col justify-content-start">{{item.owner}}</div>
                        <div class="col justify-content-end">
                            <button type="button" class="btn btn-danger"  v-on:click="unshare(item)">Remove</button>
                        </div>
                    </div>
                </div>
        </div> 
    </div>
</div>
</template>

<script>
    import AjaxForm from './AjaxForm.vue';
    import {API} from '../models';

    export default {
        props: ['devices', 'shared_devices'],
        components: {AjaxForm},
        methods: {
            sendlink(link) {
                navigator.share({
                    title: 'WebShare API Demo',
                    text: 'Track my device here',
                    url: link,
                    },
                    {
                        copy: true,
                        email: true,
                        messenger: true,
                        facebook: true,
                        whatsapp: true,
                        telegram: true,
                        skype: true,
                        language: 'ru' // specify the default language
                    }
                    ).then(() => {
                        console.log('Thanks for sharing!');
                    })
                    .catch( (e) => alert(e));
                    return false;
            }, 
            unshare(item) {
                API.unshareDevice({'id':item.id})
                    .then( () => { this.$emit('value_updated', {'event': 'unshare_device'})})
                    .catch( () => {} ); 
            },
            share_device(data, ok, fail) { 
                API.getSharingLink({},data)
                    .then( (response) => { 
                        ok(response.data);
                        this.sendlink(response.data.link); 
                    })
                    .catch( (err) => {
                        fail(err.response.data);
                    });
            },
        },
        computed: {
            my_devices: function () {
                return this.devices.filter(function (device) {
                    return device.is_shareable;
                })
            },
        },
    }
</script>