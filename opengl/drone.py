import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# 全局变量，用于摄像机控制
camera_angle_x = 20.0   # 绕X轴的旋转角度（上下转动）
camera_angle_y = 30.0   # 绕Y轴的旋转角度（左右转动）
camera_distance = 20.0  # 摄像机距离原点的距离

# 记录鼠标上一次的位置
last_mouse_x = 0
last_mouse_y = 0
mouse_left_down = False

def init():
    """OpenGL 初始化设置"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置背景色为黑色
    glEnable(GL_DEPTH_TEST)           # 开启深度测试

def reshape(width, height):
    """窗口大小改变时的回调函数"""
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / float(height), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
    """场景渲染函数"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 根据当前的旋转角度和距离计算摄像机位置（球面坐标系）
    rad_x = math.radians(camera_angle_x)
    rad_y = math.radians(camera_angle_y)
    eye_x = camera_distance * math.cos(rad_x) * math.sin(rad_y)
    eye_y = camera_distance * math.sin(rad_x)
    eye_z = camera_distance * math.cos(rad_x) * math.cos(rad_y)

    # 设置摄像机：眼睛位置(eye_x, eye_y, eye_z)，目标位置为原点，UP方向为Y轴正方向
    gluLookAt(eye_x, eye_y, eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # 绘制地面网格
    draw_grid()

    # 绘制无人机（红色球体）
    glColor3f(1.0, 0.0, 0.0)  # 红色
    glPushMatrix()
    drone_radius = 0.5
    # 将无人机抬高，使球体与地面接触（假设地面在 y=0）
    glTranslatef(0.0, drone_radius, 0.0)
    glutSolidSphere(drone_radius, 20, 20)
    glPopMatrix()

    glutSwapBuffers()

def draw_grid():
    """绘制地面网格"""
    glColor3f(0.5, 0.5, 0.5)  # 灰色
    glBegin(GL_LINES)
    grid_size = 20  # 网格横跨 -20 ~ 20
    step = 1.0      # 网格间隔
    for i in range(-grid_size, grid_size + 1):
        # 绘制平行于 Z 轴的直线
        glVertex3f(i * step, 0, -grid_size * step)
        glVertex3f(i * step, 0, grid_size * step)
        # 绘制平行于 X 轴的直线
        glVertex3f(-grid_size * step, 0, i * step)
        glVertex3f(grid_size * step, 0, i * step)
    glEnd()

def mouse(button, state, x, y):
    """鼠标点击回调函数，用于启动/结束拖动以及处理滚轮事件"""
    global last_mouse_x, last_mouse_y, mouse_left_down, camera_distance
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouse_left_down = True
            last_mouse_x = x
            last_mouse_y = y
        elif state == GLUT_UP:
            mouse_left_down = False
    # 有些 GLUT 实现中，鼠标滚轮会以 button==3 和 button==4 传入
    if button == 3:  # 滚轮向前，缩小距离（放大）
        camera_distance -= 1.0
        if camera_distance < 2.0:
            camera_distance = 2.0
        glutPostRedisplay()
    if button == 4:  # 滚轮向后，增大距离（缩小）
        camera_distance += 1.0
        glutPostRedisplay()

def motion(x, y):
    """鼠标拖动时的回调函数，用于改变摄像机角度"""
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y
    if mouse_left_down:
        dx = x - last_mouse_x
        dy = y - last_mouse_y
        camera_angle_y += dx * 0.5  # 水平拖动改变左右视角
        camera_angle_x += dy * 0.5  # 垂直拖动改变上下视角
        # 限制 camera_angle_x 的范围，避免视角翻转
        camera_angle_x = max(-89.0, min(89.0, camera_angle_x))
        last_mouse_x = x
        last_mouse_y = y
        glutPostRedisplay()

def keyboard(key, x, y):
    """键盘回调：按 ESC 键退出程序"""
    if key == b'\x1b':  # ESC 键
        sys.exit()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Drone Simulation")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':
    main()
