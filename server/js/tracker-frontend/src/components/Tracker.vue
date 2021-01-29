<script>
import * as L from 'leaflet';
const axios = require('axios');

export default {
    props:['imei', 'device_id', 'settings', 'map_settings', 'map_object', 'socket'],

    data() {
        return {
            currentPosition: null,
            segments: [],
            last_ts: null,
            date_from: null,
            date_to: null, 
            color: null,
            mode: null,
            promise: null,
            watchdog: null,
            request_context_id: 1,
        }
    },
    mounted() {
        this.init();
        this.socket.on("coordinates_updated", this.on_event);
        this.socket.on("reconnect", this.on_reconnect);
    },
    beforeDestroy() {
        this.remove_from_map();
        this.socket.off("coordinates_updated", this.on_event);
        this.socket.off("reconnect", this.on_reconnect);
    },
    render() {
         return []
    },
    methods: {
        init() {
            this.currentPosition = L.latLng(55.750996996, 37.617330864);

            this.clear_segments();
            this.last_ts =  null;
            
            this.date_from = null;
            this.date_to = null;

            if (this.promise) {
              //TODO  this.promise.cancel();
            }

            this.request_context_id++;

            if (this.watchdog) {
                clearTimeout(this.watchdog);
            }

            this.socket.emit("unsubscribe_on_device", {imei: this.imei});
        },
        get_marker() {
            return this.marker;
        },
        clear_segments() {
            while (this.segments.length > 0) {
                let s = this.segments.shift();
                this.map_object.removeLayer(s); 
            } 
        },
        set_color(color) {
            this.color = color;
            this.segments.forEach( el => el.setStyle({ 'color': this.color }) );
        },
        add_to_map() {
            this.init();

            this.marker = new L.Marker(this.currentPosition);
            this.marker.addTo(this.map_object).bindPopup("<div> <div> <div>Hello</div> </div> <div><div>World</div></div>  </div>").openPopup();

            //<div style="position: relative;width: 100%;height: 100px;border: 1px solid black;margin: 0;"> <div style="position: absolute;top: 0; right:0"> <div>Hello</div> </div> <div style="height:30px; position: absolute;bottom: 0;"><div>World</div></div>  </div>
        
            let status = "<div class='container'> <div class='row justify-content-end'> <div class='col'> <span class='battery-warn fa fa-battery-quarter'>jjkj</span></div></div><div class='row justify-content-end'> <div class='col my-3'>tracker1</div></div></div></div>";
            this.marker.setPopupContent(status);

            //this.timer = setInterval(this.updateWaypoints, 1000);
            this.$emit('tracker_added', this);
        },
        remove_from_map() {
            this.request_context_id++;
            this.on_map = false;
            this.clear_segments();
            
            if (this.marker) {
                this.map_object.removeLayer(this.get_marker());
            }

            if (this.timer) {
                clearInterval(this.timer);
            }

            this.$emit('tracker_removed',this);
            this.socket.emit("unsubscribe_from_device", {imei: this.imei});
        },
        _handle_new_points(data, directionCopy)  {
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
                                this.map_object.removeLayer(s); 
                            }
                        }
                        
                        //TODO connect segments
                        let track = L.polyline([], {color: this.color});
                        this.map_object.addLayer(track);
                        this.segments.push(track);
                        l = this.segments.length;
                    }
                    
                    this.$emit('tracker_position', this);
                    data.forEach(el => this.segments[l-1].addLatLng(el));
                }

                //TODO update position
                //this.mymap.locate({setView: false, maxZoom: 16}); 
                return data.length;
            }
        },
        updateWaypoints() {
            let directionCopy = this.mode === "follow_trail" ? 'desc' : 'asc'; 
            let context_id = this.request_context_id;
            let thisCopy = this;

            this.promise = axios.get('/'+this.imei+'/coordinates',{
                params: {
                    'since': this.date_from ? this.date_from : this.last_ts,
                    'until': this.date_to ? this.date_to : null,
                    'direction': directionCopy, 
                }
            })
            .then(function (response) {
                console.log(response);

                if (thisCopy.request_context_id != context_id) {
                    console.log("Drop request, it's not needed anymore");
                    return;
                }

                thisCopy._handle_new_points(response.data, directionCopy);

                if (thisCopy.watchdog) {
                    clearTimeout(thisCopy.watchdog);
                }

                if (thisCopy.mode == 'follow_trail') {
                    //Events are unreliable, so set an alarm clock to check
                    thisCopy.watchdog=setTimeout(thisCopy.updateWaypoints, 60000);    
                }
                else if (thisCopy.mode == 'show_full_track') {
                    if (response.data.length > 0) {
                        thisCopy.watchdog=setTimeout(thisCopy.updateWaypoints, 50);
                    }
                }

            })
            .catch(function (error) {
                console.log(error);

                if (thisCopy.request_context_id != context_id) {
                    console.log("Drop error, it's not needed anymore");
                    return;
                }

                thisCopy.watchdog=setTimeout(thisCopy.updateWaypoints, 50);
            });
        },
        choose_mode() {
            if (this.mode == 'follow_trail') {
                this.follow_trail();
            }
            else if (this.mode == 'show_full_track') {
                this.show_track();
            }
        },
        on_reconnect() {
            if (this.mode === "follow_trail") {
              this.socket.emit("subscribe_on_device", {imei: this.imei});
            }
        },
        on_event(ev) {
            if (this.mode === "follow_trail"  && ev.data.id === this.device_id) {
              this.updateWaypoints();  
            }
        },
        show_track() {
            this.init();

            if (!this.map_settings.selectedDates.length) {
                return;
            }

            this.date_from=this.map_settings.selectedDates[0].getTime()/1000;
            this.date_to=this.map_settings.selectedDates[1].getTime()/1000;

            if (this.settings.enabled) {
                this.updateWaypoints();
            }
        },
        follow_trail() {
           this.init();

           if (this.timer) {
               clearInterval(this.timer);
           }
           
           if (this.settings.enabled) {
             this.socket.emit("subscribe_on_device", {imei: this.imei});
             //TODO handle socket error and disconnect
             this.updateWaypoints();
           }
           
        }
    },

    watch: {
        'settings.enabled': {
            handler: function(newValue) {
                if (newValue) {
                    this.add_to_map();
                }
                else {
                    this.remove_from_map();
                }

                this.choose_mode();
            },
            immediate: true,
        },
        'settings.color': {
            handler: function(newValue) {
                this.set_color(newValue);
            },
            immediate: true,
        },
        'map_settings.mode': {
            handler: function(newValue) {
                this.mode=newValue;
                this.choose_mode();
            },
            immediate: true,
        } 
    }


}
</script>

    