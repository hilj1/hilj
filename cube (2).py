import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import random
import sys
import time

# Размер кубика (3x3x3)
cube_size = 3

# Цвета граней
colors = {
    'F': 'green',  # Front
    'B': 'blue',   # Back
    'U': 'white',  # Up
    'D': 'yellow',  # Down
    'L': 'orange',  # Left
    'R': 'red'     # Right
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

# Отключаем оси
ax.axis('off')

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
        [vertices[1], vertices[2], vertices[6], vertices[5]]   # Right
    ]
    return faces

# Отрисовка кубика
def draw_cube():
    global polygons
    ax.clear()
    ax.set_xlim([0, cube_size])
    ax.set_ylim([0, cube_size])
    ax.set_zlim([0, cube_size])
    ax.axis('off')
    polygons = []
    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                if x == 0 or x == cube_size - 1 or y == 0 or y == cube_size - 1 or z == 0 or z == cube_size - 1:
                    faces = create_cube_faces(x, y, z)
                    for i, (face, color) in enumerate(zip(faces, list(cubes[x, y, z].values()))):
                        poly = Poly3DCollection([face], color=color, linewidths=1, edgecolors='k', alpha=0.7)
                        ax.add_collection3d(poly)

    # Убираем метки осей, так как сами оси отключены
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')

    plt.draw()
    plt.pause(0.01)

# Вращение слоя
def rotate_layer(layer, axis, direction):
    if axis == 'x':
        # Вращение слоя вокруг оси X
        if direction == 'cw':
            temp = np.rot90(cubes[layer, :, :].copy(), k=1, axes=(1, 0))
        else:
            temp = np.rot90(cubes[layer, :, :].copy(), k=3, axes=(1, 0))
        cubes[layer, :, :] = temp

        for i in range(cube_size):
            for j in range(cube_size):
                if direction == 'cw':
                    cubes[layer, i, j]['U'], cubes[layer, i, j]['F'], cubes[layer, i, j]['D'], cubes[layer, i, j]['B'] = \
                        cubes[layer, i, j]['F'], cubes[layer, i, j]['D'], cubes[layer, i, j]['B'], cubes[layer, i, j]['U']
                else:
                    cubes[layer, i, j]['U'], cubes[layer, i, j]['F'], cubes[layer, i, j]['D'], cubes[layer, i, j]['B'] = \
                        cubes[layer, i, j]['B'], cubes[layer, i, j]['U'], cubes[layer, i, j]['F'], cubes[layer, i, j]['D']

    elif axis == 'y':
        # Вращение слоя вокруг оси Y
        if direction == 'cw':
            temp = np.rot90(cubes[:, layer, :].copy(), k=1, axes=(1, 0))
        else:
            temp = np.rot90(cubes[:, layer, :].copy(), k=3, axes=(1, 0))
        cubes[:, layer, :] = temp

        for i in range(cube_size):
            for j in range(cube_size):
                if direction == 'cw':
                    cubes[i, layer, j]['F'], cubes[i, layer, j]['R'], cubes[i, layer, j]['B'], cubes[i, layer, j]['L'] = \
                        cubes[i, layer, j]['R'], cubes[i, layer, j]['B'], cubes[i, layer, j]['L'], cubes[i, layer, j]['F']
                else:
                    cubes[i, layer, j]['F'], cubes[i, layer, j]['R'], cubes[i, layer, j]['B'], cubes[i, layer, j]['L'] = \
                        cubes[i, layer, j]['L'], cubes[i, layer, j]['F'], cubes[i, layer, j]['R'], cubes[i, layer, j]['B']

    elif axis == 'z':
        # Вращение слоя вокруг оси Z
        if direction == 'cw':
            temp = np.rot90(cubes[:, :, layer].copy(), k=1, axes=(1, 0))
        else:
            temp = np.rot90(cubes[:, :, layer].copy(), k=3, axes=(1, 0))
        cubes[:, :, layer] = temp

        for i in range(cube_size):
            for j in range(cube_size):
                if direction == 'cw':
                    cubes[i, j, layer]['U'], cubes[i, j, layer]['R'], cubes[i, j, layer]['D'], cubes[i, j, layer]['L'] = \
                        cubes[i, j, layer]['L'], cubes[i, j, layer]['U'], cubes[i, j, layer]['R'], cubes[i, j, layer]['D']
                else:
                    cubes[i, j, layer]['U'], cubes[i, j, layer]['R'], cubes[i, j, layer]['D'], cubes[i, j, layer]['L'] = \
                        cubes[i, j, layer]['R'], cubes[i, j, layer]['D'], cubes[i, j, layer]['L'], cubes[i, j, layer]['U']

    draw_cube()

# Анимация вращения слоя
def animate_rotation(layer, axis, direction):
    rotate_layer(layer, axis, direction)
    draw_cube()

# Случайная сборка кубика
def random_scramble():
    moves = ['U', 'D', 'L', 'R', 'F', 'B']
    directions = ['cw', 'ccw']
    for _ in range(30):  # Перемешивание с 30 случайными движениями
        face = random.choice(moves)
        direction = random.choice(directions)
        animate_rotation(0, face.lower(), direction)

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
    elif event.key == '1':  # Вращение U
        animate_rotation(0, 'y', 'cw')
        moves.append('U cw')
    elif event.key == '2':  # Вращение D
        animate_rotation(cube_size - 1, 'y', 'ccw')
        moves.append('D ccw')
    elif event.key == '3':  # Вращение L
        animate_rotation(0, 'x', 'cw')
        moves.append('L cw')
    elif event.key == '4':  # Вращение R
        animate_rotation(cube_size - 1, 'x', 'ccw')
        moves.append('R ccw')
    elif event.key == '5':  # Вращение F
        animate_rotation(0, 'z', 'cw')
        moves.append('F cw')
    elif event.key == '6':  # Вращение B
        animate_rotation(cube_size - 1, 'z', 'ccw')
        moves.append('B ccw')

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
