const axios = require('axios');
const template = require('url-template');

const API_METHODS = {
    'getCSRF':               {'url':'/csrf'},
    'saveDeviceSettings':    {'url': '/devices/settings/{imei}', 'method': 'post'},
    'getSharingLink':        {'url': '/shared/link', 'method':"post"},
    'unshareDevice':         {'url': '/shared/remove/{id}', 'method': 'delete'},
    'listSharedDevices':     {'url': '/shared/list'},
    'signIn':                {'url': '/auth', 'method': "post"},
    'logout':                {'url': '/logout',},
    'signUp':                {'url': '/signup', 'method': "post"},
    'addNewDevice':          {'url': '/devices/add', 'method': 'post'},
    'getDevicesList':        {'url': '/devices'},
    'removeDevice':          {'url': '/devices/{imei}', 'method': 'delete'},
};

const handler = {
    get: function(target, name) {
       if (target['name']) {
           return target['name']; 
       }

       let axios = target.client;
       let description = API_METHODS[name];

       if (description == null) {
           throw "Unknown api method";
       }
        
       var parsedUrl = template.parse(description.url);

       return function(url_params, post_data) {
           let url = parsedUrl.expand(url_params || {});

           return axios.request({
               'url' : url,
               'responseType': 'json',
               'method': description.method || 'get',
               'contentType': 'application/json;charset=UTF-8',
               'dataType': 'json',
               'headers': {"X-CSRFToken": target['csrf']},
               'data': post_data 
           });
        }
     },
     set: function(target, name, value) {
        target[name] = value;
        return true;
      }
}

const _api = {
    csrf: null,
    client: axios.create({ timeout: 1000}),
};

export let API = new Proxy(_api, handler);

