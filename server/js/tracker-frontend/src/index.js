import Vue from 'vue';
import { Coordinates, Tracker, TrackersBounds } from './coordinates';
import { Devices, DevicesSettings, User, UserSettings, SharedDevices } from './models';
import $ from "jquery";

require('leaflet-easybutton')
require('flatpickr');

function main(){
    let map = new Coordinates('mapid');
    let tracker_bounds = new TrackersBounds(map);
    let trackerObjects = {};

    let vue_data = {
        devices: [],
        devices_settings: {},
        shared_devices: [],
    };

    function renderDevices(data) {
        console.log(data);

        for (let i in data) {
            let device = data[i];
        
            if (!trackerObjects[device.imei]) {
                trackerObjects[device.imei] = new Tracker(map, device.imei);
                tracker_bounds.addTracker(trackerObjects[device.imei]);
            }   

            Vue.set(vue_data.devices_settings, device.imei, {'enabled': false, 'color':'#ff0000'});
        }

        vue_data.devices = data;
        $("#trackers_list_spinner").addClass("d-none");
    }

    function updateFriendsRequests(data) {
        vue_data.shared_devices = data;
    }

    let devicesModel = new Devices("{{ csrf_token() }}", renderDevices, function() {$("#trackers_list_spinner").removeClass("d-none");});
    let friendsModel = new SharedDevices("{{ csrf_token() }}", updateFriendsRequests);
    let deviceSettingsModel = new DevicesSettings("{{ csrf_token() }}");

    function clone(obj) {
        return JSON.parse(JSON.stringify(obj));
    }

    Vue.component('device-item', {
                props: ["device", "settings"],
                data() {
                    return { current_device_settings: clone(this.device.settings) }
                },
                methods: {
                    cancel() {
                        this.current_device_settings = clone(this.device.settings)
                    },
                    save() {
                        deviceSettingsModel.save(this.device.imei, this.current_device_settings,
                            (data) => {
                                
                            },
                            (fail) => {

                            }
                        ); 
                    }
                },
                watch: {
                    'settings.enabled': {
                        handler: function(newValue, oldValue) {
                            if (newValue) {
                                trackerObjects[this.device.imei].addToMap();
                            }
                            else {
                                trackerObjects[this.device.imei].removeFromMap();
                            }
                        },
                        immediate: true,
                    },
                    'settings.color': {
                        handler: function(newValue, oldValue) {
                            trackerObjects[this.device.imei].set_color(newValue);
                        },
                        immediate: true,
                    },
                }
            });


    var vm = new Vue(
            {
                'el': '#app',
                'data':  vue_data,
                'methods': {
                    removeFromFriends: function() {alert("xxx")},
                    add_device: devicesModel.add,
                    share_device: friendsModel.add,
                },
                computed: {
                            my_devices: function () {
                                return this.devices.filter(function (device) {
                                    return device.is_shareable;
                                })
                            },
                        },
            });



    setInterval(friendsModel.list, 10000);

    devicesModel.reload();
    friendsModel.list();

    $('#trackers_list_refresh').on('click', function() { devicesModel.reload() });

    let pages = {};
    $(".settings_page").each( function() { 
        pages[this.id] = new bootstrap.Collapse(this, {toggle: false});
    });

    let navbarCollapse = new bootstrap.Collapse($("#navbarsExample04")[0],{toggle: false}); 

    function onPageShow(event) {
        let target = event.target;
        let id = target.id;
        
        if (!pages[id]) {
            return;
        }

        for (let i in pages) {
            if (id != i) {
                pages[i].hide();
            }
        }

        $('.settings_page').css("height", $("#map_container").height()+"px"); 
    }

    $(".settings_page").on('show.bs.collapse', () => navbarCollapse.hide());
    $(".settings_page").on('hidden.bs.collapse', (e) => pages[e.target.id] && $("#map_container").removeClass("d-none") );
    $(".settings_page").on('shown.bs.collapse', onPageShow);

    $('.settings_page').bind('click dblclick mouseover mouseout scroll',function(e){ e.stopPropagation();});
    // $('#map_container').css("height","calc(100% - "+($("header").height()-3)+"px)"); 

    $(window).resize(function () {
        document.body.style.height = window.innerHeight + "px"; 
        $('#map_container').css("height","calc(100% - "+$("header").height()+"px)"); 
        $('.settings_page').css("height", $("#map_container").height()+"px"); 
    });

    $(window).resize(); 
}

window.main=main;