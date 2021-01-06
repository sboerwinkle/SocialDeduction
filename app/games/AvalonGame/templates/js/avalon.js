{% include "components/main.js" %}

$(document).ready(function () {
    socket.on('game_start', function (data) {
        $('#chat').val($('#chat').val() + "Everyone is Ready! Select the roles to play with!" + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);

        // hide the ready button
        var ready_button = document.getElementById("lobby-ready")
        ready_button.style.display = "none"
        // show lobby list without ready info.
        list(players, false);

        // now we emit the start to the specific game start and the game.js and events will take over.
        socket.emit(game_name+'_ready', {"scene":0, "room": room_id});
    });


    

});