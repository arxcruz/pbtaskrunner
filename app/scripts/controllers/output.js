'use strict';

var angular = require('angular');

function OutputCtrl($scope, taskRunnerApi, $interval, $uibModalInstance,
                    selected_task) {
    $scope.close = close;
    $scope.selected_task = selected_task;
    $scope.output = '';
    $scope.setSelectionRange = setSelectionRange;

    refreshLoadTask();

    function close() {
        $interval.cancel($scope.refresh_id);
        $uibModalInstance.close();
    }

    function loadTask() {
        taskRunnerApi.getTask($scope.selected_task)
            .success(function(data) {
                $scope.output = data.output;
                if(data.status !== 'IN PROGRESS') {
                    $interval.cancel($scope.refresh_id);
                }
                var elem = angular.element(document.querySelector('#outputArea'));
                setSelectionRange(elem,
                                  $scope.output.length, $scope.output.length);
            });
    }

    function refreshLoadTask() {
        $scope.refresh_id = $interval(function() {
            loadTask();
        }, 4000);
    }

    function setSelectionRange(input, selectionStart, selectionEnd) {
        if (input.setSelectionRange) {
            console.log('Entrou setSelectionRange');
            var originalValue = input.val();
            var val = input.val();
            console.log('original: ' + val);
            input.val('');
            input.blur().focus().val(originalValue);
        }
        else if (input.createTextRange) {
            var range = input.createTextRange();
            range.collapse(true);
            range.moveEnd('character', selectionEnd);
            range.moveStart('character', selectionStart);
            range.select();
        }
    }
}

export default {
    name: 'outputCtrl',
    fn: OutputCtrl
};
