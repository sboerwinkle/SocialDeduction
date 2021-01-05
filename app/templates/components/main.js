// Jinja2 to Javascript. Oh the horror.
var room_id = {{ game_info["room_id"] | tojson}};
var player_id = {{ game_info["player_id"] | tojson}};
var player_name = {{ game_info["player_name"] | tojson}};
var socket;
$(document).ready(function () {
    socket = io.connect('http://localhost:5000');
    socket.on('connect', function () {
        socket.emit('joined', {});
    });
    socket.on('status', function (data) {
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
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
            socket.emit('text', { msg: text });
        }
    });



    
});
function leave_room() {
    socket.emit('left', {}, function () {
        socket.disconnect();

        // go back to the login page
        window.location.href = "{{ url_for('main.index') }}";
    });
}