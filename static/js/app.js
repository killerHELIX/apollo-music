var app = angular.module('app', []);

app.controller('controller', function($scope) {
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    $scope.loggedIn = false;
    $scope.nowPlaying = {
        title: "None",
        style: "None",
        id: 0,
    };
    $scope.nowPlaying = {
        title: "None",
        style: "None",
        id: 0,
    };
    
    $scope.queue = [];
    $scope.uniqueQueueID = 1;
    
    socket.on('connect', function() {
        console.log('connected');
    });
    
    // changes loggedIn to true
    $scope.login = function(username, password) {
        console.log("Entered $scope.login in app.js");
        $scope.currentUser = username;
        $scope.loggedIn = true;
        console.log("Received " + username + " and " + password);
        console.log("$scope.username: " + $scope.username + ", $scope.password: " + $scope.password);
        
    };
    
    // changes loggedIn to false
    $scope.logout = function() {
        console.log("Entered $scope.logout in app.js");
        $scope.loggedIn = false;
        console.log("Received " + $scope.username + " and " + $scope.password);
    };
    
    $scope.selectTrack = function($event){
        console.log("Entered $scope.selectTrack in app.js");
        var element = event.target;
        var id = element.id;
        console.log("Received " + id);
        
        // set selected track
        $scope.selectedTrack = id;
    };
    
    $scope.addToQueue = function(selectedTrack) {
        console.log("Entered $scope.addToQueue on scope.js");
        $scope.queue.push({
            track: selectedTrack,
            style: "Style: Chosen at Info",
            id: $scope.uniqueQueueID,    
            });
        $scope.uniqueQueueID++;
        console.log("$scope.queue entries: ");
        for (let i=0; i < $scope.queue.length; i++){
            console.log($scope.queue[i].track + ", " + $scope.queue[i].id);
        }
    };
    
    // Plays selected track without removing from the queue
    $scope.play = function(track){
        console.log("Entered $scope.play on app.js, param " + track.title);
        $scope.nowPlaying = track;
    }
    
    
});
