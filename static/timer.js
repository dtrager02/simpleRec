//gets a random list of animes based on options from home page
//couldn't use jquery get because it was asynchronous, causing undefined values
getRoundData = () => {
    console.log("got data");
    var temp = 0;
    $.ajax({
        async: false,
        type: 'GET',
        url: '/start',
        success: function(data) {
            temp = data['data'];
        }
    });
    return temp;
};
let interval = null;
let game = {
    data: getRoundData(),
    round: -1,
    points: 0.0,
    timer: 90,
    startTimer: () => {
        if (interval) { clearInterval(interval) };
        console.log("timer started");
        game.timer = 90;
        var start1 = game.timer;
        //creates iframe with settings
        interval = setInterval(function() {
            game.timer--;
            $('.slide').width(100 * game.timer / start1 + '%')
            $('.timer p').text(game.timer);
            if (game.timer === 0) {
                clearInterval(interval);
                displayAnswer("Ran out of time");
            }
        }, 1000);
    },
    nextRound: function() {
        this.startTimer();
        if (this.round < this.data.length) {
            this.round += 1;
            return this.data[this.round];
        } else {
            return null;
        }
    }
};
var player;
//loads iframe API
var tag = document.createElement('script');
tag.id = 'iframe-demo';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onYouTubeIframeAPIReady() {
    player = new YT.Player('yt', {
        width: 420,
        height: 310,
        videoId: 'Ua5UARWRYLA',
        playerVars: {
            autoplay: 1,
            loop: 1
        },
        events: {
            'onReady': onPlayerReady,
        }
    });
    console.log(player);
}

function onPlayerReady(event) {
    $('#yt').hide();
    event.target.mute();
    event.target.unMute();
    event.target.playVideo();
    updateScreen();
}



function updateScreen() {
    $('.answer').hide();
    $('#guess').attr("placeholder", "");
    $('.123').remove();
    console.log("updated screen");
    let temp = game.nextRound();
    console.log(temp);
    if (temp) {
        $('.correct-img').attr('src', temp[1]);
        $('.correct-title').text(temp[0]);
        $('.song-title').text(temp[3]);
        //makes assumption that player wants next song to play instantly
        player.loadVideoById(temp[2]);
        $('.round-num').text("Round: " + game.round);
        $('.points').text("Points: " + game.points);
    } else {
        $('.main').append(`<h1>Congratulations! You have earned ${game.points} points in ${game.round} rounds!</h1>`)
            //TODO show difficulty level in here too for context
    }
}

//$('.start').click(startTimer); //starts timer countdown
$('.cont').click(function() {
    updateScreen();

}); //hides overlay showing anime picture
//$('.quit').click(() => document.write($.get('/')));
//global var holding pause/mute states
let playerInfo = { "paused": 0, "muted": 0 };
//PAUSE BUTTON 
$('.pause-button').click(function() {
    console.log(player);
    if (playerInfo["paused"]) {
        player.playVideo();
        playerInfo["paused"] = 0;
    } else {
        player.pauseVideo();
        playerInfo["paused"] = 1;
    }
});

//MUTE BUTTON
$('.mute-button').click(function() {
    console.log(player);
    if (playerInfo["muted"]) {
        player.unMute();
        playerInfo["muted"] = 0;
    } else {
        player.mute();
        playerInfo["muted"] = 1;
    }
});


$('#guess').on('input', function() {
    if ($('#guess').val()) {
        //prevents empty query to sqlite
        $.get("/autocomplete/" + $('#guess').val(), function(data) { //sends GET request to server returning {'data':[...]}
            var results = "";
            data['data'].forEach((result) => { results += `<div class="result">
        <p>${result}</p></div>`; }); //inserts div for each matching anime from database
            $('.search-results').html(results); //updates html
            $('.search-results').show(); //shows if it is hidden
        });
    } else {
        $('.search-results').hide(); //if empty query, hide search results just in case
    }
});

$('.submit1').click(function() {
    console.log("submitted");
    if ($('#guess').val() == game.data[game.round][0]) {
        game.points += parseInt(parseFloat(game.timer) * parseFloat(10) / parseFloat(9));
        displayAnswer("Correct!");
    } else {
        $('#guess').val("");
        $('#guess').attr("placeholder", "Try again...");
    }
});
//Sets value of input when a title suggestion is clicked
$('.search-results').on("click", '.result', function() {
    console.log("result clicked");
    $('#guess').val($(this).find("p").text());
    $('.search-results').hide();
});

function displayAnswer(status) {
    if ($('.answer').css('display') == 'none') {
        $('.answer').show();
        $('.main').append(`<div class="123 .blur"></div>`);
        $('.status').text(status);
    }
}
$('.give-up').click(function() {
    console.log($('.answer').css('display'));
    displayAnswer("Gave up :(")
});

$('#guess').focusout(function() {
    if ($('.search-results:hover').length) { return; } //if mouse is over search results, do not hide to allow autofill click event
    $('.search-results').hide(); //hide results if not focusses (like every search engine)
});

//TODO hide answer HTML until it is ready to be shown (probably with a ) (so no inspector cheating) (probably in game object)
//TODO implement highscore system with sessions
//TODO add "report problem" feature with database and view
//TODO center everything properly (search bar especially)
//make answer accept english as well