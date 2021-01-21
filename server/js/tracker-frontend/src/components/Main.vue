<template>
    <div style="height:100%">
        <div v-if="loading">
        <SplashScreen v-on:csrf_loaded="init_app"></SplashScreen>
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
                <a class="nav-link"  href="#settings_page_container" role="button" aria-expanded="false" aria-controls="settings_page_container" @click="open_settings('DevicesList')">Devices</a>
              </li>
              <li class="nav-item">
                <a class="nav-link"  href="#settings_page_container" role="button" aria-expanded="false" aria-controls="settings_page_container" @click="open_settings('AddDevice')">Add device</a>
              </li>
              <li class="nav-item">
                <a class="nav-link"  href="#settings_page_container" role="button" aria-expanded="false" aria-controls="settings_page_container" @click="open_settings('Shared')">Shared devices</a> 
              </li>
              <li class="nav-item">
                <a class="nav-link"  href="#settings_page_container" role="button" aria-expanded="false" aria-controls="settings_page_container">Profile</a> 
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/logout" role="button">Logout</a>
              </li>
            </ul>
          </div>
        </div>
    </nav>
      <div class="collapse settings_page" id="settings_page_container">
        <div class="card container overflow-auto h-100" v-bind:style="{ height: map_height }">
            <div class="card-header">
                <div class="container-fluid">
                <span class="text-start">
                    Trackers list
                </span>
                <span class="text-end">
                <button type="button" class="btn-close" aria-label="Close"  aria-expanded="false" @click="close_settings()" ></button>
                </span>
                </div>
            </div>
            <div class="card-body">
                <component :is="currentSettingsComponent" v-bind="currentSettingsProperties" v-on:value_updated="update_settings">></component>
            </div>    
        </div>
     </div>
</header>
    <div id="map_container" class="map_container" v-bind:style="{ height: map_height }">
        <div id="mapid"></div>
    </div>
</div>
</template>

<script>
import SplashScreen from './SplashScreen.vue'
import DevicesList from './DevicesList.vue'
import Shared from './Shared.vue'
import AddDevice from './AddDevice.vue'

import { Coordinates, Tracker, TrackersBounds } from '../coordinates';
import {API} from '../models';
import Vue from 'vue';

import { Collapse } from 'bootstrap'

export default {
  name: 'Main',
  props: {},
  components: {DevicesList,Shared,AddDevice,SplashScreen},
  data() {
      return {
        settings_collapse: null,  
        map: null,
        tracker_bounds: null, 
        trackerObjects: {},
        loading: true,  
        devices: [],
        devices_settings: {},
        shared_devices: [],
        currentSettingsComponent: "DevicesList",
        map_height:"calc(100vh-51px)",
      }
  },
  created() {
    window.addEventListener("resize", this.resize_handler);
  },
  mounted() {
      this.settings_collapse = new Collapse(document.getElementById('settings_page_container'), {toggle:false});
      this.resize_handler(); 

      document.getElementById('settings_page_container').addEventListener('shown.bs.collapse', (e) => {
             let navbar_height = document.getElementById('navbar').offsetHeight;
             e.target.style.height= (window.innerHeight - navbar_height)+"px";
      }, false);

      API.getCSRF()
      .then((response) => {
         API.csrf=response.data.csrf;
         this.init_app();
      })
      .catch( (error) => {
         if (error.response.status == 403) {
                this.$emit('need_signup');
         }
         //thisCopy.$emit('csrf_failed', error)
      });
  },
  methods: {
        open_settings(component) {
            this.currentSettingsComponent = component;

            let element = document.getElementById('settings_page_container'); 
            let navbar_height = document.getElementById('navbar').offsetHeight;
            element.style.height=(window.innerHeight - navbar_height)+"px";

            this.settings_collapse.show();       
        },
        close_settings() {
           this.settings_collapse.hide();  
        },
        resize_handler() {
            document.body.style.height = window.innerHeight + "px";
            let navbar_height = document.getElementById('navbar').offsetHeight;
            this.map_height= (window.innerHeight - navbar_height)+"px";
        },
        init_app() {
           this.map = new Coordinates('mapid');
           this.tracker_bounds = new TrackersBounds(this.map);  

           setInterval(this.updateFriendsRequests, 10000);

           this.update_devices();
           this.updateFriendsRequests();

           this.loading = false;
        },
        update_settings(event) {
            switch(event.event) {
                case 'device_added':
                    this.update_devices();
                    break;
                case 'state_changed':
                    if (event.state) {
                       this.trackerObjects[event.imei].addToMap();
                    }
                    else {
                       this.trackerObjects[event.imei].removeFromMap();
                    } 
                    break;
                case 'color_changed':
                    this.trackerObjects[event.imei].set_color(event.color);
                    break;
            }

            console.log(event);
        },
        update_devices() {
            let promise = API.getDevicesList();
            promise.then( (response) => this.renderDevices(response.data));
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
        updateFriendsRequests() {
            API.listSharedDevices().then((response) => { this.shared_devices = response.data});
        }
    },
    computed: {
        currentSettingsProperties: function() {
            if (this.currentSettingsComponent === 'DevicesList') {
                return {'devices': this.devices,
                        'devices_settings': this.devices_settings,
                    };
            }
            else if (this.currentSettingsComponent === 'Shared') {
                return {'devices': this.devices, 'shared_devices':this.shared_devices};
            }
            else if (this.currentSettingsComponent === 'AddDevice') {
                return {};
            }
            else {
                throw "Unknown currentSettingsComponent "+ this.currentSettingsComponent;
            }
        },
     },
}
</script>

<style>
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