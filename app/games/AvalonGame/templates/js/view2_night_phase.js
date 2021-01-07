

/* Randomize array in-place using Durstenfeld shuffle algorithm */
function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

var player_dict;


$(document).ready(function () {
    socket.on('v2_night', function (data) {
        // loads the night phase, display roles.
        hide_all();
        view_night_phase.style.display = "block";
        player_dict = data.players;

        // console.log(data.assigned_roles);
        // console.log(data.all_roles);
        // console.log(player_dict);

        var myrole = data.assigned_roles[player_id];
        document.getElementById('role-name').innerHTML = myrole;

        var knowledge = document.getElementById('role-knowledge')

        if(data.all_roles[myrole].Team == "Evil"){
            knowledge.innerHTML = "You are evil.";

            if(myrole == "Oberon"){
                knowledge.innerHTML += "</br>It's Oberon Time!";
                // oberon ends here
            } else {
                // grabs all evil players that are not oberon
                var evil_knowledge = []
                for(var player in data.assigned_roles){
                    // don't know oberon, don't add yourself.
                    if(temp_player_role == "Oberon" || player == player_id){
                        continue
                    }
                    var temp_player_role = data.assigned_roles[player];
                    // evil team don't know oberon
                    if(data.all_roles[temp_player_role].Team == "Evil"){
                        evil_knowledge.push(player_dict[player]);
                    } 
                }
                if(evil_knowledge.length == 0){
                    knowledge.innerHTML += "</br>You are the only evil team member!";
                } else {
                    shuffleArray(evil_knowledge);
                    knowledge.innerHTML += "</br>Your fellow evil doer(s) are: <b>" + evil_knowledge.join(", ") + "</b>."
                }
            }
        } // end evil team
        else {
            knowledge.innerHTML = "You are good.";
            if(myrole == "Loyal Servant of Arthur"){
                knowledge.innerHTML += "</br>May the good team prevail!";
                // end loyal servants
            }
            else if(myrole == "Merlin"){
                var merlin_knowledge = [];
                var has_mordred = false;
                
                for(var player in data.assigned_roles){
                    var temp_player_role = data.assigned_roles[player];
                    // merlin cannot see mordred.
                    if(temp_player_role == "Mordred"){
                        has_mordred = true;
                        continue;
                    }
                    if(data.all_roles[temp_player_role].Team == "Evil"){
                        merlin_knowledge.push(player_dict[player]);
                    }
                }
                if(merlin_knowledge.length == 0){
                    knowledge.innerHTML += "</br>There are no known evil players to you.";
                } else {
                    shuffleArray(merlin_knowledge);
                    knowledge.innerHTML += "</br>You know that <b>" + merlin_knowledge.join(", ") + "</b> belong(s) to evil.";
                }
                if(has_mordred){
                    knowledge.innerHTML += "</br>However, Mordred eludes your vision...";
                }
            } // end merlin

            else if(myrole == "Percival"){
                var percival_knowledge = [];
                var has_morgana = false;
                var has_merlin = false;
                
                for(var player in data.assigned_roles){
                    var temp_player_role = data.assigned_roles[player];
                    if(temp_player_role == "Morgana"){
                        has_morgana = true;
                        percival_knowledge.push(player_dict[player])
                    }
                    else if(temp_player_role == "Merlin"){
                        has_merlin = true;
                        percival_knowledge.push(player_dict[player])
                    }
                }
                if(has_morgana && has_merlin){
                    shuffleArray(percival_knowledge);
                    knowledge.innerHTML += "</br>You know that <b>" + percival_knowledge.join(", ") + "</b> is Merlin and Morgana.";
                    knowledge.innerHTML += "</br>However, you are unsure who is who!";
                }
                else if(has_morgana){
                    knowledge.innerHTML += "</br>You know that <b>" + percival_knowledge[0] + "</b> is Morgana, an evil witch!";
                }
                else if(has_merlin){
                    knowledge.innerHTML += "</br>You know that <b>" + percival_knowledge[0] + "</b> is Merlin, your close ally!";
                }
                else{
                    knowledge.innerHTML += "</br>You are basically a generic good.";
                }
            }
        }
    });

});