'use strict';

function OnConfig($routeProvider) {
    $routeProvider.otherwise({
        templateUrl: '/views/default.html'
    });
}

module.exports = OnConfig;
