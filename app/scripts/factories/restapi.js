'use strict';

var angular = require('angular');
var factoriesModule = require('./_index.js');

function restApi($http) {

    function request(verb, param, apiUrl, data) {
        var req = {
            method: verb,
            url: url(param, apiUrl),
            data: data,
        };

        return $http(req);
    }

    function url(param, apiUrl) {
        if (param === null || !angular.isDefined(param)) {
            param = '';
        }
        return apiUrl + param;
    }

    return {
        get: function get(param, apiUrl) {
            return request('GET', param, apiUrl);
        },
        post: function post(data, apiUrl) {
            return request('POST', null, apiUrl, data);
        },
        put: function put(data, apiUrl) {
            return request('PUT', null, apiUrl, data);
        },
        del: function del(param, apiUrl) {
            return request('DELETE', param, apiUrl);
        },
    };
}

// Environment

function environmentApi($http, restApi, AppSettings) {
    return {
        getEnvironments: function() {
            return restApi.get(null, AppSettings.environmentApiUrl);
        }
    };
}

function taskRunnerApi($http, restApi, AppSettings) {
    return {
        getTasks: function() {
            return restApi.get(null, AppSettings.taskRunnerApiUrl);
        },
        createTask: function(task) {
            return restApi.post(task, AppSettings.taskRunnerApiUrl);
        },
        getTask: function(task) {
            return restApi.get(null, task.uri);
        }
    };
}

function testApi($http, restApi, AppSettings) {
    return {
        getTests: function() {
            return restApi.get(null, AppSettings.testApiUrl);
        }
    };
}

factoriesModule.factory('restApi', restApi)
               .factory('environmentApi', environmentApi)
               .factory('taskRunnerApi', taskRunnerApi)
               .factory('testApi', testApi);
