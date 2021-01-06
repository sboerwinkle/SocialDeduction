{% include "components/main.js" %}

var roles_list;
var balance;


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
        balance = data.balance;
        document.getElementById('balance-text').innerHTML = "Expected balance: " + balance[0].toString() + " Good, " + balance[1].toString() + " Evil."

        // displays checkboxes for all the roles
        var roles = function () {
            var role_picker = document.getElementById('role-picker');
            role_picker.innerHTML = "";

            for (var role_name in roles_list) {
                var role_item = '<li>';
                role_item += role_name;
                for (var x = 0; x < roles_list[role_name].Number; x++) {
                    // name the item for input detection/syncing
                    role_item += "<input type=\"checkbox\"";
                    role_item += 'id="' + role_name + x.toString() + '" ';
                    role_item += 'name="' + role_name + '"';
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
            $("#view-planning [id='" + data.id + "']").prop('checked', data.value);
        }
    });

    // event handlers (sockets to)
    // checkboxes
    $(document).on("change", '#view-planning :checkbox', function () {
        var message = {
            room: room_id,
            type: "checkbox",
            id: this.id,
            value: this.checked
        };
        socket.emit("v1_select_change", message);
    });
    // end view 1


});


// view 1 submit
function finish_planning(){

    // grab roles
    var checked_boxes = $('#role-picker :checked');

    // basic check -> correct amount
    if(checked_boxes.length < (balance[0]+balance[1])){
        alert("You do not have enough characters selected!");
        return;
    } else if(checked_boxes.length > (balance[0]+balance[1])){
        alert("Yo have too many characters selected!");
        return;
    }

    var roles = [];
    var num_good = 0;
    var num_evil = 0;
    for(var i = 0; i < checked_boxes.length; i++){
        var name = checked_boxes[i].name;
        roles.push(name)

        if(roles_list[name].team == "Good"){
            num_good ++;
        } else {
            num_evil ++;
        }
    }

    // medium check -> must have at least 1 good or 1 evil
    if(num_good == 0){
        alert("You must have at least 1 good character!");
        return;
    }
    else if(num_evil == 0){
        alert("You must have at least 1 evil character!");
        return;
    }

    // final check -> match guidelines
    if(num_good != balance[0] || num_evil != balance[1]){
        alert("Your good/evil ratio does not match the expected ratio.");
        return;
    }

    // emit info to server now.
}