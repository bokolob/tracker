

import * as L from 'leaflet';

(function(){
L.Control.Calendar = L.Control.extend({
    onAdd: function() {
        var button = L.DomUtil.create('img');
        button.setAttribute('id', 'compass_div');
        button.setAttribute('src', '/static/arrow.jpg');
        button.setAttribute('height', 60);
        button.setAttribute('width', 30);


        L.DomEvent.addListener(button, 'dblclick', L.DomEvent.stop);
        L.DomEvent.addListener(button, 'mousedown', L.DomEvent.stop);
        L.DomEvent.addListener(button, 'mouseup', L.DomEvent.stop);

        return button;
    },

    onRemove: function() {
        // Nothing to do here
    }
});

L.control.calendar = function(opts) {
    return new L.Control.Calendar(opts);
}

})()
