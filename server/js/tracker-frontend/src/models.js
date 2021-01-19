const axios = require('axios');

class BaseModel {
    xhr(options) {
        if (typeof options == "string") {
            options = {'url': options};
        }

        options['responseType'] = 'json';
        options['maxRedirects'] = 0;

        return axios(options);
    }
}

export class UserSettings {
    updateSettings() {

    }
}

export class DevicesSettings extends BaseModel {
    save = (imei, newValue, onDone, onFail) => {
        this.xhr({
            'url': '/devices/settings/'+imei,
            'method': "POST", 
            'contentType': 'application/json;charset=UTF-8',
            'dataType': 'json',
            'data': newValue
         }
        )
        .then(onDone)
        .catch(onFail) 
    }
}

export class SharedDevices extends BaseModel {
    constructor(onListUpdate) {
        super();
        this.onUpdateCallback = onListUpdate;
    }

    add = (description, onSuccess, onFail) => {
        this.xhr({
                'url': '/shared/link',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': description
             }
        )
        .then( (data) => { onSuccess(data); this.list() })
        .catch(onFail)
    };

    remove = (onSuccess, onFail)  => {
        this.xhr('/shared/remove')
        .then(onSuccess)
        .catch(onFail)
    };

    list = (onSuccess, onFail ) => {
        let thisCopy=this;
        this.xhr({'url': '/shared/list'})
        .then(
            function(data) {
                console.log(data)
                thisCopy.onUpdateCallback(data.data);
                if (onSuccess) {
                    onSuccess(data.data); 
                }
            }
        )
        .catch(onFail)
    };

}

export class User extends BaseModel {
    constructor() {
        super();
    }

    login = (description, onSuccess, onFail) => {
        this.xhr({
                'url': '/auth',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': description
             }
        )
        .then(onSuccess)
        .catch(onFail)
    };

    logout = (onSuccess, onFail)  => {
        this.xhr('/logout')
        .then(onSuccess)
        .catch(onFail)
    };

    signup = (description, onSuccess, onFail ) => {
        this.xhr({
                'url': '/signup',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': description
                }
        )
        .then(onSuccess)
        .catch(onFail)
    };
}

export class Devices extends BaseModel {

    constructor(onUpdate, beforeUpdateCallback) {
        super();
        this.onUpdateCallback = onUpdate;
        this.beforeUpdateCallback = beforeUpdateCallback;
        this.devices = [] 
    }

    remove = function(/*imei*/) {

    };

    add = (description, onSuccess, onFail) => {
        let thisCopy = this;
        this.xhr({
                'url': '/devices/add',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': description
             }
        )
        .then(function(data) {
            console.log(data);
            thisCopy.reload(onSuccess, onFail); 
        })
        .catch(function(jqXHR) {
                if (onFail) {
                    onFail(jqXHR);
                }
         });
    };

    reload = (onSuccess, onFail) => {
        if (this.beforeUpdateCallback) {
            this.beforeUpdateCallback();
        }
        let thisCopy = this;

        this.xhr('/devices')
            .then(function(data) {
                console.log(data)
                thisCopy.devices=data;
                thisCopy.onUpdateCallback(thisCopy.devices);

                if (onSuccess) {
                    onSuccess(data); 
                }
            })
            .catch(function(jqXHR) { 
                if(onFail){ 
                    onFail(jqXHR);
                } 
            });
    };

}
