class BaseModel {
    constructor(csrf) {
        this.csrf = csrf;        
    } 

    xhr(options) {
        if (typeof options == "string") {
            options = {'url': options};
        }

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

class SharedDevices extends BaseModel {
    constructor(csrf, onListUpdate) {
        super(csrf);
        this.onUpdateCallback = onListUpdate;
    }

    add = (description, onSuccess, onFail) => {
        this.xhr({
                'url': '/shared/link',
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
        this.xhr('/shared/remove')
        .done(onSuccess)
        .fail(onFail)
    };

    list = (onSuccess, onFail ) => {
        let thisCopy=this;
        this.xhr({'url': '/shared/list'})
        .done(
            function(data) {
                console.log(data)
                thisCopy.onUpdateCallback(data);
                if (onSuccess) {
                    onSuccess(data); 
                }
            }
        )
        .fail(onFail)
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

class Devices extends BaseModel {

    constructor(csrf, onUpdate, beforeUpdateCallback) {
        super(csrf);
        this.onUpdateCallback = onUpdate;
        this.beforeUpdateCallback = beforeUpdateCallback;
        this.devices = [] 
    }

    remove = function(imei) {

    };

    add = (description, onSuccess, onFail) => {
        let thisCopy = this;
        this.xhr({
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
        this.xhr('/devices')
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