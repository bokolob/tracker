class UserSettings {
    updateSettings() {

    }
};

class Friends {
    add = (description, onSuccess, onFail) => {
        $.ajax({
                'url': '/friends/add',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': JSON.stringify(description)
             }
        )
        .done(onSuccess)
        .fail(onFail)
    };

    remove = (onSuccess, onFail)  => {
        $.ajax('/friends/remove')
        .done(onSuccess)
        .fail(onFail)
    };

    list = (onSuccess, onFail ) => {
        $.ajax({'url': '/friends'})
        .done(onSuccess)
        .fail(onFail)
    };
}

class User {
    login = (description, onSuccess, onFail) => {
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
    };

    logout = (onSuccess, onFail)  => {
        $.ajax('/logout')
        .done(onSuccess)
        .fail(onFail)
    };

    signup = (description, onSuccess, onFail ) => {
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
    };
}

class Devices {

    constructor(onUpdate, beforeUpdateCallback) {
        this.onUpdateCallback = onUpdate;
        this.beforeUpdateCallback = beforeUpdateCallback;
        this.devices = [] 
    }

    remove = function(imei) {
    }.bind(this);

    add = (description, onSuccess, onFail) => {
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
            thisCopy.reload(onSuccess, onFail); 
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
                if (onFail) {
                    onFail(jqXHR, textStatus, errorThrown);
                }
         });
    };

    reload = (onSuccess, onFail) => {
        this.beforeUpdateCallback();
        let thisCopy = this;
        $.ajax('/devices')
            .done(function(data) {
                console.log(data)
                thisCopy.devices=data;
                thisCopy.onUpdateCallback(thisCopy.devices);

                if (onSuccess) {
                    onSuccess(data); 
                }
            })
            .fail( function(jqXHR) { if(onFail){ onFail(jqXHR); } });
    };

}