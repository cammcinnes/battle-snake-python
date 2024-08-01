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
from collections import deque as queue

# Direction vectors
dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]



# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "cammcinnes",  # TODO: Your Battlesnake Username
        "color": "#3633FF",  # TODO: Choose color
        "head": "sand-worm",  # TODO: Choose head
        "tail": "pixel",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def floodfill(x, y, matrix, points, width, height):
    if x < 0 or x > width - 1 or y < 0 or y > height - 1 or matrix[x][y] == 1 or matrix[x][y] == 5:
        return points
    
    points +=1
    matrix[x][y] = 1
    
    points = floodfill(x - 1, y, matrix, points, width, height)
    points = floodfill(x + 1, y, matrix, points, width, height)
    points = floodfill(x, y + 1, matrix, points, width, height)
    points = floodfill(x, y - 1, matrix, points, width, height)
    return points
    
def mapping(game_state: typing.Dict):
    snakes = game_state['board']['snakes']
    width = game_state['board']['width']
    height = game_state['board']['height']
    foodlist = game_state['board']['food']
    
    matrix = [[0 for _ in range(height)] for _ in range(width)]
    
    for snake in snakes:
        body = snake['body']
        head = snake['head']
        counter = 0
        for body_part in body:
            x,y = body_part['x'], body_part['y']
            if counter == 0:
                matrix[x][y] = 5
            else:
                matrix[x][y] = 1
            counter +=1
    
    for food in foodlist:
        x,y = food['x'], food['y']
        matrix[x][y] = 2
    
    
    return matrix
 
def isValid(visited, x, y):
   
    # If cell lies out of bounds
    if x < 0 or y < 0 or x >= 10 or y >= 10 or visited[x][y] == 1:
        return False
 
    # If cell is already visited
    if visited[x][y] == 3:
        return False
 
    # Otherwise
    return True
 
# Function to perform the BFS traversal
def BFS(visited, a, b):
   
    # Stores indices of the matrix cells
    q = queue()
 
    # Mark the starting cell as visited
    # and push it into the queue
    q.append(( a, b ))
    visited[a][b] = 3
 
    # Iterate while the queue
    # is not empty
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        
        visited[x][y] = 3
        # Go to the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if isValid(visited, adjx, adjy):
                if visited[adjx][adjy] == 2:
                    print (adjx, adjy)
                    return (adjx, adjy)
                q.append((adjx, adjy))
                
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    move_points = {"up": 10, "down": 10, "left": 10, "right": 10}
    moves = ["up", "down", "left", "right"]

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_body = game_state["you"]["body"]

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        move_points["left"] = 0

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        move_points["right"] = 0

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        move_points["down"] = 0

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        move_points["up"] = 0
        
#     # Food Sensing
#     food_list = game_state['board']['food']
#     health = game_state['you']['health']
#     if health < 10:
#         for food_piece in food_list:
#             # Check left side
#             if my_head['x'] - 1 == food_piece['x'] and my_head['y'] == food_piece['y']:
#                 move_points['left'] += 10
                
#             # Check right side
#             if my_head['x'] + 1 == food_piece['x'] and my_head['y'] == food_piece['y']:
#                 move_points['right'] += 10
#             # Check top side
#             if my_head['x'] == food_piece['x'] and my_head['y'] + 1 == food_piece['y']:
#                 move_points['up'] += 10

#             # Check bottom side
#             if my_head['x'] == food_piece['x'] and my_head['y'] - 1 == food_piece['y']:
#                 move_points['down'] += 10
#     else:
#             for food_piece in food_list:
#                 # Check left side
#                 if my_head['x'] - 1 == food_piece['x'] and my_head['y'] == food_piece['y']:
#                     move_points['left'] -= 5  
#                 # Check right side
#                 if my_head['x'] + 1 == food_piece['x'] and my_head['y'] == food_piece['y']:
#                     move_points['right'] -= 5
#                 # Check top side
#                 if my_head['x'] == food_piece['x'] and my_head['y'] + 1 == food_piece['y']:
#                     move_points['up'] -= 5
#                 # Check bottom side
#                 if my_head['x'] == food_piece['x'] and my_head['y'] - 1 == food_piece['y']:
#                     move_points['down'] -= 5

    # Snake Boundary Code
    width = game_state['board']['width']
    height = game_state['board']['height']
    
    # Right Boundary
    if my_head['x'] == width - 1:
        move_points['right'] = 0
    # Left Boundary
    if my_head['x'] == 0:
        move_points['left'] = 0
    # Top Boundary
    if my_head['y'] == height - 1:
        move_points['up'] = 0
    # Bottom Boundary
    if my_head['y'] == 0:
        move_points['down'] = 0
        
    # Snake Self Collision Barrier
    
    for body_part in my_body:
        # Check left side
        if my_head['x'] - 1 == body_part['x'] and my_head['y'] == body_part['y']:
            move_points['left'] = 0
        # Check right side
        if my_head['x'] + 1 == body_part['x'] and my_head['y'] == body_part['y']:
            move_points['right'] = 0
        # Check top side
        if my_head['x'] == body_part['x'] and my_head['y'] + 1 == body_part['y']:
            move_points['up'] = 0
        # Check bottom side
        if my_head['x'] == body_part['x'] and my_head['y'] - 1 == body_part['y']:
            move_points['down'] = 0
    # Snake vs Snake Collision avoider
    
    snakes = game_state['board']['snakes']
    
    for snake in snakes:
        enemy_body = snake['body']
        for body_part in enemy_body:
            # Check left side
            if my_head['x'] - 1 == body_part['x'] and my_head['y'] == body_part['y']:
                move_points['left'] = 0
            # Check right side
            if my_head['x'] + 1 == body_part['x'] and my_head['y'] == body_part['y']:
                move_points['right'] = 0
            # Check top side
            if my_head['x'] == body_part['x'] and my_head['y'] + 1 == body_part['y']:
                move_points['up'] = 0
                
            # Check bottom side
            if my_head['x'] == body_part['x'] and my_head['y'] - 1 == body_part['y']:
                move_points['down'] = 0
    
    # BFS for food
    matrix = mapping(game_state)
    nearest_food = BFS(matrix, my_head['x'], my_head['y'])
    health = game_state['you']['health']
    
    if nearest_food != None:
        if health < 99:
            if nearest_food[0] > my_head['x']:
                move_points['right'] += 10
            elif nearest_food[0] < my_head['x']:
                move_points['left'] += 10
            elif nearest_food[1] > my_head['y']:
                move_points['up'] += 10
            elif nearest_food[1] < my_head['y']:
                move_points['down'] += 10
        else:
            if nearest_food[0] > my_head['x']:
                move_points['right'] -= 5
            elif nearest_food[0] < my_head['x']:
                move_points['left'] -= 5
            elif nearest_food[1] > my_head['y']:
                move_points['up'] -= 5
            elif nearest_food[1] < my_head['y']:
                move_points['down'] -= 5

    # Flood Fill Code
    
    x = my_head['x']
    y = my_head['y']
    
    # Left
    if move_points['left'] != 0:
        matrix = mapping(game_state)
        move_points['left'] += floodfill(x - 1, y, matrix, 0, width, height)
    # Right
    if move_points['right'] != 0:
        matrix = mapping(game_state)
        move_points['right'] += floodfill(x + 1, y, matrix, 0, width, height)
    # Up
    if move_points['up'] != 0:
        matrix = mapping(game_state)
        move_points['up'] += floodfill(x, y + 1, matrix, 0, width, height)
    # Down
    if move_points['down'] != 0:
        matrix = mapping(game_state)
        move_points['down'] += floodfill(x, y - 1, matrix, 0, width, height)
        
    # Compare all of the moves to create a list of all moves with the highest score
    best_moves = []
    for move, points in move_points.items():
        if len(best_moves) == 0:
            best_moves.append(move)
        else:
            for good_move in best_moves:
                if points > move_points[good_move]:
                    best_moves.clear()
                    best_moves.append(move)
                elif points == move_points[good_move]:
                    best_moves.append(move)
                    break
                    
    # Choose a random move from the best choices
    next_move = random.choice(best_moves)
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    print(f"MOVE {game_state['turn']} POINTS: UP - {move_points['up']}, DOWN - {move_points['down']}, LEFT - {move_points['left']}, RIGHT - {move_points['right']}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
