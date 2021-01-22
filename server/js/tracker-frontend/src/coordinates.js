import * as L from 'leaflet';
require('leaflet-easybutton')
require('./calendar');
import flatpickr from "flatpickr";
const axios = require('axios');

/* Polyfill indexOf. */
var indexOf;

if (typeof Array.prototype.indexOf === 'function') {
    indexOf = function (haystack, needle) {
        return haystack.indexOf(needle);
    };
} else {
    indexOf = function (haystack, needle) {
        var i = 0, length = haystack.length, idx = -1, found = false;

        while (i < length && !found) {
            if (haystack[i] === needle) {
                idx = i;
                found = true;
            }

            i++;
        }

        return idx;
    };
}

class EventEmitter {
    constructor() {
        this.events = {};
    }

    on = (event, listener) => {
        if (typeof this.events[event] !== 'object') {
            this.events[event] = [];
        }
    
        this.events[event].push(listener);
    };
    
    removeListener =  (event, listener) => {
        let idx;
    
        if (typeof this.events[event] === 'object') {
            idx = indexOf(this.events[event], listener);
    
            if (idx > -1) {
                this.events[event].splice(idx, 1);
            }
        }
    };
    
    emit =  (event, args) => {
        if (typeof this.events[event] === 'object') {
            let listeners = this.events[event].slice();
            let length = listeners.length;
    
            for (let i = 0; i < length; i++) {
                listeners[i].apply(this, args);
            }
        }
    };

    once =  (event, listener) => {
        this.on(event, function g () {
            this.removeListener(event, g);
            listener.apply(this, arguments);
        });
    };

}

export class Coordinates extends EventEmitter {

    onLocationFound = (e) => {
        // var radius = e.accuracy;
        this.my_position=e.latlng;

        L.circle(e.latlng, 10).addTo(this.mymap);
        this.emit('location_found', e);
    }

    constructor(id) {
        super();
        this.init_layers();

        this.mymap = L.map(id, 
            {
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

        this.mymap.on('locationfound', this.onLocationFound);
        this.mymap.locate({setView: false, maxZoom: 16});
    }

    init_date_picker() {
        this.date_picker = null;
        //let cnt=1;

        this.calendarButton = L.easyButton({
                'id':'cal_button',
                position: 'topright',
                states: [ 
                {
                    stateName: 'calndar',        // name the state
                    icon:      'fa fa-clock-o',            // and define its properties
                    title:     'follow tracker',        // like its title
                    onClick: () => {
                        //cnt++;
                        // $('#cal_button').find("span span")[0].innerHTML=""+cnt;

                        if (this.date_picker) {
                            this.date_picker.toggle();
                        }
                    }
                },
            ]
        }).addTo(this.mymap);

        this.date_picker = flatpickr("#cal_button",
                                     {disableMobile: "true",  mode: "range", 
                                         maxDate: "today",
                                          enableTime: true, 
                                          time_24hr: true, 
                                          clickOpens:false,
                                          onClose: (selectedDates, dateStr, instance) => {
                                                this.emit('dates_selected', [selectedDates, dateStr, instance]);
                                          },
                                     }); 
    }

    init_follow_button() {
        L.easyButton({
            states: [ 
            {
                    stateName: 'follow_tracker',        // name the state
                    icon:      'fa fa-link',            // and define its properties
                    title:     'follow tracker',        // like its title
                    onClick: (btn) => {       // and its callback
                        this.emit('follow_button_pressed', [true]);
                        btn.state('dont_follow');    // change state on click!
                    }
                },
                {
                    stateName: 'dont_follow',
                    icon:      'fa fa-chain-broken',
                    title:     'Don\'t follow',
                    onClick: (btn)  => {
                        this.emit('follow_button_pressed', [false]);
                        btn.state('follow_tracker');
                    }
            },
        ]
        }).addTo(this.mymap);
    }

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

    }

    init_center_button() {
        L.easyButton('fa fa-crosshairs', () => {
            this.emit('center_button_pressed', []);
        }).addTo( this.mymap );
    }

    init_trail_button() {
        L.easyButton('fa fa-arrow-up', () => {
            this.emit('trail_mode', [false]);
        }).addTo( this.mymap );
    }

}

export class Compass {
    toRadians (angle) {
        return angle * (Math.PI / 180);
    }

    toDegrees(angle) {
        return (angle*180/Math.PI + 360);
    }

    angleFromCoordinate(lat1, long1, lat2, long2) {
        lat1 = this.toRadians(lat1);
        long1 = this.toRadians(long1);

        lat2 = this.toRadians(lat2);
        long2 = this.toRadians(long2);

        let dLon = (long2 - long1);

        let y = Math.sin(dLon) * Math.cos(lat2);
        let x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1)
                * Math.cos(lat2) * Math.cos(dLon);

        let brng = Math.atan2(y, x);

        brng = this.toDegrees(brng);
        brng = (brng + 360) % 360;
        //brng = 360 - brng; // count degrees counter-clockwise - remove to make clockwise

        return brng;
    }

    updateCompass = (my_position, currentPosition) => {
        if (this.my_position) {
            let bearing = this.angleFromCoordinate(my_position.lat, my_position.lng, currentPosition.lat, currentPosition.lng);
            console.log(bearing);
            // TODO $("#compass_div").css({'transform' : 'rotate('+ (bearing) +'deg)'});
        }
    }
}

export class TrackersBounds extends EventEmitter {
    constructor(mymap) {
        super();
        this.follow = false;
        this.mymap=mymap;
        this.group= L.featureGroup([]);
        mymap.on('follow_button_pressed', this.onFollowButtonPressed);
        mymap.on('center_button_pressed', this.onCenterButtonPressed);
    }

    onFollowButtonPressed = (mode) => {
        this.follow=mode;
    }

    onCenterButtonPressed = () => {
        //map.panTo(this.currentPosition,13);
        this.mymap.mymap.fitBounds(this.getBounds()); 
    }

    addTracker = (tracker) => {
        tracker.on('tracker_added', () => {
            this.group.addLayer(tracker.getMarker());
        });

        tracker.on('tracker_removed', () => {
            this.group.removeLayer(tracker.getMarker());
        }); 
        
        tracker.on('tracker_position', () => {
            if (this.follow) {
                this.mymap.mymap.fitBounds(this.getBounds());
            }

            this.emit('bounds_changed', []);
        });
    };

    getBounds = () => {
        return this.group.getBounds();
    }
}

export class Tracker extends EventEmitter {
    constructor(mymap, imei) {
        super();
        this.mymap = mymap;
        this.imei = imei;
        this.follow_trail = true;
        this.trail_length=1000;
        this.color='red';
        this._init();

        mymap.on('trail_mode', this.onTrailButtonPressed);
        mymap.on('dates_selected', this.onDatesSelected);
    }

    _init() {
        this.currentPosition = L.latLng(55.750996996, 37.617330864);

        this.segments = [];
        this.last_ts =  null;
        
        this.date_from = null;
        this.date_to = null;
    }

    addToMap = () => {
        this._init();

        this.marker = new L.Marker(this.currentPosition);
        this.marker.addTo(this.mymap.mymap).bindPopup("<div> <div> <div>Hello</div> </div> <div><div>World</div></div>  </div>").openPopup();

        //<div style="position: relative;width: 100%;height: 100px;border: 1px solid black;margin: 0;"> <div style="position: absolute;top: 0; right:0"> <div>Hello</div> </div> <div style="height:30px; position: absolute;bottom: 0;"><div>World</div></div>  </div>
       
        let status = "<div class='container'> <div class='row justify-content-end'> <div class='col'> <span class='battery-warn fa fa-battery-quarter'>jjkj</span></div></div><div class='row justify-content-end'> <div class='col my-3'>tracker1</div></div></div></div>";
        this.marker.setPopupContent(status);
        this.timer = setInterval(this.updateWaypoints, 1000);
        this.emit('tracker_added', [ this ]);
    }

    removeFromMap = () => {
        this.clear_segments();
        
        if (this.marker) {
            this.mymap.mymap.removeLayer(this.getMarker());
        }

        if (this.timer) {
            clearInterval(this.timer);
        }

        this.emit('tracker_removed', [ this ]);
    }

    getMarker = () => {
        return this.marker;
    };

    onTrailButtonPressed =  () => {
        if (!this.follow_trail) {
            this.follow_trail = true;
            this.last_ts=null;
            this.date_from = null;
            this.date_to = null; //8640000000000000;
            this.clear_segments();
        }
    } 

    onDatesSelected = (selectedDates, dateStr, instance) => {
        console.log([selectedDates, dateStr, instance]);
        if (selectedDates.length == 2) {
            this.date_from=selectedDates[0].getTime()/1000;
            this.date_to=selectedDates[1].getTime()/1000;
            this.last_ts = null;

            this.follow_trail = false;
            this.clear_segments();
        }
    };

    clear_segments = () => {
        while (this.segments.length > 0) {
            let s = this.segments.shift();
            this.mymap.mymap.removeLayer(s); 
        } 
    }

    set_color = (color) => {
        this.color = color;
        this.segments.forEach( el => el.setStyle({ 'color': this.color }) );
    }

    _handle_new_points = (data, directionCopy) => {
        if (data.length > 0) {
            let p = data.length - 1;

            if (directionCopy == 'desc') {
                data = data.reverse();
            }

            let newPosition = L.latLng(data[p]['lat'], data[p]['lng']);

            if (this.last_ts && data[p]['ts'] <= this.last_ts) {
                return 0; //Stale answer
            }

            this.last_ts = data[p]['ts']; 

            if (this.date_from) {
                this.date_from = this.last_ts;
            }
            
            if (this.currentPosition != newPosition) {
                this.currentPosition = newPosition;
                this.marker.setLatLng(newPosition);
                let l = this.segments.length; 
                
                if (l == 0 ||  this.segments[l-1].getLatLngs().length >= 100) {
                    if (this.follow_trail) {
                        while (this.segments.length*100 > this.trail_length) {
                            let s = this.segments.shift();
                            this.mymap.mymap.removeLayer(s); 
                        }
                    }
                    
                    //TODO connect segments

                    let track = L.polyline([], {color: this.color});
                    this.mymap.mymap.addLayer(track);
                    this.segments.push(track);
                    l = this.segments.length;
                }
                
                this.emit('tracker_position', [ this.imei, newPosition, this ]);
                data.forEach(el => this.segments[l-1].addLatLng(el));
            }

            //TODO update position
            //this.mymap.locate({setView: false, maxZoom: 16}); 
            return data.length;
        }
    }

    updateWaypoints = () => {
        let directionCopy = this.follow_trail ? 'desc' : 'asc'; 

        let thisCopy = this;

        axios.get('/'+this.imei+'/coordinates',{
            params: {
                'since': this.date_from ? this.date_from : this.last_ts,
                'until': this.date_to ? this.date_to : null,
                'direction': directionCopy, 
            }
        })
        .then(function (response) {
            console.log(response);
            thisCopy._handle_new_points(response.data, directionCopy);
        })
        .catch(function (error) {
            console.log(error);
        });
    }

}