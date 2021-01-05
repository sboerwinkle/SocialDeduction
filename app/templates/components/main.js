// Jinja2 to Javascript. Oh the horror.
var room_id = {{ game_info["room_id"] | tojson}};
var player_id = {{ game_info["player_id"] | tojson}};
var player_name = {{ game_info["player_name"] | tojson}};
var socket;

var players;

$(document).ready(function () {
    socket = io.connect('http://localhost:5000');
    socket.on('connect', function () {
        socket.emit('joined', { "room": room_id, "player_id": player_id, "player_name": player_name });
    });
    socket.on('player_change', function (data) {
        // deal with players joining.
        if (data.type == "add") {
            $('#chat').val($('#chat').val() + '<' + data.change.player + ' has entered the room.>\n');
        }

        // deal with players leaving.
        if (data.type == "leave") {
            $('#chat').val($('#chat').val() + '<' + data.change.player + ' has left the room.>\n');
        }

        // ready change
        if (data.type == "ready") {
            // $('#chat').val($('#chat').val() + '<' + data.change.player + ' has changed ready state>\n');
        }


        $('#chat').scrollTop($('#chat')[0].scrollHeight);

        // update list of players
        players = data.players;
        var list = function (players) {
            var player_list = document.getElementById('lobby-player-list');
            player_list.innerHTML = ""
            for (var i = 0; i < players.length; i++) {
                var player_item = '<li>'
                if (players[i].id == player_id) {
                    player_item += "(You) <b>" + players[i].name + "</b>"
                } else {
                    player_item += players[i].name;
                }
                player_item += " | ";
                if (players[i].ready) {
                    player_item += 'Ready! '
                } else {
                    player_item += 'Not Ready! '
                }
                player_item += '</li>'
                player_list.innerHTML += player_item;
            }
        }
        list(players);

    });
    socket.on('message', function (data) {
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#text').keypress(function (e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', { msg: text, "room": room_id, "player_id": player_id, "player_name": player_name });
        }
    });

    $('#lobby-ready-button').change(
        function () {
            var ready = false;
            if (this.checked) {
                ready = true;
                document.getElementById('lobby-ready-text').innerHTML = "Ready!" 
            } else {
                ready = false;
                document.getElementById('lobby-ready-text').innerHTML = "Not Ready!"
            }

            // TODO: emit ready change.
            socket.emit('ready change', { "room": room_id, "player_id": player_id, "ready": ready })
        }
    );



});
function leave_room() {
    socket.emit('left', { "room": room_id, "player_id": player_id, "player_name": player_name }, function () {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}