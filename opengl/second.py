import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ---------------------------
# 摄像机控制相关全局变量
# ---------------------------
camera_angle_x = 20.0   # 绕X轴旋转（上下）
camera_angle_y = 30.0   # 绕Y轴旋转（左右）
camera_distance = 20.0  # 摄像机距离原点的距离

last_mouse_x = 0
last_mouse_y = 0
mouse_left_down = False

# ---------------------------
# 无人机和路径控制相关变量
# ---------------------------
drone_radius = 0.5
# 初始无人机位置，设置在路径第一个点，注意保证球体与地面接触
drone_pos = [0.0, drone_radius, 0.0]

# 定义一系列路径点（你可以修改为任意坐标）
# 注意：这里的 y 坐标均设置为 drone_radius，保证无人机始终在离地面 drone_radius 的高度
path_points = [
    [0.0, drone_radius, 0.0],
    [5.0, drone_radius, 0.0],
    [5.0, drone_radius, 5.0],
    [0.0, drone_radius, 5.0],
    [0.0, drone_radius, 0.0]
]
current_target_index = 1  # 当前目标点的索引
speed = 0.05  # 每次更新时无人机移动的步长（单位/帧）

def init():
    """OpenGL初始化设置"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 背景色为黑色
    glEnable(GL_DEPTH_TEST)           # 开启深度测试

def reshape(width, height):
    """窗口尺寸改变时的回调"""
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

    # 根据当前视角参数计算摄像机位置（球面坐标）
    rad_x = math.radians(camera_angle_x)
    rad_y = math.radians(camera_angle_y)
    eye_x = camera_distance * math.cos(rad_x) * math.sin(rad_y)
    eye_y = camera_distance * math.sin(rad_x)
    eye_z = camera_distance * math.cos(rad_x) * math.cos(rad_y)

    gluLookAt(eye_x, eye_y, eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # 绘制地面网格
    draw_grid()
    # 绘制路径（可选）
    draw_path()

    # 绘制无人机（红色球体），位置使用 drone_pos
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(drone_pos[0], drone_pos[1], drone_pos[2])
    glutSolidSphere(drone_radius, 20, 20)
    glPopMatrix()

    glutSwapBuffers()

def draw_grid():
    """绘制地面网格"""
    glColor3f(0.5, 0.5, 0.5)  # 灰色
    glBegin(GL_LINES)
    grid_size = 20  # 网格范围 -20 ~ 20
    step = 1.0     # 网格间隔
    for i in range(-grid_size, grid_size + 1):
        # 平行于 Z 轴的线
        glVertex3f(i * step, 0, -grid_size * step)
        glVertex3f(i * step, 0, grid_size * step)
        # 平行于 X 轴的线
        glVertex3f(-grid_size * step, 0, i * step)
        glVertex3f(grid_size * step, 0, i * step)
    glEnd()

def draw_path():
    """绘制路径（可选），用绿线连接路径点，并用小黄球标记路径点"""
    # 绘制路径线
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for point in path_points:
        glVertex3f(point[0], point[1], point[2])
    glEnd()
    # 绘制路径点
    glColor3f(1.0, 1.0, 0.0)
    for point in path_points:
        glPushMatrix()
        glTranslatef(point[0], point[1], point[2])
        glutSolidSphere(0.1, 10, 10)
        glPopMatrix()

def update_drone_position():
    """
    按路径点更新无人机位置：朝向当前目标点移动，
    当与目标点距离足够小时，切换到下一个目标。
    """
    global drone_pos, current_target_index
    target = path_points[current_target_index]
    # 计算当前位置到目标的向量
    vec = [target[i] - drone_pos[i] for i in range(3)]
    distance = math.sqrt(sum([vec[i] ** 2 for i in range(3)]))
    # 如果足够接近目标点，则直接设置为目标，并切换目标点
    if distance < 0.01:
        drone_pos = target.copy()
        current_target_index = (current_target_index + 1) % len(path_points)
    else:
        # 计算单位方向向量，按设定速度前进
        direction = [vec[i] / distance for i in range(3)]
        drone_pos = [drone_pos[i] + direction[i] * speed for i in range(3)]

def timer(value):
    """定时器回调函数，用于更新无人机位置并重绘"""
    update_drone_position()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # 约60FPS

def mouse(button, state, x, y):
    """鼠标点击回调，用于拖动视角和滚轮缩放"""
    global last_mouse_x, last_mouse_y, mouse_left_down, camera_distance
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouse_left_down = True
            last_mouse_x = x
            last_mouse_y = y
        elif state == GLUT_UP:
            mouse_left_down = False
    # 部分 GLUT 实现中，鼠标滚轮事件以 button==3/4 传入
    if button == 3:  # 滚轮向前（放大视图，即减小摄像机距离）
        camera_distance -= 1.0
        if camera_distance < 2.0:
            camera_distance = 2.0
        glutPostRedisplay()
    if button == 4:  # 滚轮向后（缩小视图，即增大摄像机距离）
        camera_distance += 1.0
        glutPostRedisplay()

def motion(x, y):
    """鼠标拖动回调，用于改变视角"""
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y
    if mouse_left_down:
        dx = x - last_mouse_x
        dy = y - last_mouse_y
        camera_angle_y += dx * 0.5
        camera_angle_x += dy * 0.5
        # 限制垂直视角范围，避免视角颠倒
        camera_angle_x = max(-89.0, min(89.0, camera_angle_x))
        last_mouse_x = x
        last_mouse_y = y
        glutPostRedisplay()

def keyboard(key, x, y):
    """键盘回调：按 ESC 键退出程序"""
    if key == b'\x1b':  # ESC
        sys.exit()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Drone Simulation with Path Movement")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)  # 启动定时器，更新无人机位置
    glutMainLoop()

if __name__ == '__main__':
    main()
