class Coordinates {
    constructor(id) {
        this.init_layers();

        this.mymap = L.map(id, 
            {
                center: [55.750996996, 37.617330864],
                zoom: 14,
                layers: this.baseLayers['OSM']
            }
        );

        //.setView([55.750996996, 37.617330864], 13);

        L.control.layers(this.baseLayers, {}).addTo(this.mymap);

        this.currentPosition = L.latLng(55.750996996, 37.617330864);
        this.follow=false;
        this.marker = new L.Marker(this.currentPosition);
        this.firstLoad = true;
        this.segments = [];
        this.last_ts = Math.round(new Date().getTime()/1000) - 48*3600;
        
        this.date_from = null;
        this.date_to = null;

        this.marker.addTo(this.mymap).bindPopup("<div> <div> <div>Hello</div> </div> <div><div>World</div></div>  </div>").openPopup();

        //<div style="position: relative;width: 100%;height: 100px;border: 1px solid black;margin: 0;"> <div style="position: absolute;top: 0; right:0"> <div>Hello</div> </div> <div style="height:30px; position: absolute;bottom: 0;"><div>World</div></div>  </div>
       
        //let status = "<div class='container'> <div class='row justify-content-end'> <div class='col'> <span class='battery-warn fa fa-battery-quarter'>jjkj</span></div></div><div class='row justify-content-end'> <div class='col my-3'>tracker1</div></div></div></div>";

        this.marker.setPopupContent(status);
                    

        this.init_center_button(); 
        this.init_follow_button();
        this.init_date_picker();

        /*
                function onLocationFound(e) {
                     var radius = e.accuracy;
                     L.circle(e.latlng, radius).addTo(mymap);
                 }

                 //mymap.on('locationfound', onLocationFound);
        */

    }

    init_date_picker() {
        this.date_picker = null;
        let cnt=1;

        this.calendarButton = L.easyButton({
                'id':'cal_button',
                position: 'topright',
                states: [ 
                {
                    stateName: 'calndar',        // name the state
                    icon:      'fa fa-clock-o',            // and define its properties
                    title:     'follow tracker',        // like its title
                    onClick: (btn, map) => {
                        cnt++;
                        $('#cal_button').find("span span")[0].innerHTML=""+cnt;

                        if (this.date_picker) {
                            this.date_picker.toggle();
                        }      // and its callback
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
                                                console.log([selectedDates, dateStr, instance]);
                                                if (selectedDates.length == 2) {
                                                    this.date_from=selectedDates[0].getTime()/1000;
                                                    this.date_to=selectedDates[1].getTime()/1000;
                                                }
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
                    onClick: (btn, map) => {       // and its callback
                        this.follow=true;
                        btn.state('dont_follow');    // change state on click!
                    }
                },
                {
                    stateName: 'dont_follow',
                    icon:      'fa fa-chain-broken',
                    title:     'Don\'t follow',
                    onClick: (btn, map)  => {
                        this.follow=false;
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
        L.easyButton('fa fa-crosshairs', (btn, map) => {
            map.panTo(this.currentPosition,13);
        }).addTo( this.mymap );
    }

    updateWaypoints = (imei) => {
        let thisCopy = this;
        $.ajax({
            url: '/'+imei+'/coordinates',
            data: {
                'since': this.date_from ? this.date_from : this.last_ts,
                'until': this.date_to ? this.date_to : null,
            },
            success: function(data) {
                if (data.length > 0) {
                    let p = data.length - 1;
                    let newPosition = L.latLng(data[p]['lat'], data[p]['lng']);
                    thisCopy.last_ts = data[p]['ts']; 

                    if (thisCopy.date_from) {
                        thisCopy.date_from = thisCopy.last_ts;
                    }

                    if (thisCopy.firstLoad || thisCopy.follow) {
                        //mymap.flyTo(newPosition);
                        thisCopy.mymap.panTo(newPosition,13);
                        thisCopy.firstLoad=false;
                    }
                    
                    if (thisCopy.currentPosition != newPosition) {
                        thisCopy.currentPosition = newPosition;
                        thisCopy.marker.setLatLng(newPosition);
                        let l = thisCopy.segments.length; 
                        
                        if (l == 0 ||  thisCopy.segments[l-1].getLatLngs().length >= 100) {
                            let track = L.polyline([], {color: 'red'});
                            thisCopy.mymap.addLayer(track);
                            thisCopy.segments.push(track);
                            l++;
                        }
                    
                        data.forEach(el => thisCopy.segments[l-1].addLatLng(el));
                    }

                    thisCopy.mymap.locate({setView: false, maxZoom: 16});
                }            
            }
        });
    };

}