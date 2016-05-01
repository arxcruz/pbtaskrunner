'use strict';

var angular = require('angular');

function TaskRunnerCtrl($scope, $uibModal, $interval, testApi, environmentApi,
                        taskRunnerApi) {
    $scope.errorMessage = '';
    $scope.environments = [];
    $scope.selectedInterface = 'celery';
    $scope.results = [];
    $scope.createTask = createTask;
    $scope.getTaskOutput = getTaskOutput;
    $scope.currentPage = 1;
    $scope.pageSize = 10;
    $scope.loading = false;

    getTests();
    getEnvironments();
    updateTasks();

    function clearAll() {
        $scope.errorMessage = '';
        $scope.successMessage = '';
        $scope.selectedTest = '';
        $scope.requester = '';
        $scope.selectedEnvironment = '';
    }

    function getTasks() {
        taskRunnerApi.getTasks()
            .success(function(data) {
                $scope.results = data;
            })
            .finally(function() {
                $scope.loading = false;
            });
    }

    function getTests() {
        testApi.getTests()
            .success(function(data) {
                $scope.tests = data.tests;
            });
    }

    function getEnvironments() {
        environmentApi.getEnvironments()
            .success(function(data) {
              $scope.environments = data;
            });
    }

    function updateTasks() {
        $interval(function() {
            getTasks();
        }, 4000);
    }

    function createTask() {
        $scope.$broadcast('show-errors-check-validity');
        var task = {};
        task.requester = $scope.requester;
        task.test_environment = $scope.selectedEnvironment.id;
        task.template = $scope.selectedTest;

        taskRunnerApi.createTask(task)
            .success(function(data) {
                $scope.successMessage = 'Test added sucessfully';
                clearAll();
                getTasks();
            })
            .error(function(errorInfo, status) {
                $scope.errorMessage = 'An error ocurred: ' + errorInfo.message;
            });
    }

    function getTaskOutput(selected_task) {
        console.log('passou');
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'output.html',
            controller: 'outputCtrl',
            windowClass: 'app-modal-window',
            resolve: {
                selected_task: function() {
                    return selected_task;
                }
            }
        });
    }
}

export default {
    name: 'taskRunnerCtrl',
    fn: TaskRunnerCtrl
};
