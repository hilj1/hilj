import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import sys
import time
import os

# Размер кубика (3x3x3)
cube_size = 3

# Цвета граней
colors = {
    'F': 'green',  # Front
    'B': 'blue',  # Back
    'U': 'white',  # Up
    'D': 'yellow',  # Down
    'L': 'orange',  # Left
    'R': 'red'  # Right
}

# Инициализация кубика
def initialize_cube():
    return np.array([[[{face: colors[face] for face in colors}
                       for z in range(cube_size)]
                       for y in range(cube_size)]
                       for x in range(cube_size)])

cubes = initialize_cube()

# Создаем фигуру и ось
fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(projection='3d')
ax.set_xlim([0, cube_size])
ax.set_ylim([0, cube_size])
ax.set_zlim([0, cube_size])
polygons = []

# Создание граней маленького кубика
def create_cube_faces(x, y, z):
    vertices = np.array([[x, y, z],
                         [x + 1, y, z],
                         [x + 1, y + 1, z],
                         [x, y + 1, z],
                         [x, y, z + 1],
                         [x + 1, y, z + 1],
                         [x + 1, y + 1, z + 1],
                         [x, y + 1, z + 1]])

    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Front
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Back
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Bottom
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Top
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left
        [vertices[1], vertices[2], vertices[6], vertices[5]]  # Right
    ]
    return faces

# Отрисовка кубика
def draw_cube():
    global polygons
    ax.clear()
    ax.set_xlim([0, cube_size])
    ax.set_ylim([0, cube_size])
    ax.set_zlim([0, cube_size])
    polygons = []
    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                faces = create_cube_faces(x, y, z)
                for i, (face, color) in enumerate(zip(faces, list(cubes[x, y, z].values()))):
                    poly = Poly3DCollection([face], color=color, linewidths=1, edgecolors='k', alpha=0.7)
                    ax.add_collection3d(poly)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.draw()
    plt.pause(0.01)

# Вращение слоя
def rotate_layer(face, direction):
    if face == 'U':
        layer_index = 0
        axis = 2
    elif face == 'D':
        layer_index = cube_size - 1
        axis = 2
    elif face == 'L':
        layer_index = 0
        axis = 0
    elif face == 'R':
        layer_index = cube_size - 1
        axis = 0
    elif face == 'F':
        layer_index = 0
        axis = 1
    elif face == 'B':
        layer_index = cube_size - 1
        axis = 1

    if direction == 'cw':
        k = 1
    else:
        k = -1

    new_cubes = cubes.copy()

    if axis == 2:  # U, D
        new_cubes[:, :, layer_index] = np.rot90(cubes[:, :, layer_index], k=k)
    elif axis == 0:  # L, R
        new_cubes[layer_index, :, :] = np.rot90(cubes[layer_index, :, :], k=k)
    elif axis == 1:  # F, B
        new_cubes[:, layer_index, :] = np.rot90(cubes[:, layer_index, :], k=k)
    
    if face == 'U':
        for i in range(cube_size):
            for j in range(cube_size):
                cubes[i,j,0] = new_cubes[i,j,0]
    elif face == 'D':
        for i in range(cube_size):
            for j in range(cube_size):
                cubes[i,j,cube_size-1] = new_cubes[i,j,cube_size-1]
    elif face == 'L':
        for i in range(cube_size):
            for j in range(cube_size):
                cubes[0,i,j] = new_cubes[0,i,j]
    elif face == 'R':
        for i in range(cube_size):
            for j in range(cube_size):
                cubes[cube_size-1,i,j] = new_cubes[cube_size-1,i,j]
    elif face == 'F':
        for i in range(cube_size):
            for j in range(cube_size):
                cubes[i,0,j] = new_cubes[i,0,j]
    elif face == 'B':
        for i in range(cube_size):
            for j in range(cube_size):
                cubes[i,cube_size-1,j] = new_cubes[i,cube_size-1,j]
    

    draw_cube()

# Анимация вращения слоя
def animate_rotation(face, direction):
    rotate_layer(face, direction)
    draw_cube()
    plt.pause(0.1)

# Случайная сборка кубика
def random_scramble():
    moves = ['U', 'D', 'L', 'R', 'F', 'B']
    directions = ['cw', 'ccw']
    for _ in range(30):  # Перемешивание с 30 случайными движениями
        face = random.choice(moves)
        direction = random.choice(directions)
        animate_rotation(face, direction)

# Сброс кубика
def reset_cube():
    global cubes
    cubes = initialize_cube()
    draw_cube()

# Регистрация игрока
def register_player():
    player_name = input("Пожалуйста, введите ваше имя: ")
    return player_name

# Обработка событий клавиатуры
def on_key(event):
    global player_name, start_time, moves

    if event.key == 'r':  # Сброс кубика
        reset_cube()
        moves = []
    elif event.key == 's':  # Перемешивание
        random_scramble()
        start_time = time.time()
        moves = []
    else:
        key = event.key.lower()
        if key in ['u', 'd', 'l', 'r', 'f', 'b']:
            direction = 'cw' if key in ['u', 'l', 'f'] else 'ccw'
            face = key.upper()
            animate_rotation(face, direction)
            moves.append(face + ' ' + direction)

# Добавление меню
def create_menu():
    reset_button_ax = plt.axes([0.1, 0.02, 0.2, 0.075])
    reset_button = Button(reset_button_ax, 'Сброс')
    reset_button.on_clicked(lambda event: reset_cube())

    scramble_button_ax = plt.axes([0.4, 0.02, 0.2, 0.075])
    scramble_button = Button(scramble_button_ax, 'Сборка')
    scramble_button.on_clicked(lambda event: random_scramble())

    exit_button_ax = plt.axes([0.7, 0.02, 0.2, 0.075])
    exit_button = Button(exit_button_ax, 'Выход')
    exit_button.on_clicked(lambda event: sys.exit())

# Запись данных в файл
def record_game(player_name, time_taken, moves):
    filename = f"{player_name}_cube_games.txt"
    with open(filename, 'a') as file:
        file.write(f"Имя игрока: {player_name}\n")
        file.write(f"Время сборки: {time_taken:.2f} секунд\n")
        file.write(f"Комбинации: {', '.join(moves)}\n")
        file.write("---\n")

# Запуск приложения
player_name = register_player()
start_time = 0
moves = []
fig.canvas.mpl_connect('key_press_event', on_key)
create_menu()
reset_cube()
plt.show()

if start_time != 0:
    end_time = time.time()
    time_taken = end_time - start_time
    record_game(player_name, time_taken, moves)
