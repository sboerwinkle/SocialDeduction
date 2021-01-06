{% include "components/main.js" %}

$(document).ready(function () {
    var view_planning = document.getElementById("view-planning"); // view 1 planning
    // var view_night_phase = document.getElementById("view-night-phase"); // view 2
    // var view_quest_pick = document.getElementById("view-quest-pick"); // view 3
    // var view_quest_vote = document.getElementById("view-quest-vote"); // view 4
    // var view_questing = document.getElementById("view-questing"); // view 5
    // var view_evil_vote = document.getElementById("view-evil-vote"); // view 6
    // var view_end_game = document.getElementById("view-end-game"); // view 7


    // default hide all screens until needed.
    var hide_all = function () {
        view_planning.style.display = "none";
    }
    hide_all();


    socket.on('game_start', function (data) {
        $('#chat').val($('#chat').val() + "Everyone is Ready! Select the roles to play with!" + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);

        // hide the ready button
        var ready_button = document.getElementById("lobby-ready");
        ready_button.style.display = "none";
        // show lobby list without ready info.
        list(players, false);

        // now we emit the start to the specific game start and the game.js and events will take over.
        socket.emit(game_name + '_ready', { "room": room_id });
    });


    // TODO: Perhaps only game host can edit?
    // view 1
    // socket from
    socket.on('game_planning', function (data) {
        // enable the game planning view.
        hide_all();

        roles_list = data.roles;

        // displays checkboxes for all the roles
        var roles = function () {
            var role_picker = document.getElementById('role-picker');
            role_picker.innerHTML = "";

            for (var i = 0; i < roles_list.length; i++) {
                var role_item = '<li>';
                role_item += roles_list[i].Name;

                for (var x = 0; x < roles_list[i].Number; x++) {
                    // name the item for input detection/syncing
                    role_item += "<input type=\"checkbox\"";
                    role_item += 'name="' + roles_list[i].Name + x.toString() + '"';
                    role_item += ">";
                }

                role_item += "</li>"
                role_picker.innerHTML += role_item;
            }
        }
        roles();
        view_planning.style.display = "block";
    });

    socket.on('v1_select_change', function (data) {
        if (data.type == "checkbox") {
            $("#view-planning [name='" + data.name + "']").prop('checked', data.value);
        }
    });

    // event handlers (sockets to)
    // checkboxes
    $(document).on("change", '#view-planning :checkbox', function () {
        var message = {
            room: room_id,
            type: "checkbox",
            name: this.name,
            value: this.checked
        };
        socket.emit("v1_select_change", message);
    });

    // finish planning.

    // end view 1


});