class AjaxForm {
    #form;

    constructor(form) {
        this.#form = $($(form)[0]);
    }

    bind() {
        let thisCopy = this;
        this.#form.submit(function(e) { thisCopy.#onSubmit(e) });
    }

    #serializeFormToJson() {
        let a = this.#form.serializeArray();
        let o = {};

        a.forEach(pair => {
            o[pair['name']] = pair['value'];
        });    

        return JSON.stringify(o);
    }

    #onDone(data)
    {
        console.log(data); // show response from the php script.
        if (data.redirect) {
            window.location.href = data.redirect;
        }
        
        for (var prop in data.errors) {
            let input = this.#form.find("input[name="+prop+"]");

            if (input.length) {
                input.siblings(".invalid-tooltip")[0].innerHtml = data.errors[prop]; 
                input.addClass("is-invalid");
            }
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

        $.ajax({
                'url': url,
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': this.#serializeFormToJson()
               })
               .done(function(data) { thisCopy.#onDone })
               //TODO .fail()

        return false;
    }
}