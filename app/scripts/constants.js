'use strict';

var apiUrl = 'http://localhost:5000';

var AppSettings = {
    environmentApiUrl: apiUrl + '/api/v1.0/envs',
    taskRunnerApiUrl: apiUrl + '/api/v1.0/testtask',
    testApiUrl: apiUrl + '/api/v1.0/tests'
};

module.exports = AppSettings;
