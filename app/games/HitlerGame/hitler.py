from flask import redirect, render_template, request, session, url_for, flash
from flask_socketio import emit
import uuid
import random

from . import hitler_bp
from ... import socketio
from ...main.forms import LoginForm, NameForm
from ...main import games_db
from ..boardGame import BoardGame

help_text = """Available commands:
   /ls
List non-empty game objects

=== Read / Write ===
   /show [who] [what]
Reveal a value. [who] may be a player prefix, or '_'/'the' for the table.
   /set [who] [what] [value]
Publicly set a value
   /peek [who] [what]
Privately check a value. Others can see you peeking!
   /poke [who] [what] [value]
Privately set a value. Others can see you poking!

=== Deck Manipulation ===
   /draw [num] [who] [what] [who] [what]
Move a number of cards from the top of one deck to another
   /shuffle [who] [what]
Shuffles a deck

=== Secret Hitler stuff ===
   /setup
Sets up the game for the current number of connected players
   /vote [vote]
Set your vote. Votes aren't anonymous, but aren't revealed until everyone's voted.
   /showvote
Reveal and clear each player's 'vote'. Run automatically if everyone votes.
   /discard [x]
Discard the specified card (1-3) from the current 'policies'
   /enact
If there is one policy left, reveals it and pulls from the appropriate policy track.
   /reshuffle
Shuffle the 'discards' into the 'deck'
"""

class Hitler(BoardGame):
    game_name = "Secret Hitler"

    def first_word(self, x):
        ix = x.find(' ')
        if ix == -1:
            if x == '':
                raise Exception("Not enough arguments!")
            return (x, '')
        return (x[:ix], x[ix+1:])

    def input(self, player_name, msg):
        if not msg.startswith("/"):
            self.write(player_name + ": " + msg)
            return
        msg = msg[1:]
        (command, msg) = self.first_word(msg)

        if command == "help":
            self.write(help_text, lambda x: x.name == player_name)
        elif command in ("set", "show", "peek", "poke"):
            (who, msg) = self.first_word(msg)
            (what, msg) = self.first_word(msg)
            who = self.resolve_who(player_name, who)
            privacy = 1 if command in ("peek", "poke") else 0
            if command in ("set", "poke"):
                self.set_value(player_name, privacy, who, what, msg)
            else:
                self.get_value(player_name, privacy, who, what)
        elif command == "ls":
            l = lambda x: x.name == player_name
            self.write("| table", l)
            for k in self.objs:
                self.write("|   " + k, l)
            for p in self.players.values():
                self.write("| " + p.name, l)
                for k in p.objs:
                    self.write("|   " + k, l)
        elif command == "draw":
            (num, msg) = self.first_word(msg)
            (who1, msg) = self.first_word(msg)
            (what1, msg) = self.first_word(msg)
            (who2, msg) = self.first_word(msg)
            (what2, msg) = self.first_word(msg)
            num = int(num)
            who1 = self.resolve_who(player_name, who1)
            who2 = self.resolve_who(player_name, who2)
            who1_str = self.posessive(None, who1, '')
            who2_str = self.posessive(None, who2, '')
            d1 = self.get_deck(who1, what1)
            if len(d1) < num:
                raise Exception(f"Only {len(d1)} cards!")
            d2 = self.get_deck(who2, what2)
            self.set_deck(who2, what2, d1[:num] + d2)
            self.set_deck(who1, what1, d1[num:])
            self.write(f"{player_name} drew {num} cards from {who1_str} {what1} to {who2_str} {what2}")
        elif command == "shuffle":
            (who, msg) = self.first_word(msg)
            (what, msg) = self.first_word(msg)
            who = self.resolve_who(player_name, who)
            who_str = self.posessive(player_name, who, 'their')
            self.write(f"{player_name} shuffled {who_str} {what}")
            d = self.get_deck(who, what)
            random.shuffle(d)
            self.set_deck(who, what, d)
        elif command == "showvote":
            for p in self.players.values():
                if 'vote' in p.objs:
                    self.write(f"{p.name} voted '{p.objs['vote']}'")
                    del p.objs['vote']
                else:
                    self.write(f"{p.name} did not vote.")
        elif command == "discard":
            (num, msg) = self.first_word(msg)
            num = int(num) - 1
            policies = self.get_deck(self, 'policies')
            discards = self.get_deck(self, 'discards')
            discards = [policies[num]] + discards
            policies = policies[:num] + policies[num+1:]
            self.set_deck(self, 'policies', policies)
            self.set_deck(self, 'discards', discards)
            self.write(f"{player_name} discarded a policy...")
        elif command == "reshuffle":
            all_cards = self.get_deck(self, 'deck') + self.get_deck(self, 'discards')
            random.shuffle(all_cards)
            del self.objs['discards']
            self.set_deck(self, 'deck', all_cards)
            self.write(f"{player_name} reshuffled the deck+discards")
        elif command == "vote":
            self.set_value(player_name, 1, self.find_player(player_name), 'vote', msg)
            for p in self.players.values():
                if not ('vote' in p.objs):
                    return
            self.input(player_name, "/showvote")
        elif command == "enact":
            tokens = self.get_deck(self, 'policies')
            if len(tokens) != 1:
                raise Exception(f"Can only /enact with 1 card in the 'policies', currently there are {len(tokens)}")
            if tokens[0] == "F":
                deck = "fascism"
                adjective = "Fascist"
            else:
                deck = "liberalism"
                adjective = "Liberal"
            policies = self.get_deck(self, deck)
            if len(policies) == 0:
                raise Exception("No policies of that type left to enact")
            policy = policies[0]
            self.set_deck(self, deck, policies[1:])
            del self.objs['policies']
            self.write(f"* {player_name} enacted {adjective} policy '{policy}'! Remaining policies:")
            self.write("* " + self.objs.get('liberalism', ''))
            self.write("* " + self.objs.get('fascism', ''))
        elif command == "setup":
            self.write(f"{player_name} set up everything...")
            self.objs = {}
            for p in self.players.values():
                p.objs = {}
            deck = ['L'] * 6 + ['F'] * 11
            random.shuffle(deck)
            self.set_deck(self, 'deck', deck)
            players = len(self.players)
            if players == 1:
                players = 5 # For debugging
            if players < 5 or players > 10:
                self.write(f"Core rules only support 5-10 players! Roles, parties, and the policy tracks are left unset.")
                return
            fascists = (players - 3) // 2
            liberals = players - fascists - 1
            roles = ['Fascist'] * fascists + ['Liberal'] * liberals + ['Hitler']
            random.shuffle(roles)
            party_membership = []
            hitler = "No one???"
            player_list = [y for y in self.players.values()]
            for i in range(len(player_list)):
                p = player_list[i]
                role = roles[i]
                p.objs['role'] = role
                p.objs['party'] = 'Liberals' if role == 'Liberal' else 'Fascists'
                if role == 'Fascist':
                    party_membership.append(p.name)
                elif role == 'Hitler':
                    hitler = p.name
                self.write(f"Your role is '{role}'", lambda x: x.name == p.name)
            if players <= 6:
                self.write(f"Other fascists are: {party_membership}", lambda x: x.name == hitler)
            else:
                self.write("You do not know who the other fascist is.", lambda x: x.name == hitler)
            self.write(f"Fascists are: {party_membership}. Hitler is: {hitler}", lambda x: x.objs['role'] == 'Fascist')
            if players > 8:
                fascism = ['check','check','spec. elect']
            elif players > 6:
                fascism = ['wait','check','spec. elect']
            else:
                fascism = ['wait','wait','peek']
            fascism += ['kill','kill','Fascist Victory!']
            self.set_deck(self, 'fascism', fascism)
            self.set_deck(self, 'liberalism', ['wait', 'wait', 'wait', 'wait', 'Liberal Victory!'])
        else:
            raise Exception(f"Unknown command '/{command}', try '/help'")

    def set_value(self, player_name, privacy, who, what, value):
        if value == '':
            if what in who.objs:
                del who.objs[what]
        else:
            who.objs[what] = value

        if privacy < 2:
            who_str = self.posessive(player_name, who, "their")
            if privacy == 0:
                if value == '':
                    msg = f"{player_name} deleted {who_str} {what}"
                else:
                    msg = f"{player_name} set {who_str} {what} to '{value}'"
            else:
                msg = f"{player_name} set {who_str} {what} in secret"
            self.write(msg)

    def get_value(self, player_name, privacy, who, what):
        if privacy < 2:
            if privacy == 0:
                msg = f"{player_name} revealed:"
            else:
                who_str = self.posessive(player_name, who, "their")
                msg = f"{player_name} peeked at {who_str} {what}"
            self.write(msg)

        value = who.objs.get(what, None)
        if privacy > 0:
            target = lambda x: x.name == player_name
            who_str = self.posessive(player_name, who, "your")
        else:
            target = None
            who_str = self.posessive(None, who, "")
        if value == None:
            self.write(f">>> {who_str} {what} isn't set.", target)
        else:
            self.write(f">>> {who_str} {what} is '{value}'", target)

    # Assumes object is set.
    def get_deck(self, who, what):
        if not (what in who.objs):
            return []
        arr = who.objs[what].split(';')
        if arr[-1] != '':
            raise Exception("Invalid array!")
        return arr[:-1]
    def set_deck(self, who, what, arr):
        value = "".join(x+';' for x in arr)
        if value == "":
            del who.objs[what]
        else:
            who.objs[what] = value

    # Can I not spell?
    def posessive(self, player_name, who, is_player_str):
        if who is self:
            return "the"
        elif who.name == player_name:
            return is_player_str
        else:
            return who.name + "'s"

    def resolve_who(self, player_name, who):
        if who == "_" or who == "the":
            return self
        if who == "my":
            who = player_name;
        return self.find_player(who)


# game route
from flask import session
@hitler_bp.route('/game/hitler/<room_id>',  methods=['GET', 'POST'])
def game_room(room_id):

    if "player_id" not in session:
        session['player_id'] = str(uuid.uuid4())
    
    if "player_name" not in session:
        form = NameForm()
        if form.validate_on_submit():
            session['player_name'] = form.name.data
        elif request.method == 'GET':
            return render_template("name.html", form=form)
    
    game_info = {}
    game_info["room_id"] = room_id
    game_info["player_id"] = session['player_id']
    game_info["player_name"] = session['player_name']
    game_info["game_name"] = Hitler.game_name
    
    return render_template("main.html", game_info=game_info)
