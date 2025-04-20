from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_drone():
    # 清除颜色缓冲区和深度缓冲区
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # 设置视口
    glViewport(0, 0, 800, 600)
    
    # 设置投影矩阵
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    # 启用深度测试
    glEnable(GL_DEPTH_TEST)
    
    # 绘制机身
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # 蓝色
    glTranslatef(0.0, 0.0, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # 绘制四个螺旋桨
    propeller_length = 1.5
    propeller_width = 0.1
    propeller_height = 0.05

    # 前左螺旋桨
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # 红色
    glTranslatef(-0.5, 0.5, 0.5)
    glRotatef(90, 1, 0, 0)
    glScalef(propeller_length, propeller_width, propeller_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # 前右螺旋桨
    glPushMatrix()
    glColor3f(0.0, 1.0, 0.0)  # 绿色
    glTranslatef(0.5, 0.5, 0.5)
    glRotatef(90, 1, 0, 0)
    glScalef(propeller_length, propeller_width, propeller_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # 后左螺旋桨
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # 蓝色
    glTranslatef(-0.5, -0.5, 0.5)
    glRotatef(90, 1, 0, 0)
    glScalef(propeller_length, propeller_width, propeller_height)
    glutSolidCube(1.0)
    glPopMatrix()

    # 后右螺旋桨
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0)  # 黄色
    glTranslatef(0.5, -0.5, 0.5)
    glRotatef(90, 1, 0, 0)
    glScalef(propeller_length, propeller_width, propeller_height)
    glutSolidCube(1.0)
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0, 0, 0, 0, 0, 1)
    draw_drone()
    glFlush()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"drone")
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main() 
