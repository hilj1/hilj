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
    def __init__(self):
        """
        Инициализирует собранный кубик Рубика.  Внутренне представляет кубик
        как трехмерный массив (список списков списков) ячеек Cubie.
        """
        # Цвета для собранного кубика (U, D, F, B, L, R):
        self.U, self.D, self.F, self.B, self.L, self.R = 'W', 'Y', 'G', 'B', 'O', 'R' #White, Yellow, Green, Blue, Orange, Red

        # Создаем 3x3x3 массив ячеек Cubie
        self.cube = [[[Cubie([self.U, self.D, self.F, self.B, self.L, self.R]) for _ in range(3)] for _ in range(3)] for _ in range(3)]

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
    cube = RubiksCube()
    print("Изначальный кубик:")
    print(cube)

    cube.move('R')
    print("\nПосле хода R:")
    print(cube)

    cube.move("U")
    print("\nПосле хода U:")
    print(cube)