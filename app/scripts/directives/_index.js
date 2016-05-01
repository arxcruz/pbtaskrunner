'use strict';

var angular = require('angular');
var bulk = require('bulk-require');

module.exports = angular.module('pbtaskrunner.directives', []);

bulk(__dirname, ['./**/!(*_index|*.spec).js']);
