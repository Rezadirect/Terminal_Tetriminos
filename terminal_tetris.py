import os
import time
from colorama import Fore
import random
import keyboard

GRID_WIDTH = 28
GRID_HEIGHT = 20

TETROMINOS = {
    'I': [['▊', '▊', '▊', '▊']],
    'O': [['▊', '▊'],
           ['▊', '▊']],
    'T': [['.', '▊', '.'],
           ['▊', '▊', '▊']],
    'J': [['▊', '.', '.'],
           ['▊', '▊', '▊']],
    'L': [['.', '.', '▊'],
           ['▊', '▊', '▊']],
    'S': [['.', '▊', '▊'],
           ['▊', '▊', '.']],
    'Z': [['▊', '▊', '.'],
           ['.', '▊', '▊']]
}

list_lines = [f"{Fore.WHITE}█" for _ in range(GRID_WIDTH * GRID_HEIGHT)]

def random_color():
    return random.choice([Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.GREEN, Fore.CYAN, Fore.MAGENTA])

def reset_grid():
    for i in range(len(list_lines)):
        list_lines[i] = f"{Fore.WHITE}█"

def check_lines(score):
    for y in range(GRID_HEIGHT - 1, -1, -1):
        line_indices = [y * GRID_WIDTH + x for x in range(GRID_WIDTH)]
        if all("▊" in list_lines[i] for i in line_indices):
            for i in line_indices:
                list_lines[i] = f"{Fore.WHITE}█"
            for row in range(y - 1, -1, -1):
                for x in range(GRID_WIDTH):
                    source_index = row * GRID_WIDTH + x
                    target_index = (row + 1) * GRID_WIDTH + x
                    list_lines[target_index] = list_lines[source_index]
                    list_lines[source_index] = f"{Fore.WHITE}█"
                    score += random.randint(100, 500)
            return score
    return score

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def can_place(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell == '▊':
                grid_x = offset_x + x
                grid_y = offset_y + y
                if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT or (grid_y >= 0 and "▊" in list_lines[grid_x + (grid_y * GRID_WIDTH)]):
                    return False
    return True

def place_shape(shape, offset_x, offset_y, block_color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell == '▊':
                grid_x = offset_x + x
                grid_y = offset_y + y
                if grid_y >= 0:
                    list_lines[grid_x + (grid_y * GRID_WIDTH)] = f"{block_color}▊"

def drop_block(x, y, current_shape, block_color, num, Score):
    if can_place(current_shape, x, y + 1):
        y += num
    else:
        place_shape(current_shape, x, y, block_color)
        Score = check_lines(Score)
        current_shape = random.choice(list(TETROMINOS.values()))
        x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
        y = 0
        block_color = random_color()
        if not can_place(current_shape, x, y):
            print("Game over! Exiting...")
            exit()

    return x, y, current_shape, block_color, Score

def handle_input(x, y, current_shape, block_color):
    direction = 0

    if keyboard.is_pressed('left'):
        direction = -1
    if keyboard.is_pressed('right'):
        direction = 1
    if keyboard.is_pressed('down'):
        speed = 10
    else:
        speed = 1
    if keyboard.is_pressed('up'):
        new_shape = rotate(current_shape)
        if can_place(new_shape, x, y):
            current_shape = new_shape

    if direction != 0:
        if can_place(current_shape, x + direction, y):
            x += direction

    return x, y, current_shape, block_color, speed

def display_grid(x, y, current_shape, block_color):
    os.system('cls' if os.name == 'nt' else 'clear')
    temp_lines = list(list_lines)

    # Display falling shape
    for row_offset, row in enumerate(current_shape):
        for col_offset, cell in enumerate(row):
            if cell == '▊':
                temp_lines[(x + col_offset) + ((y + row_offset) * GRID_WIDTH)] = f"{block_color}▊"

    # Determine landing position
    landing_y = get_final_y_position(x, y, current_shape)
    for row_offset, row in enumerate(current_shape):
        for col_offset, cell in enumerate(row):
            if cell == '▊':
                temp_lines[(x + col_offset) + ((landing_y + row_offset) * GRID_WIDTH)] = f"{block_color}▒"

    for i in range(GRID_HEIGHT):
        print(''.join(temp_lines[i * GRID_WIDTH:(i + 1) * GRID_WIDTH]))

def get_final_y_position(x, y, current_shape):
    while can_place(current_shape, x, y + 1):
        y += 1
    return y

def main(Score, counter1, counter2):
    reset_grid()
    current_shape = random.choice(list(TETROMINOS.values()))
    x, y = GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0
    
    block_color = random_color()

    while True:
        # Speed Control
        if counter2 < 4:
            counter1 = 0
        else:
            counter1 = 1
            counter2 = 0
        counter2 += 1
        
        display_grid(x, y, current_shape, block_color)
        print(f"{Fore.YELLOW}Position: x: {x} y: {y}\nScore: {Score}")
        
        x, y, current_shape, block_color, Score = drop_block(x, y, current_shape, block_color, counter1, Score)
        x, y, current_shape, block_color, speed = handle_input(x, y, current_shape, block_color)
        time.sleep(0.05 / speed)

if __name__ == "__main__":
    main(0, 0, 0)
