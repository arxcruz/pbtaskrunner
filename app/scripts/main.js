'use strict';

var angular = require('angular');

// Angular modules

require('angular-ui-bootstrap');
require('angular-utils-pagination');
require('angular-route');

// jQuery and Bootstrap
global.jQuery = require('jquery');
require('bootstrap');

// Modules
require('./controllers');
require('./factories/_index');
require('./directives/_index');
require('./filters/_index');

var requires = [
    'ngRoute',
    'ui.bootstrap',
    'angularUtils.directives.dirPagination',
    'pbtaskrunner.controllers',
    'pbtaskrunner.factories',
    'pbtaskrunner.directives',
    'pbtaskrunner.filters'
];

angular.module('pbtaskrunner', requires);

var onConfig = require('./on_config');
angular.module('pbtaskrunner').config(onConfig);

angular.module('pbtaskrunner').constant('AppSettings', require('./constants'));

angular.bootstrap(document, ['pbtaskrunner']);
