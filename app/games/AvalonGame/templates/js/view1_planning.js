// view 1
$(document).ready(function () {
    // TODO: Perhaps only game host can edit?

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
function finish_planning() {

    // grab roles
    var checked_boxes = $('#role-picker :checked');

    // basic check -> correct amount
    if (checked_boxes.length < (balance[0] + balance[1])) {
        alert("You do not have enough characters selected!");
        return;
    } else if (checked_boxes.length > (balance[0] + balance[1])) {
        alert("Yo have too many characters selected!");
        return;
    }

    var roles = [];
    var num_good = 0;
    var num_evil = 0;
    for (var i = 0; i < checked_boxes.length; i++) {
        var name = checked_boxes[i].name;
        roles.push(name)

        if (roles_list[name].Team == "Good") {
            num_good++;
        } else {
            num_evil++;
        }
    }

    // medium check -> must have at least 1 good or 1 evil
    if (num_good == 0) {
        alert("You must have at least 1 good character!");
        return;
    }
    else if (num_evil == 0) {
        alert("You must have at least 1 evil character!");
        return;
    }

    // final check -> match guidelines
    if (num_good != balance[0] || num_evil != balance[1]) {
        alert("Your good/evil ratio does not match the expected ratio.");
        return;
    }

    // emit info to server now.
    socket.emit("v1_finish", { room: room_id, roles: roles });
}