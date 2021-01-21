<template>
    <AjaxForm inline-template v-on:process="add_device">
        <form id="add_device_form" class="needs-validation" @submit.prevent="processForm" novalidate>
            <div class="alert alert-success" v-if="success"  role="alert">
                Success!
            </div>
            <div class="alert alert-danger" v-else-if="failed" role="alert">
                Failed :(
            </div>
            <div class="mb-3 position-relative">
                <label for="imeiInput" class="form-label">Imei</label>
                <input type="text" :class="(errors['imei']) ? 'form-control is-invalid': 'form-control is-valid'" id="imeiInput" placeholder="imei" name="imei" v-model.trim="requestFields['imei']" required>
                <div class="invalid-tooltip" v-if="errors['imei']">{{ errors['imei'] }}</div>
            </div>
            <div class="mb-3 position-relative">
                <label for="nameInput" class="form-label">Name</label>
                <input type="text" :class="(errors['name']) ? 'form-control is-invalid': 'form-control is-valid'"  id="nameInput" placeholder="name" name="name" v-model.trim="requestFields['name']" required>
                <div class="invalid-tooltip" v-if="errors['name']">{{ errors['name'] }}</div>
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Add device</button>
            </div>
        </form>
    </AjaxForm>
</template>

<script>
    import AjaxForm from './AjaxForm.vue'
    import {API} from '../models';

    export default {
        props: [],
        components: {AjaxForm},
        methods: {
            add_device: function(data, ok, fail) {
                API.addNewDevice({}, data)
                    .then( (response) => { 
                        ok(response.data); 
                        this.$emit('value_updated', {'event': 'device_added'}) 
                     })
                    .catch( (err) => { 
                        fail(err.response.data);
                         console.log(err); 
                        } );
            }
        }
    }
</script>