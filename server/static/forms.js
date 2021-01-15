
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

class AjaxForm {

    constructor(form, modelCallback, onDoneCallback, onFailCallback) {
        this.form = $(form);
        this.modelCallback = modelCallback;
        this.onDoneCallback=onDoneCallback;
        this.onFailCallback=onFailCallback;
    }

    init = () => {
        let thisCopy = this;
        this.form.submit(function(e) { thisCopy.onSubmit(e) });
        return this;
    };

    serializeForm() {
        let a = this.form.serializeArray();
        let o = {};

        a.forEach(pair => {
            o[pair['name']] = pair['value'];
        });    

        return o;
    }

    onDone = (data) =>
    {
        console.log(data);
        if (data.redirect) {
            window.location.href = data.redirect;
        }

        this.form.find(":input").removeClass("is-invalid");
        this.form.find(":input").removeClass("is-valid");
        this.form.find(":input").siblings(".invalid-tooltip").empty();
        this.form.find(".alert-success").removeClass("d-none");

        if (this.onDoneCallback) {
            this.onDoneCallback(data); 
        }

        this.form.reset();

    };

    onFail = (jqXHR) => {
        this.form.find(".alert-danger").removeClass("d-none");
        if (jqXHR.responseJSON) {
            let data = jqXHR.responseJSON;
            console.log(data);
            for (var prop in data.errors) {
                let input = this.form.find("input[name="+prop+"]");
                
                console.log(["input[name="+prop+"]", input, data.errors[prop]]);

                if (input.length) {
                    input.siblings(".invalid-tooltip")[0].innerHTML = data.errors[prop]; 
                    input.addClass("is-invalid");
                }
            }
        }
        if (this.onFailCallback) {
            this.onFailCallback(); 
        }
    };

    onSubmit = (e) => {
        e.preventDefault(); // avoid to execute the actual submit of the form.

        if (!this.form[0].checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            this.form.addClass('was-validated');
            return false;
        }

        this.form.addClass('was-validated');
        this.form.find(":input").removeClass("is-invalid");
        this.form.find(":input").siblings(".invalid-tooltip").empty();
        
        this.form.find(".alert-success").addClass("d-none");
        this.form.find(".alert-danger").addClass("d-none");

        this.modelCallback(this.serializeForm(), this.onDone, this.onFail);

        return false;
    };
}