class AjaxForm {
    #form;
    #modelCallback;
    #onDoneCallback;
    #onFailCallback;

    constructor(form, modelCallback, onDoneCallback, onFailCallback) {
        this.#form = $(form);
        this.#modelCallback = modelCallback;
        this.#onDoneCallback=onDoneCallback;
        this.#onFailCallback=onFailCallback;
    }

    bind() {
        let thisCopy = this;
        this.#form.submit(function(e) { thisCopy.#onSubmit(e) });
        return this;
    }

    #serializeForm() {
        let a = this.#form.serializeArray();
        let o = {};

        a.forEach(pair => {
            o[pair['name']] = pair['value'];
        });    

        return o;
    }

    #onDone(data)
    {
        console.log(data);
        if (data.redirect) {
            window.location.href = data.redirect;
        }

        this.#form.find(":input").removeClass("is-invalid");
        this.#form.find(":input").removeClass("is-valid");
        this.#form.find(":input").siblings(".invalid-tooltip").empty();

        if (this.#onDoneCallback) {
            this.#onDoneCallback(data); 
        }

    }

    #onFail(jqXHR) {
        if (jqXHR.responseJSON) {
            let data = jqXHR.responseJSON;
            console.log(data);
            for (var prop in data.errors) {
                let input = this.#form.find("input[name="+prop+"]");
                
                console.log(["input[name="+prop+"]", input, data.errors[prop]]);

                if (input.length) {
                    input.siblings(".invalid-tooltip")[0].innerHTML = data.errors[prop]; 
                    input.addClass("is-invalid");
                }
            }
        }
        if (this.#onFailCallback) {
            this.#onFailCallback(); 
        }
    }

    #onSubmit(e){
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var url = this.#form.attr('action');

        if (!this.#form[0].checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            this.#form[0].classList.add('was-validated');
            return false;
        }

        this.#form.addClass('was-validated');
        this.#form.find(":input").removeClass("is-invalid");
        this.#form.find(":input").siblings(".invalid-tooltip").empty();

        let thisCopy = this;

        this.#modelCallback(this.#serializeForm(), 
                            function(data) {thisCopy.#onDone(data)},
                            function(jqXHR) {thisCopy.#onFail(jqXHR)}
        );

        return false;
    }
}