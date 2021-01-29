<script>
export default {
    props:['target_coords', 'phone_coords'],

    watch: {
        'target_coords': {
            handler() {this.update_coords() },
            immediate: true,
        },
        'phone_coords': {
            handler() {this.update_coords() },
            immediate: true,
        }
    },

    methods: {
        update_coords() {
            if (!this.phone_coords || !this.target_coords) {
                return;   
            }
            
            let bearing = this.angleFromCoordinate(this.phone_coords.lat, this.phone_coords.lng, this.target_coords.lat, this.target_coords.lng);
            this.$emit('compass_rotation', bearing);
            console.log(bearing)
        },
        toRadians (angle) {
            return angle * (Math.PI / 180);
        },
        toDegrees(angle) {
            return (angle*180/Math.PI + 360);
        },
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

    }

}
</script>