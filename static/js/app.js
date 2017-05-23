var app = angular.module('app', []);

app.controller('controller', function($scope) {
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.loggedIn = false;
    
    socket.on('connect', function() {
        console.log('connected');
    });
    
    
    
});