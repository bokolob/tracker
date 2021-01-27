<template>
    <div id="map_container" class="map_container" v-bind:style="{ height: map_height }">
        <div id="mapid"></div>
        <TrackersContainer 
            :devices_settings="devices_settings"
            :devices="devices"
            :map_settings="settings"  
            :map_object="mymap" 
            :socket="socket" 
            v-on:bounds_changed="on_bounds_changed"
            />
    </div>
</template>

<script>
import * as L from 'leaflet';
require('leaflet-easybutton')
require('../calendar');
import flatpickr from "flatpickr";
import TrackersContainer from './TrackersContainer.vue';

const default_center=L.latLng(55.750996996, 37.617330864);

export default {
    props: ['map_height', 'devices', 'devices_settings', 'socket'],

    data() {
        return {
            settings: {mode:'follow_trail', follow_trackers: true},
            mymap: null, 
            my_position: null,
            view_bounds: null,
        }
    },
    
    mounted() {
        this.init_map();
    },

    components: {TrackersContainer},

    computed: {
        center() {
            if (this.view_bounds && this.view_bounds.isValid()) {
                this.view_bounds.getCenter();
            }
            return default_center;
        }
    },
    methods: {
        on_bounds_changed(bounds) {
            this.view_bounds = bounds;
            if (this.settings.follow_trackers) {
                this.mymap.fitBounds(this.view_bounds); 
            }
        },
        init_map() {
            this.init_layers();

            this.mymap = L.map("mapid", 
                {
                    tap: false,
                    preferCanvas: true,
                    center: [55.750996996, 37.617330864],
                    zoom: 14,
                    layers: this.baseLayers['OSM']
                }
            );

            L.control.layers(this.baseLayers, {}).addTo(this.mymap);

            this.init_center_button(); 
            this.init_follow_button();
            this.init_date_picker();
            this.init_trail_button();

            L.control.calendar({position: 'topright'}).addTo(this.mymap);

            this.mymap.on('locationfound', (e) => this.onLocationFound(e));
            this.mymap.locate({setView: false, maxZoom: 16});
        },
        onLocationFound(e) {
            // var radius = e.accuracy;
            this.my_position=e.latlng;
            L.circle(e.latlng, 10).addTo(this.mymap);
        },    
        init_date_picker() {
            this.date_picker = null;

            L.easyButton({
                    'id':'cal_button',
                    position: 'topright',
                    states: [ 
                    {
                        stateName: 'calndar',        // name the state
                        icon:      'fa fa-clock-o',            // and define its properties
                        title:     'follow tracker',        // like its title
                        onClick:   () => this.date_picker.toggle()
                    },
                ]
            }).addTo(this.mymap);

            this.date_picker = flatpickr("#cal_button",
                                        {disableMobile: "true",  mode: "range", 
                                            maxDate: "today",
                                            enableTime: true, 
                                            time_24hr: true, 
                                            clickOpens:false,
                                            onClose: (selectedDates) => {
                                                    this.settings.mode="none";
                                                    this.settings.selectedDates = selectedDates; 
                                                    this.settings.mode="show_full_track";
                                            },
                                        }); 

        },

        init_follow_button() {
            L.easyButton({
                states: [ 
                {
                        stateName: 'follow_tracker',        // name the state
                        icon:      'fa fa-link',            // and define its properties
                        title:     'follow tracker',        // like its title
                        onClick: (btn) => {       // and its callback
                            this.settings.follow_trackers=true;
                            btn.state('dont_follow');    // change state on click!
                        }
                    },
                    {
                        stateName: 'dont_follow',
                        icon:      'fa fa-chain-broken',
                        title:     'Don\'t follow',
                        onClick: (btn)  => {
                            this.settings.follow_trackers=false;
                            btn.state('follow_tracker');
                        }
                },
            ]
            }).addTo(this.mymap);
        },
        init_layers() {
            this.baseLayers = {
                'OSM': L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                    maxZoom: 18,
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    id: 'mapbox/streets-v11',
                    tileSize: 512,
                    zoomOffset: -1
                }),

                //2gis:
                '2GIS': L.tileLayer('http://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}'),

                //Google Map Streets:
                'GoogleMap': L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {subdomains:['mt0','mt1','mt2','mt3']}),

                //Google Map Terrain:
                'GoogleMapTerrain': L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {subdomains:['mt0','mt1','mt2','mt3']}),

                //Google Map Hybrid:
                'GoogleMapHybrid': L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {subdomains:['mt0','mt1','mt2','mt3']}),

                //Google Map Satellite:
                'GoogleMapSattelite': L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {subdomains:['mt0','mt1','mt2','mt3']}),
            };
        },
        init_center_button() {
            L.easyButton('fa fa-crosshairs', () => {
                if (this.view_bounds) {
                    this.mymap.fitBounds(this.view_bounds); 
                }
            }).addTo( this.mymap );
        },
        init_trail_button() {
            L.easyButton('fa fa-arrow-up', () => {
                this.settings.mode="follow_trail";
                this.settings.selectedDates=[];
            }).addTo( this.mymap );
        }
    
    }
}
</script>


<style scoped>
    .map_container {
        height: calc(100% - 51px); 
    }

    #mapid {
        height: 100%;
        width: 100%;
    }   
</style>