function playPause() {
    console.log("Entered playPause() on media.js")
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

function changeVolume() {
    console.log("Entered changeVolume on media.js")
    var player = document.getElementById("nowPlaying");
    var slider = document.getElementById("volume");

    player.volume = slider.value;
}