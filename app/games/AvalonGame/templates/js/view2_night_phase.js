
$(document).ready(function () {
    socket.on('v2_night', function (data) {
        // loads the night phase, display roles.
        hide_all();
        view_night_phase.style.display = "block";

        console.log(data.assigned_roles)
    });

});