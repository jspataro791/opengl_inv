
#=========================================================================
# # IMPORTS
#=========================================================================

import sys

import OpenGL

OpenGL.FORWARD_COMPATIBLE_ONLY = True
OpenGL.FULL_LOGGING = True
OpenGL.USE_ACCELERATE = True

from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *


import numpy as np


#=========================================================================
# # CLASSES
#=========================================================================


class OGLWidget(QGLWidget):

    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)

        self.cameraPos = np.array([0, 0, 0], dtype=np.float32)
        self.cameraFront = np.array([0, 0, -1], dtype=np.float32)
        self.cameraUp = np.array([0, 1, 0], dtype=np.float32)

        self.cameraSpeed = 0.2

    def keyPressEvent(self, ev):

        key = ev.key()

        if key == Qt.Key_W:
            print('forward')
            self.cameraPos += self.cameraSpeed * self.cameraFront
        if key == Qt.Key_S:
            self.cameraPos -= self.cameraSpeed * self.cameraFront
        if key == Qt.Key_A:
            crossVec = np.cross(self.cameraFront, self.cameraUp)
            crossVecNorm = crossVec / np.linalg.norm(crossVec)

            self.cameraPos -= crossVecNorm * self.cameraSpeed

        if key == Qt.Key_D:
            crossVec = np.cross(self.cameraFront, self.cameraUp)
            crossVecNorm = crossVec / np.linalg.norm(crossVec)

            self.cameraPos += crossVecNorm * self.cameraSpeed

        print(self.cameraPos)

        self.update()

    def initializeGL(self):

        VERTEX_SHADER = shaders.compileShader("""#version 120 
         void main() { 
         gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
         }""", GL_VERTEX_SHADER)

        FRAGMENT_SHADER = shaders.compileShader("""#version 120 
         void main() { 
         gl_FragColor = vec4( 0, 1, 0, 1 ); 
         }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

        self.vbo = vbo.VBO(np.array([[0, 1, 0],
                                     [-1, -1, 0],
                                     [1, -1, 0],
                                     [2, -1, 0],
                                     [4, -1, 0],
                                     [4, 1, 0],
                                     [2, -1, 0],
                                     [4, 1, 0],
                                     [2, 1, 0]], dtype=np.float32))

        glClearColor(0.5, 0.5, 0.5, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_MULTISAMPLE)
        lightPosition = np.array([0.5, 0.5, 7.0, 1.0], dtype=np.float32)

        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, self.width() / self.height(), 1, 100)

#     def resizeGL(self, width, height):
#
#         glViewport(0, 0, width, height)

        self.quadric = gluNewQuadric()

    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        camAdd = self.cameraPos + self.cameraFront

        gluLookAt(self.cameraPos[0], self.cameraPos[1], self.cameraPos[2],
                  camAdd[0], camAdd[1], camAdd[2],
                  self.cameraUp[0], self.cameraUp[1], self.cameraUp[2])

        glPushMatrix()

        gluSphere(self.quadric, 1, 25, 25)

        glPopMatrix()

        glFlush()


#         try:
#             self.vbo.bind()
#             try:
#                 glEnableClientState(GL_VERTEX_ARRAY)
#                 glVertexPointerf(self.vbo)
#                 glDrawArrays(GL_TRIANGLES, 0, len(self.vbo))
#             finally:
#                 self.vbo.unbind()
#                 glDisableClientState(GL_VERTEX_ARRAY)
#         finally:
#             shaders.glUseProgram(0)

#=========================================================================
# # MAIN
#=========================================================================


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = OGLWidget()
    win.show()

    app.exec_()
