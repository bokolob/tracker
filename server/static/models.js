class BaseModel {
    constructor(csrf) {
        this.csrf = csrf;        
    } 

    xhr(options) {
        let prevBeforeSend = options['beforeSend'];
        let wrapper = null;
        let thisCopy=this;

        wrapper = function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", thisCopy.csrf);
            }
            if (prevBeforeSend != null) {
                prevBeforeSend(xhr, settings);
            }
        }

        options['beforeSend'] = wrapper;

        let result = $.ajax(options); 

        options['beforeSend'] = prevBeforeSend;

        return result;
    }

}

class UserSettings {
    updateSettings() {

    }
};

class Friends {
    constructor(onListUpdate, onRequestsUpdate) {
        this.onListUpdateCallback = onListUpdate;
        this.onRequestsUpdateCallback = onRequestsUpdate;
    }

    add = (description, onSuccess, onFail) => {
        $.ajax({
                'url': '/friends/add',
                'method': "POST", 
                'contentType': 'application/json;charset=UTF-8',
                'dataType': 'json',
                'data': JSON.stringify(description)
             }
        )
        .done( (data) => { onSuccess(data); this.list() })
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

    accept = (id) => {
        alert("accept " + id);
    };

    reject = (id) => {
        alert("reject " + id);
    };

}

class User extends BaseModel {
    constructor(csrf) {
        super(csrf);
    }

    login = (description, onSuccess, onFail) => {
        this.xhr({
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
        this.xhr('/logout')
        .done(onSuccess)
        .fail(onFail)
    };

    signup = (description, onSuccess, onFail ) => {
        this.xhr({
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