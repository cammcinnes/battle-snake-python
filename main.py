# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "cammcinnes",  # TODO: Your Battlesnake Username
        "color": "#000000",  # TODO: Choose color
        "head": "pixel",  # TODO: Choose head
        "tail": "pixel",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


def game_state_to_matrix(game_state: typing.Dict):
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]
    opponents = game_state['board']['snakes']

    # Initialize the matrix with 1s (empty spaces)
    matrix = [[1 for _ in range(width)] for _ in range(height)]

    # Mark the positions of the snakes
    for snake in opponents:
        for segment in snake['body']:
            x, y = segment['x'], segment['y']
            matrix[y][x] = 0  # Mark the snake positions with 0
    # Mark heads on the snakes
    for snake in opponents:
        head_x, head_y = snake['head']['x'], snake['head']['y']
        if snake['length'] > game_state["you"]['length']:
            matrix[head_y][head_x] = -1  # Mark heads on the snakes with -1
        else:
            matrix[head_y][head_x] = 1

    # Mark the position of your own snake
    my_body = game_state["you"]["body"]
    for segment in my_body:
        x, y = segment['x'], segment['y']
        matrix[y][x] = 0  # Mark the snake positions with 0

    return matrix


def flood_recursive(x, y, weight, matrix, e_dist):
    if y < 0 or y >= len(matrix) or x < 0 or x >= len(matrix[0]):
        return weight
    if matrix[y][x] == 0:
        return weight
    if matrix[y][x] == -1:
        if e_dist <= 2:
            return weight - 100
        else:
            return weight - 10

    matrix[y][x] = 0  # Mark the cell as visited by setting it to 0
    weight += 1  # Increment the weight
    e_dist += 1  #Increment enemy distance
    # Recursively call for all 4 directions
    weight = flood_recursive(x, y - 1, weight, matrix, e_dist)
    weight = flood_recursive(x, y + 1, weight, matrix, e_dist)
    weight = flood_recursive(x - 1, y, weight, matrix, e_dist)
    weight = flood_recursive(x + 1, y, weight, matrix, e_dist)

    return weight


def choose_next_move(move_weight):
    final_move = ""
    final_move_weight = -float(
        'inf')  # Set to negative infinity to ensure any move_weight is larger

    for move, weight in move_weight.items():
        if weight > final_move_weight:
            final_move = move
            final_move_weight = weight
        elif weight == final_move_weight:
            list = [{
                "dir": final_move,
                "w": final_move_weight
            }, {
                "dir": move,
                "w": weight
            }]
            random.shuffle(list)
            final_move = list[0]["dir"]
            final_move_weight = list[0]["w"]

    # Choose a default move if no final_move is selected
    if final_move == "":
        next_move = "up"
    else:
        next_move = final_move

    return next_move


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    move_weight = {"up": 1, "down": 1, "left": 1, "right": 1}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        move_weight["left"] = 0
    elif my_neck["x"] > my_head[
            "x"]:  # Neck is right of head, don't move right
        move_weight["right"] = 0
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        move_weight["down"] = 0
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        move_weight["up"] = 0

    # Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == (board_width - 1):  # right side of screen
        move_weight["right"] = 0
    if my_head["x"] == 0:  # left side of screen
        move_weight["left"] = 0
    if my_head["y"] == (board_height - 1):  # top side of screen
        move_weight["up"] = 0
    if my_head["y"] == 0:  # bottom side of screen
        move_weight["down"] = 0

    # Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    for a in my_body:
        if a["x"] == (my_head["x"] -
                      1) and my_head["y"] == a["y"]:  # left side body
            move_weight["left"] = 0
        if my_head["x"] == (a["x"] - 1) and my_head["y"] == a["y"]:
            move_weight["right"] = 0
        if my_head["y"] == (a["y"] - 1) and my_head["x"] == a["x"]:
            move_weight["up"] = 0
        if a["y"] == (my_head["y"] - 1) and my_head["x"] == a["x"]:
            move_weight["down"] = 0

    # Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for opponent in opponents:
        for segment in opponent['body']:
            if segment['x'] == my_head["x"] + 1 and segment['y'] == my_head[
                    "y"]:
                move_weight["right"] = 0
            if segment['x'] == my_head["x"] - 1 and segment['y'] == my_head[
                    "y"]:
                move_weight["left"] = 0
            if segment['x'] == my_head['x'] and segment[
                    'y'] == my_head["y"] - 1:
                move_weight["down"] = 0
            if segment['x'] == my_head['x'] and segment[
                    'y'] == my_head["y"] + 1:
                move_weight["up"] = 0

    #TODO: Prevent battlesnake from doing headon collisions in corners

    # Flood fill weights
    if move_weight["left"] != 0:
        matrix = game_state_to_matrix(game_state)
        move_weight["left"] = flood_recursive(my_head["x"] - 1, my_head["y"],
                                              0, matrix, 0)
    if move_weight["right"] != 0:
        matrix = game_state_to_matrix(game_state)
        move_weight["right"] = flood_recursive(my_head["x"] + 1, my_head["y"],
                                               0, matrix, 0)
    if move_weight["up"] != 0:
        matrix = game_state_to_matrix(game_state)
        move_weight["up"] = flood_recursive(my_head["x"], my_head["y"] + 1, 0,
                                            matrix, 0)
    if move_weight["down"] != 0:
        matrix = game_state_to_matrix(game_state)
        move_weight["down"] = flood_recursive(my_head["x"], my_head["y"] - 1,
                                              0, matrix, 0)

    # Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    health = game_state['you']['health']
    for f in food:
        if f['x'] == my_head["x"] + 1 and f['y'] == my_head["y"]:
            move_weight[
                "right"] += 10  # Arbitrary high value to prioritize food
        if f['x'] == my_head["x"] - 1 and f['y'] == my_head["y"]:
            move_weight["left"] += 10
        if f['x'] == my_head['x'] and f['y'] == my_head["y"] - 1:
            move_weight["down"] += 10
        if f['x'] == my_head['x'] and f['y'] == my_head["y"] + 1:
            move_weight["up"] += 10

    next_move = choose_next_move(move_weight)
    print("right:", move_weight["right"])
    print("left:", move_weight["left"])
    print("up:", move_weight["up"])
    print("down:", move_weight["down"])
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
