from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def reversed_path(directions):
    # אם אין כיוון תחזיר כלום
    if directions is None:
        return None
    # ליסט לכל הדרכים האפשריות
    potential_path = ["n", "e", "s", "w"]
    # תחזיר אינדקס של הפט
    return potential_path[(potential_path.index(directions) + 2) % 4]


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# אינישילייזד
previous_path = []
possible_path = {}
# אפנד את הפאט לחדר ההעכשוי
previous_path.append((player.current_room, None, None, 0))
# בזמן שהאורך של הפאט גדול מ 0 תוסיף את הורטקס לפאט הקודם
while len(previous_path) > 0:
    node = previous_path[-1]
    room = node[0]
    last_path = node[1]
# אם האיידי של חדר לא בדרך אפשרית תוסיף את זה לליסט
    if room.id not in possible_path:
        possible_path[room.id] = set()
# אם הפאט האחרון לא לא תוסיף תוסיף את איידי חדר ל דרך האחרונה
    if last_path is not None:
        possible_path[room.id].add(last_path)
# אם האורך של דרך אפשרית שווה לאורך של הגרף ברייק אוף דה לופ
    if len(possible_path) == len(room_graph):
        break
# תבדוק את היציאות מהחדר אם יש וזה לא בליסט שלנו תוסיף לליסט
    room_exists = room.get_exits()
    possible_exists = [
        i for i in room_exists if i not in possible_path[room.id]]
# אם האורך של החדרים האפשריים גדול מ0 רנדומייז דיירקשן גט את החדר בדיירקשן תוסיף לפט הקודם אחרת תוסיף דרך אחרונה ופופ
    if len(possible_exists) > 0:

        direction = random.choice(possible_exists)
        room_to = room.get_room_in_direction(direction)
        possible_path[room.id].add(direction)
        previous_path.append((room_to, reversed_path(direction)))
        traversal_path.append(direction)
    else:
        traversal_path.append(last_path)
        previous_path.pop(-1)


for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
