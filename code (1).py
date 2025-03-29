import sys
from PySide2.QtWidgets import QApplication, QOpenGLWidget
from PySide2.QtCore import Qt, QTimer, QPoint
from PySide2.QtGui import QKeyEvent, QMouseEvent
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# import numpy as np

class RubiksCubeWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.rotation_x = 20
        self.rotation_y = 45
        self.cube = RubiksCube()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # 60 FPS

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -6.0)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # Отрисовка кубика Рубика
        self.cube.draw()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.text().upper()
        if key in ['U', 'D', 'L', 'R', 'F', 'B']:
            self.cube.rotate_face(key)
            self.update()

class RubiksCube:
    def __init__(self):
        # Инициализация кубика Рубика
        self.cubies = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    self.cubies.append(Cubie(x, y, z))

    def draw(self):
        for cubie in self.cubies:
            cubie.draw()

    def rotate_face(self, face):
        # Вращение грани кубика
        for cubie in self.cubies:
            if face == 'U' and cubie.y == 1:
                cubie.rotate(0, 1, 0)
            elif face == 'D' and cubie.y == -1:
                cubie.rotate(0, -1, 0)
            elif face == 'L' and cubie.x == -1:
                cubie.rotate(-1, 0, 0)
            elif face == 'R' and cubie.x == 1:
                cubie.rotate(1, 0, 0)
            elif face == 'F' and cubie.z == 1:
                cubie.rotate(0, 0, 1)
            elif face == 'B' and cubie.z == -1:
                cubie.rotate(0, 0, -1)

class Cubie:
    def __init__(self, x, y, z):
        self.position = np.array([x, y, z], dtype=float)
        self.colors = self._get_colors(x, y, z)

    def _get_colors(self, x, y, z):
        # Определение цветов для каждой грани
        colors = {
            'front': [0, 0, 1],  # Синий
            'back': [0, 1, 0],   # Зеленый
            'left': [1, 0.5, 0],  # Оранжевый
            'right': [1, 0, 0],   # Красный
            'up': [1, 1, 1],      # Белый
            'down': [1, 1, 0],   # Желтый
        }
        active_faces = []
        if z == 1:
            active_faces.append('front')
        if z == -1:
            active_faces.append('back')
        if x == -1:
            active_faces.append('left')
        if x == 1:
            active_faces.append('right')
        if y == 1:
            active_faces.append('up')
        if y == -1:
            active_faces.append('down')
        return {face: colors[face] for face in active_faces}

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        self._draw_cubie()
        glPopMatrix()

    def _draw_cubie(self):
        glBegin(GL_QUADS)
        for face, color in self.colors.items():
            glColor3fv(color)
            for vertex in self._get_face_vertices(face):
                glVertex3fv(vertex)
        glEnd()

    def _get_face_vertices(self, face):
        # Вершины для каждой грани
        vertices = {
            'front': [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)],
            'back': [(0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5)],
            'left': [(-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)],
            'right': [(0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5)],
            'up': [(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5)],
            'down': [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5)],
        }
        return vertices[face]

    def rotate(self, ax, ay, az):
        # Вращение кубика
        rotation_matrix = np.array([
            [np.cos(ay)*np.cos(az), -np.cos(ay)*np.sin(az), np.sin(ay)],
            [np.sin(ax)*np.sin(ay)*np.cos(az) + np.cos(ax)*np.sin(az), -np.sin(ax)*np.sin(ay)*np.sin(az) + np.cos(ax)*np.cos(az), -np.sin(ax)*np.cos(ay)],
            [-np.cos(ax)*np.sin(ay)*np.cos(az) + np.sin(ax)*np.sin(az), np.cos(ax)*np.sin(ay)*np.sin(az) + np.sin(ax)*np.cos(az), np.cos(ax)*np.cos(ay)]
        ])
        self.position = np.dot(rotation_matrix, self.position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = RubiksCubeWidget()
    widget.resize(800, 600)
    widget.setWindowTitle("3D Кубик Рубика на PySide2")
    widget.show()
    sys.exit(app.exec_())