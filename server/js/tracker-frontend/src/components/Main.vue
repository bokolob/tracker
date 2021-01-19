<template>
    <div>
        <div v-if="loading">
        <SplashScreen v-on:csrf_loaded="csrf_loaded"></SplashScreen>
        </div>
    <header>
    <nav id="navbar" class="navbar navbar-expand-md navbar-dark bg-dark" aria-label="Fourth navbar example">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Expand at md</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample04" aria-controls="navbarsExample04" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
    
          <div class="collapse navbar-collapse" id="navbarsExample04">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
              <li class="nav-item active">
                <a class="nav-link" data-bs-toggle="collapse" href="#nav-trackers-list" role="button" aria-expanded="false" aria-controls="nav-trackers-list">Devices</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-bs-toggle="collapse" href="#nav-add-tracker" role="button" aria-expanded="false" aria-controls="nav-add-tracker">Add device</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" data-bs-toggle="collapse" href="#nav-friends" role="button" aria-expanded="false" aria-controls="nav-friends">Shared devices</a> 
              </li>
              <li class="nav-item">
                <a class="nav-link" data-bs-toggle="collapse" href="#nav-profile" role="button" aria-expanded="false" aria-controls="nav-profile">Profile</a> 
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/logout" role="button">Logout</a>
              </li>
            </ul>
          </div>
        </div>
    </nav>

      <div class="collapse settings_page" id="nav-trackers-list">
        <div class="card container overflow-auto h-100">
            <div class="card-header">
                <div class="container-fluid">
                <span class="text-start">
                    Trackers list
                </span>
                <span class="text-end">
                <button type="button" class="btn-close" aria-label="Close" data-bs-toggle="collapse" href="#nav-trackers-list" aria-expanded="false" aria-controls="#nav-trackers-list" ></button>
                </span>
                </div>
            </div>
            <div class="card-body">
                    <div class="accordion" id="tracker_list">
                        <div class="accordion-item" v-for="item in devices" :key="item.imei">
                            <DeviceItem :device="item" :settings="devices_settings[item.imei]" v-on:state_changed="state_changed" v-on:color_changed="color_changed" :device_settings_model="deviceSettingsModel"></DeviceItem>
                       </div>
                   </div>
            </div>    
        </div>
    </div>
        <div class="collapse settings_page" id="nav-add-tracker" >
            <div class="card container overflow-auto h-100">
                <div class="card-header text-end">
                    <button type="button" class="btn-close" aria-label="Close" data-bs-toggle="collapse" href="#nav-add-tracker" aria-expanded="false" aria-controls="nav-add-tracker" ></button>
                </div>
                <div class="card-body">
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
                </div>
            </div>    
        </div> 
        <div class="collapse settings_page" id="nav-friends" >
            <div class="card container overflow-auto h-100">
                <div class="card-header text-end">
                    <button type="button" class="btn-close" aria-label="Close" data-bs-toggle="collapse" href="#nav-friends" aria-expanded="false" aria-controls="nav-friends" ></button>
                </div>
                <div class="card-body">
                    <div class="container">
                         <AjaxForm inline-template v-on:process="share_device" :arguments="{'my_devices': my_devices}">
                            <form  id="share_device_form" class="needs-validation" @submit.prevent="processForm" novalidate>
                                <div class="alert alert-success" v-if="success"  role="alert">
                                    Success! <a :href="response.link">Sharing link</a>
                                </div>
                                <div class="alert alert-danger" v-else-if="failed" role="alert">
                                    Failed :(
                                </div>
                                <div class="mb-3 position-relative">
                                    <label for="device_for_sharing" class="form-label">Device for sharing</label>
                                    <select :class="(errors['name']) ? 'form-select is-invalid': 'form-select is-valid'" aria-label="Available devices" name="device_id" id="device_for_sharing" v-model.trim="requestFields['device_id']" >
                                        <option v-for="item in arguments.my_devices" :value="item.id" :key="item.name">{{item.name}}</option>
                                    </select>
                                    <div class="invalid-tooltip" v-if="errors['device_id']">{{errors['device_id']}}</div>
                                </div>
                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary">Get sharing link</button>
                                </div>
                            </form> 
                        </AjaxForm>
                    </div>
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
                                            <button type="button" class="btn btn-danger"  v-on:click="removeFromFriends">Remove</button>
                                        </div>
                                    </div>
                               </div>
                        </div> 
                    </div>
                </div>
            </div>    
        </div> 
        <div class="collapse settings_page" id="nav-profile" >
            <div class="card container overflow-auto h-100">
                <div class="card-header text-end">
                    <button type="button" class="btn-close" aria-label="Close" data-bs-toggle="collapse" href="#nav-profile" aria-expanded="false" aria-controls="nav-profile" ></button>
                </div>
                <div class="card-body">
                    <div class="container">
                    </div>
                </div>
            </div>
        </div>
</header>
    <div id="map_container" class="map_container">
        <div id="mapid"></div>
    </div>
</div>
</template>

<script>
import SplashScreen from './SplashScreen.vue'
import DeviceItem from './DeviceItem.vue'
import AjaxForm from './AjaxForm.vue'

import { Coordinates, Tracker, TrackersBounds } from '../coordinates';
import { Devices, DevicesSettings, SharedDevices } from '../models';
import Vue from 'vue';
const axios = require('axios');

export default {
  name: 'Main',
  props: {},
  components: {DeviceItem, SplashScreen, AjaxForm},
  data() {
      return {
        map: null,
        tracker_bounds: null, 
        trackerObjects: {},
        loading: true,  
        devices: [],
        devices_settings: {},
        devicesModel: null,
        friendsModel: null,
        deviceSettingsModel: null,
        shared_devices: []
      }
  },
  created() {
    window.addEventListener("resize", this.resize_handler);
  },
  mounted() {
      this.map = new Coordinates('mapid');
      this.tracker_bounds = new TrackersBounds(this.map); 
      let thisCopy = this;
      
      axios.get('/csrf')
            .then(function (response) {
                // handle success
                console.log(response);
                thisCopy.csrf_loaded(response.data.csrf);
                //thisCopy.$emit('csrf_loaded', response.data.csrf)
            })
            .catch(function (error) {
                // handle error
                console.log(error);
                
                if (error.response.status == 403) {
                    thisCopy.$emit('need_signup');
                    //route_to_login_page
                }
                //thisCopy.$emit('csrf_failed', error)
            });
  },
  methods: {
        removeFromFriends: function() {alert("xxx")},
        add_device: function(data) { this.devicesModel.add(data) },
        share_device: function(data) {this.friendsModel.add(data)},
        resize_handler() {
            document.body.style.height = window.innerHeight + "px"; 
        },
        csrf_loaded(csrf) {
           axios.defaults.headers.common["X-CSRFToken"] = csrf;
           this.devicesModel = new Devices(this.renderDevices);
           this.friendsModel = new SharedDevices(this.updateFriendsRequests);
           this.deviceSettingsModel = new DevicesSettings();

           setInterval(this.friendsModel.list, 10000);
           this.devicesModel.reload();
           this.friendsModel.list(); 

           this.loading = false;
        },
        state_changed(imei, newValue) {
            if (newValue) {
                this.trackerObjects[imei].addToMap();
            }
            else {
                this.trackerObjects[imei].removeFromMap();
            }
        },
        color_changed(imei, newValue) {
            this.trackerObjects[imei].set_color(newValue);
        },
        renderDevices(data) {
            console.log(data);

            for (let i in data) {
                let device = data[i];
            
                if (!this.trackerObjects[device.imei]) {
                    this.trackerObjects[device.imei] = new Tracker(this.map, device.imei);
                    this.tracker_bounds.addTracker(this.trackerObjects[device.imei]);
                }   

                Vue.set(this.devices_settings, device.imei, {'enabled': false, 'color':'#ff0000'});
            }

            this.devices = data;
        },
        updateFriendsRequests(data) {
            this.shared_devices = data;
        }
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

<style>
    #map_container {
        height: calc(100% - 51px); 
    }

    #mapid {
        height: 100%;
        width: 100%;
    }
    
    .map_container {
        height: calc(100% - 51px); 
    }

    #mapid {
        height: 100%;
        width: 100%;
    }   
    
    header.navbar {
        margin-bottom: 0px;
    }

    .settings_page {
        position: absolute;
        width: 100%;
        background: transparent;
        z-index: 2000;
    }

    .calendar-button {
        margin-left:auto;
        margin-right: auto;
        margin: 5px;
    }

    .flatpickr-calendar {
        z-index: 4000;
    }
    
</style>