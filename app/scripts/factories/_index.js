'use strict';

var angular = require('angular');
var bulk = require('bulk-require');

module.exports = angular.module('pbtaskrunner.factories', []);

bulk(__dirname, ['./**/!(*_index|*.spec).js']);
