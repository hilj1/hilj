
import tkinter as tk
from tkinter import Canvas

class Cubie:
    """
    Представляет одну маленькую ячейку (кубик) на кубике Рубика.
    """
    def __init__(self, colors):
        """
        Инициализирует ячейку с заданными цветами на каждой из шести сторон.
        Цвета задаются в виде списка или кортежа, где каждый элемент
        соответствует цвету грани: [верх, низ, перед, зад, лево, право].
        """
        if len(colors) != 6:
            raise ValueError("Ячейка должна иметь цвета для всех 6 граней.")
        self.colors = colors

    def rotate(self, axis, direction):
        """
        Поворачивает ячейку вокруг заданной оси (x, y, или z) в указанном
        направлении (по часовой стрелке или против часовой стрелки).
        Эта функция меняет порядок цветов ячейки в зависимости от поворота.
        """
        if axis == 'x':  # Поворот вокруг оси X (например, для движения R/L)
            if direction == 'clockwise':
                self.colors[0], self.colors[2], self.colors[1], self.colors[3] = \
                    self.colors[2], self.colors[1], self.colors[3], self.colors[0]
            else:  # counterclockwise
                self.colors[0], self.colors[3], self.colors[1], self.colors[2] = \
                    self.colors[3], self.colors[1], self.colors[2], self.colors[0]
        elif axis == 'y':  # Поворот вокруг оси Y (например, для движения U/D)
             if direction == 'clockwise':
                self.colors[2], self.colors[5], self.colors[3], self.colors[4] = \
                    self.colors[5], self.colors[3], self.colors[4], self.colors[2]
             else: #counterclockwise
                 self.colors[2], self.colors[4], self.colors[3], self.colors[5] = \
                     self.colors[4], self.colors[3], self.colors[5], self.colors[2]

        elif axis == 'z':  # Поворот вокруг оси Z (например, для движения F/B)
            if direction == 'clockwise':
                self.colors[0], self.colors[4], self.colors[1], self.colors[5] = \
                    self.colors[4], self.colors[1], self.colors[5], self.colors[0]
            else: #counterclockwise
                self.colors[0], self.colors[5], self.colors[1], self.colors[4] = \
                    self.colors[5], self.colors[1], self.colors[4], self.colors[0]


    def __repr__(self):
        """
        Возвращает строковое представление ячейки для отладки.
        """
        return f"Cubie(colors={self.colors})"



class RubiksCube:
    """
    Представляет кубик Рубика 3x3x3.
    """
    def __init__(self, canvas, x_offset, y_offset, cubie_size):
        """
        Инициализирует собранный кубик Рубика.  Внутренне представляет кубик
        как трехмерный массив (список списков списков) ячеек Cubie.
        """
        # Цвета для собранного кубика (U, D, F, B, L, R):
        self.U, self.D, self.F, self.B, self.L, self.R = 'white', 'yellow', 'green', 'blue', 'orange', 'red'

        # Создаем 3x3x3 массив ячеек Cubie
        self.cube = [[[Cubie([self.U, self.D, self.F, self.B, self.L, self.R]) for _ in range(3)] for _ in range(3)] for _ in range(3)]

        self.canvas = canvas
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.cubie_size = cubie_size

    def move(self, move):
        """
        Выполняет заданный ход на кубике.
        Эта функция должна вызывать соответствующие повороты ячеек
        внутри кубика в зависимости от хода.
        """
        # Примеры ходов:  U (верх), D (низ), F (перед), B (зад), L (лево), R (право)
        # и их обратные ходы: U', D', F', B', L', R'
        if move == 'R': #Rotate Right face clockwise
            for i in range(3):
                for j in range(3):
                    self.cube[i][j][2].rotate('x', 'clockwise')
        elif move == "R'": # Rotate Right face counterclockwise
              for i in range(3):
                for j in range(3):
                    self.cube[i][j][2].rotate('x', 'counterclockwise')
        elif move == "U": # Rotate Upper face clockwise
            for i in range(3):
                for k in range(3):
                    self.cube[0][i][k].rotate('y', 'clockwise')
        elif move == "U'":  # Rotate Upper face counterclockwise
            for i in range(3):
                for k in range(3):
                    self.cube[0][i][k].rotate('y', 'counterclockwise')

        # TODO:  Реализовать остальные ходы.
        self.draw() #redraw the cube after the move

    def draw(self):
        """Отрисовывает кубик на холсте."""
        self.canvas.delete("all")  # Очищаем холст перед перерисовкой

        # Рисуем только переднюю грань, верхнюю и левую для простоты
        for i in range(3):
            for j in range(3):
                # Рисуем переднюю грань
                x1 = self.x_offset + j * self.cubie_size
                y1 = self.y_offset + i * self.cubie_size
                x2 = x1 + self.cubie_size
                y2 = y1 + self.cubie_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.cube[i][j][0].colors[2], outline="black") #Передняя грань

                #Рисуем верхнюю грань (немного сдвигаем вверх и влево)
                x1_u = self.x_offset + j * self.cubie_size - self.cubie_size/3
                y1_u = self.y_offset + i * self.cubie_size - self.cubie_size/3
                x2_u = x1_u + self.cubie_size
                y2_u = y1_u + self.cubie_size
                self.canvas.create_rectangle(x1_u, y1_u, x2_u, y2_u, fill=self.cube[0][i][j].colors[0], outline="black") #Верхняя грань

                # Рисуем левую грань (сдвигаем влево)
                x1_l = self.x_offset + j * self.cubie_size - self.cubie_size/3 - self.cubie_size
                y1_l = self.y_offset + i * self.cubie_size - self.cubie_size/3
                x2_l = x1_l + self.cubie_size
                y2_l = y1_l + self.cubie_size
                self.canvas.create_rectangle(x1_l, y1_l, x2_l, y2_l, fill=self.cube[i][0][j].colors[4], outline="black") #Левая грань

    def __repr__(self):
        """
        Возвращает строковое представление кубика для отладки.
        """
        cube_str = ""
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cube_str += f"[{i},{j},{k}]: {self.cube[i][j][k]} "
                cube_str += "\n"
        return cube_str


# Пример использования:
if __name__ == '__main__':
    window = tk.Tk()
    window.title("Кубик Рубика")

    canvas_width = 600
    canvas_height = 400
    canvas = Canvas(window, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    cubie_size = 50
    x_offset = 200
    y_offset = 100


    cube = RubiksCube(canvas, x_offset, y_offset, cubie_size)
    cube.draw()

    # Создаем кнопки для выполнения ходов
    button_r = tk.Button(window, text="R", command=lambda: cube.move('R'))
    button_r.pack()

    button_u = tk.Button(window, text="U", command=lambda: cube.move('U'))
    button_u.pack()

    button_r_prime = tk.Button(window, text="R'", command=lambda: cube.move("R'"))
    button_r_prime.pack()

    button_u_prime = tk.Button(window, text="U'", command=lambda: cube.move("U'"))
    button_u_prime.pack()



    window.mainloop()
