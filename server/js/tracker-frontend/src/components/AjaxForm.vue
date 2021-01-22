<script>
export default {
    props: ['additional_data'],
    data() {
        return {
            success:false,
            failed:false,
            requestFields:{},
            response:{},
            errors:{}
        };
    },
    methods: {
            processForm: function(e) {
                let form = e.target;
                this.success=false;
                this.response = {};

                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                    form.classList.add('was-validated');
                    return;
                }
                
                this.$emit('process',
                            this.requestFields, 
                            (data) => {
                                this.requestFields = {};
                                this.failed = false;
                                this.success = true;
                                this.response = data;
                                this.errors = {}; 
                            }, 
                            (jqXHR) => {
                                this.failed = true;
                                this.success = false;
                                if (jqXHR.errors) {
                                    this.errors = jqXHR.errors;
                                }
                            });
       }
    }
}
</script>
