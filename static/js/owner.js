var app = angular.module('owner', []);

app.controller('ownerController', function($scope) {
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.loggedIn = false;
    
    socket.on('connect', function() {
        console.log('connected');
    });
    
    $scope.test = function(){
        console.log("Entered $scope.test");
    };
    
    
    
});