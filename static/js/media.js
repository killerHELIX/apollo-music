function playPause() {
    var element = document.getElementById("nowPlaying");
    
    if (element.paused) {
        element.play();
        $('#nowPlayingSelector').click(function(){
            $(this).addClass('fa-pause');
            $(this).removeClass('fa-play');
        });
    } else {
        element.pause();
        $('#nowPlayingSelector').click(function(){
            $(this).addClass('fa-play');
            $(this).removeClass('fa-pause');
        });
    }
    

}