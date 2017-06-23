var app = angular.module('app', []);
var socket = io.connect('https://' + document.domain + ':' + location.port);

app.service('shared', function() {
    var loggedIn = false;
    var currentUser = "";
    
    return {
        isLoggedIn: function () {
            return loggedIn;
        },
        
        setLoggedIn: function (value) {
            loggedIn = value;
        },
        
        getCurrentUser: function () {
            return currentUser;
        },
        
        setCurrentUser: function(value) {
            currentUser = value;
        },
    };
});

app.controller('owner', function($scope, $sce, shared) {
    
    // required for audio player
    $scope.trustedUrl = function(url) {
        return $sce.trustAsResourceUrl(url);
    };
    
    $scope.playing = false;
    $scope.player = document.getElementById('nowPlaying');
    
    // listen for end of song, move to next in queue
    if ($scope.player != null) {
        $scope.player.addEventListener('ended', function(){
            if ($scope.queue.length != 0) {
                var last = $scope.queue.pop();
                console.log("Song ended.  Now playing... " + last.title);
                $scope.nowPlaying = last;
                $scope.play(last);
                $scope.remove(last);
                $scope.$apply();
            // if at end of queue, continue playing the same track
            } else {
                console.log('At end of queue.  Replaying...');
                $scope.player.play();
            }
        });
    } else {
        console.log("This page doesn't have an audio player!");
    }
    
    $scope.selectedTrack = {
        title: "None",
        genre: "None",
        url: "None",
        queueID: 0,
    };
    
    $scope.nowPlaying = {
        title: "None",
        genre: "None",
        url: "static/media/RickRoll.webm",
        queueID: 0,
    };
    
    $scope.nowPlayingSrc = $scope.nowPlaying.url;
    
    $scope.queue = [];
    $scope.uniqueQueueID = 1;
    
    $scope.volume = 1;
    
    socket.on('connect', function() {
        console.log('Owner CTRL connected.');
        console.log('$scope.nowPlaying.url: ' + $scope.nowPlaying.url);
        console.log("path: " + $scope.nowPlayingSrc);
        console.log("audio path: " + document.getElementById('nowPlaying').src);

    });
    
    
    
    $scope.selectTrack = function($event){
        console.log("Entered $scope.selectTrack in owner CTRL (app.js)");
        var element = event.target;
        var id = element.id;
        console.log("Received " + id);
        
        // set selected track
        $scope.selectedTrack.title = id;
        
        socket.emit('findTrack', $scope.selectedTrack);
    };
    
    
    $scope.debugPopulateDB = function() {
        console.log("Entered debugPopulateDB on owner CTRL (app.js)");
        socket.emit('debugPopulateDB');
    };
    
    socket.on('foundTrack', function(track) {
        console.log("Entered foundTrack on owner CTRL (app.js)");
        // update selectedTrack with new info
        $scope.selectedTrack = track;
        console.log('track then selectedTrack');
        console.log(track);
        console.log($scope.selectedTrack.subtracks);
        $scope.$apply();
    });
    
    // pushes selected track to queue
    // TODO: Actually query a database instead of an incredibly tedious switch statement
    $scope.push = function(track) {
        console.log("Entered $scope.push on owner CTRL (app.js)");
        track['queueID'] = $scope.uniqueQueueID;
        $scope.queue.push(track);
        $scope.uniqueQueueID++;
        
        console.log("$scope.queue entries: ");
        for (let i=0; i < $scope.queue.length; i++){
            console.log($scope.queue[i].title + ", " + $scope.queue[i].genre + ", " + $scope.queue[i].url + ", " + $scope.queue[i].queueID);
        }
    };
    
    // remove specific track from queue
    $scope.remove = function(track) {
        console.log("Entered $scope.remove in owner CTRL (app.js)");
        for (let i = 0; i < $scope.queue.length; i++) {
            if ($scope.queue[i].queueID == track.queueID) {
                console.log("Found matching IDs: " + $scope.queue[i].queueID + ", " + track.queueID);
                $scope.queue.splice(i,1);
                console.log("new $scope.queue entries: ");
                break;
            }
        }
        for (let i=0; i < $scope.queue.length; i++){
            console.log($scope.queue[i].title + ", " + $scope.queue[i].genre + ", " + $scope.queue[i].url + ", " + $scope.queue[i].id);
        }
        
           
    };
    
    // Plays selected track without removing from the queue
    $scope.play = function(track){
        console.log("Entered $scope.play on owner CTRL (app.js), params: " + track.title + ", " + track.genre + ", " + track.url + ", " + track.id);
        $scope.nowPlaying = track;
        
        // load new url to player
        $scope.updatePlayer('nowPlaying', track);
        $scope.player.play();
        console.log("audio path: " + document.getElementById('nowPlaying').src);
    };
    
    // updates and reloads player with new track
    $scope.updatePlayer = function(id, track) {
        var player = document.getElementById(id);
        player.src = track.url;
        player.load();
    };
    
    
    // update button icons
    $scope.isPlaying = function() {
        if ($scope.player.paused) {
            return "btn btn-default btn-lg fa fa-play";
        } else {
            return "btn btn-default btn-lg fa fa-pause";
        }
    };
    
});

app.controller('layout', function($scope, $sce, shared) {
    $scope.loggedIn = shared.isLoggedIn();
    $scope.currentUser = shared.getCurrentUser();
    
    socket.on('connect', function() {
        console.log("Layout CTRL connected.");
        console.log("shared.loggedIn: " + shared.isLoggedIn());
        console.log("$scope.loggedIn: " + $scope.loggedIn);

    });
    
    // wrapper to guarantee value integrity
    $scope.setLoggedIn = function (value) {
        $scope.loggedIn = value;
        shared.setLoggedIn(value);
    }
    
    $scope.setCurrentUser = function (value) {
        $scope.currentUser = value;
        shared.setCurrentUser(value);
    }
   
    // changes loggedIn to true
    $scope.login = function(username, password) {
        console.log("Entered $scope.login in layout CTRL (app.js)");
        socket.emit('validateLogin', username, password);
        $scope.setCurrentUser(username);
        $scope.setLoggedIn(true);
        console.log("Received " + username + " and " + password);
        console.log("$scope.username: " + $scope.username + ", $scope.password: " + $scope.password);
        console.log("shared.loggedIn: " + shared.isLoggedIn());
        console.log("$scope.loggedIn: " + $scope.loggedIn);
        
    };
    
    // changes loggedIn to false
    $scope.logout = function() {
        console.log("Entered $scope.logout in layout CTRL (app.js)");
        $scope.setLoggedIn(false);
        console.log("Received " + $scope.username + " and " + $scope.password);
        console.log("shared.loggedIn: " + shared.isLoggedIn());
        console.log("$scope.loggedIn: " + $scope.loggedIn);

    };
   
    // passes new user info to server for database insertion
    $scope.register = function(username, password) {
        console.log("Entered $scope.register in layout CTRL (app.js)");
        socket.emit('registerNew', username, password);
        
    };

});
