class UserSettings {
    #settings;
    updateSettings() {

    }
};

class User {
    login(description, onFail, onSuccess) {
        $.ajax({
                'url': '/auth',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': JSON.stringify(description)
             }
        )
        .done(onSuccess)
        .fail(onFail)
    }

    logout(onFail, onSuccess) {
        $.ajax('/logout')
        .done(onSuccess)
        .fail(onFail)
    }

    signup(description, onFail, onSuccess ) {
        $.ajax({
                'url': '/signup',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': JSON.stringify(description)
                }
        )
        .done(onSuccess)
        .fail(onFail)
    }
};

class Devices {
    #beforeUpdateCallback;
    #onUpdateCallback;
    #devices = []

    constructor(onUpdate, beforeUpdateCallback) {
        this.#onUpdateCallback=onUpdate;
        this.#beforeUpdateCallback = beforeUpdateCallback;
    }

    removeDevice(imei) {
    }

    addDevice(description, onFail, onSuccess) {
        let thisCopy = this;
        $.ajax({
                'url': '/devices/add',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': JSON.stringify(description)
             }
        )
        .done(function(data) {
            console.log(data);
            thisCopy.#devices.push(description);
            thisCopy.getDevices(onFail, onSuccess); 
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
                if (onFail) {
                    onFail(jqXHR, textStatus, errorThrown);
                }
         });
    }

    getDevices(onFail, onSuccess) {
        this.#beforeUpdateCallback();
        let thisCopy = this;
        $.ajax('/devices')
            .done(function(data) {
                console.log(data)
                thisCopy.#devices=data;
                thisCopy.#onUpdateCallback(thisCopy.#devices);

                if (onSuccess) {
                    onSuccess(data); 
                }
            })
            .fail( function(jqXHR) { if(onFail){ onFail(jqXHR); } });
    }



}