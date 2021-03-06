import Vue from 'vue';

 Vue.component('form-ajax', {
    props: ['arguments'],
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
                                if (data.redirect) {
                                    window.location.href = data.redirect;
                                }
                                
                                this.requestFields = {};
                                this.failed = false;
                                this.success = true;
                                this.response = data;
                            }, 
                            (jqXHR) => {
                                this.failed = true;
                                this.success = false;
                                if (jqXHR.responseJSON) {
                                    this.errors = jqXHR.responseJSON.errors;
                                }
                            });
       }
    }
});