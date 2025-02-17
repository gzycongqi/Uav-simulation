import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

# ---------------------------
# 摄像机控制相关全局变量
# ---------------------------
camera_angle_x = 20.0   # 绕X轴旋转（上下）
camera_angle_y = 30.0   # 绕Y轴旋转（左右）
camera_distance = 30.0  # 摄像机距离原点的距离

last_mouse_x = 0
last_mouse_y = 0
mouse_left_down = False

# ---------------------------
# 无人机和路径控制相关变量
# ---------------------------
drone_radius = 0.5
drone_pos = [0.0, 1.0, 0.0]

path_points = [
    [0.0, 1.0, 0.0],
    [5.0, 2.0, 0.0],
    [5.0, 3.0, 5.0],
    [0.0, 4.0, 5.0],
    [-5.0, 3.0, 0.0],
    [0.0, 2.0, -5.0],
    [0.0, 1.0, 0.0]
]
current_target_index = 1
speed = 0.05

# ---------------------------
# 地面纹理相关变量
# ---------------------------
ground_texture = None

def load_texture(filename):
    """
    加载图片并生成 OpenGL 纹理
    """
    try:
        image = Image.open(filename)
        # 翻转图片，使其符合 OpenGL 坐标
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGB").tobytes()
        width, height = image.size

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        return tex_id
    except Exception as e:
        print(f"纹理加载失败: {e}")
        return None

def init():
    """OpenGL初始化设置"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 背景色：黑色
    glEnable(GL_DEPTH_TEST)           # 开启深度测试
    glEnable(GL_TEXTURE_2D)           # 开启纹理映射
    global ground_texture
    # 加载地面纹理（请确保 ground.jpg 存在）
    ground_texture = load_texture("ground.jpg")
    if ground_texture is None:
        print("纹理加载失败，程序无法继续运行。")
        sys.exit()

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

    # 根据当前摄像机参数计算摄像机位置（球面坐标系）
    rad_x = math.radians(camera_angle_x)
    rad_y = math.radians(camera_angle_y)
    eye_x = camera_distance * math.cos(rad_x) * math.sin(rad_y)
    eye_y = camera_distance * math.sin(rad_x)
    eye_z = camera_distance * math.cos(rad_x) * math.cos(rad_y)
    gluLookAt(eye_x, eye_y, eye_z,
              0.0, 0.0, 0.0,  # 观察目标为原点
              0.0, 1.0, 0.0)  # UP方向为Y轴正方向

    # 绘制带纹理的地面
    draw_ground()
    # 绘制路径（可选，用绿线和黄色小球标记路径点）
    draw_path()

    # 绘制无人机（红色球体），位置由 drone_pos 控制
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(drone_pos[0], drone_pos[1], drone_pos[2])
    glutSolidSphere(drone_radius, 20, 20)
    glPopMatrix()

    glutSwapBuffers()

def draw_ground():
    """使用纹理绘制地面，将图片贴在一个较大的四边形上"""
    if ground_texture is None:
        print("纹理未加载，无法绘制地面。")
        return

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ground_texture)
    glColor3f(1.0, 1.0, 1.0)  # 保证颜色白色不影响纹理颜色

    # 绘制一个位于 y=0 平面的四边形
    # 这里设置的顶点坐标和纹理坐标可根据需要调整
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-50.0, 0.0, -50.0)
    
    glTexCoord2f(10.0, 0.0)
    glVertex3f(50.0, 0.0, -50.0)
    
    glTexCoord2f(10.0, 10.0)
    glVertex3f(50.0, 0.0, 50.0)
    
    glTexCoord2f(0.0, 10.0)
    glVertex3f(-50.0, 0.0, 50.0)
    glEnd()

    # 若其他部分不需要纹理，可禁用纹理映射
    glDisable(GL_TEXTURE_2D)

def draw_path():
    """绘制路径（可选）：用绿线连接路径点，并用小黄球标记每个路径点"""
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for point in path_points:
        glVertex3f(point[0], point[1], point[2])
    glEnd()
    glColor3f(1.0, 1.0, 0.0)
    for point in path_points:
        glPushMatrix()
        glTranslatef(point[0], point[1], point[2])
        glutSolidSphere(0.1, 10, 10)
        glPopMatrix()

def update_drone_position():
    """
    根据路径点更新无人机位置：
    朝当前目标点移动，当接近目标点时切换到下一个目标点。
    """
    global drone_pos, current_target_index
    target = path_points[current_target_index]
    vec = [target[i] - drone_pos[i] for i in range(3)]
    distance = math.sqrt(sum(v * v for v in vec))
    if distance < 0.01:
        drone_pos = target.copy()
        current_target_index = (current_target_index + 1) % len(path_points)
    else:
        direction = [v / distance for v in vec]
        drone_pos = [drone_pos[i] + direction[i] * speed for i in range(3)]

def timer(value):
    """定时器回调，用于更新无人机位置并重绘"""
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
    # 部分 GLUT 实现中，滚轮事件以 button==3/4 传入
    if button == 3:  # 滚轮向前（放大视图，即减小摄像机距离）
        camera_distance -= 1.0
        if camera_distance < 2.0:
            camera_distance = 2.0
        glutPostRedisplay()
    if button == 4:  # 滚轮向后（缩小视图，即增大摄像机距离）
        camera_distance += 1.0
        glutPostRedisplay()

def motion(x, y):
    """鼠标拖动回调，用于调整摄像机视角"""
    global last_mouse_x, last_mouse_y, camera_angle_x, camera_angle_y
    if mouse_left_down:
        dx = x - last_mouse_x
        dy = y - last_mouse_y
        camera_angle_y += dx * 0.5
        camera_angle_x += dy * 0.5
        camera_angle_x = max(-89.0, min(89.0, camera_angle_x))
        last_mouse_x = x
        last_mouse_y = y
        glutPostRedisplay()

def keyboard(key, x, y):
    """键盘回调：按 ESC 键退出程序"""
    if key == b'\x1b':
        sys.exit()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Drone Simulation with Textured Ground")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, timer, 0)  # 启动定时器
    glutMainLoop()

if __name__ == '__main__':
    main()
