var app = angular.module('app', []);

app.controller('controller', function($scope, $sce) {
    var socket = io.connect('https://' + document.domain + ':' + location.port);
    
    // required for audio player
    $scope.trustedUrl = function(url) {
        return $sce.trustAsResourceUrl(url);
    };
    
    $scope.loggedIn = false;
    $scope.playing = false;
    $scope.player = document.getElementById('nowPlaying');
    
    // listen for end of song, move to next in queue
    $scope.player.addEventListener('ended', function(){
        var last = $scope.queue.pop();
        console.log("Song ended.  Now playing... " + last.title);
        $scope.play(last);
        $scope.remove(last);
    });
    
    $scope.selectedTrack = {
        title: "None",
        genre: "None",
        url: "None",
        id: 0,
    };
    
    $scope.nowPlaying = {
        title: "None",
        genre: "None",
        url: "static/media/RickRoll.webm",
        id: 0,
    };
    
    $scope.nowPlayingSrc = $scope.nowPlaying.url;
    
    $scope.queue = [];
    $scope.uniqueQueueID = 1;
    
    $scope.volume = 1;
    
    socket.on('connect', function() {
        console.log('connected');
        console.log('$scope.nowPlaying.url: ' + $scope.nowPlaying.url);
        console.log("path: " + $scope.nowPlayingSrc);
        console.log("audio path: " + document.getElementById('nowPlaying').src);

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
        $scope.selectedTrack.title = id;
    };
    
    // pushes selected track to queue
    // TODO: Actually query a database instead of an incredibly tedious switch statement
    $scope.push = function() {
        console.log("Entered $scope.addToQueue on scope.js");
        switch($scope.selectedTrack.title){
            case 'A3':
                $scope.queue.push({
                    title: $scope.selectedTrack.title,
                    genre: "genre",
                    id: $scope.uniqueQueueID,
                    url: "static/media/LetGoArkPatrol.webm",
                });
                $scope.uniqueQueueID++;
                break;
            
            case 'B1':
                $scope.queue.push({
                    title: $scope.selectedTrack.title,
                    genre: "genre",
                    id: $scope.uniqueQueueID,
                    url: "static/media/Prismo.webm",
                });
                $scope.uniqueQueueID++;
                break;
                
            case 'B3':
                $scope.queue.push({
                    title: $scope.selectedTrack.title,
                    genre: "genre",
                    id: $scope.uniqueQueueID,
                    url: "static/media/10sec.m4a",
                });
                $scope.uniqueQueueID++;
                break;
                
            default:
                $scope.queue.push({
                    title: $scope.selectedTrack.title,
                    genre: "genre",
                    id: $scope.uniqueQueueID,
                    url: "static/media/RickRoll.webm",
            });
            $scope.uniqueQueueID++;
            break;   
                
        }
        
        
        console.log("$scope.queue entries: ");
        for (let i=0; i < $scope.queue.length; i++){
            console.log($scope.queue[i].title + ", " + $scope.queue[i].genre + ", " + $scope.queue[i].url + ", " + $scope.queue[i].id);
        }
    };
    
    // remove specific track from queue
    $scope.remove = function(track) {
        console.log("Entered $scope.remove in app.js");
        for (let i = 0; i < $scope.queue.length; i++) {
            if ($scope.queue[i].id == track.id) {
                console.log("Found matching IDs: " + $scope.queue[i].id + ", " + track.id);
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
        console.log("Entered $scope.play on app.js, params: " + track.title + ", " + track.genre + ", " + track.url + ", " + track.id);
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
