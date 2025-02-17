import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import math

# 初始化 Pygame
pygame.init()

# 设置窗口标题
pygame.display.set_caption("drone simulation")

# 加载一个图片文件作为图标
icon = pygame.image.load('plane.png')  # 请替换为你自己的图标路径
pygame.display.set_icon(icon)

step = 0.5  # 控制移动速度

screen_width, screen_height = 2000, 1000
# 设置屏幕大小
screen = pygame.display.set_mode((screen_width, screen_height+100))

# 加载图片
image = pygame.image.load('drone.png')  # 替换成你的图片路径
# 加载背景图片
background = pygame.image.load('ground.jpg')  # 替换成你的背景图片路径

sensor = pygame.image.load('sensor.png')

# 获取背景图片的尺寸
background_width, background_height = background.get_size()

# 设置新的尺寸
new_width = int(image.get_width() * 0.1)  # 将宽度缩小为原来的一半
new_height = int(image.get_height() * 0.1)  # 将高度缩小为原来的一半

# 使用 pygame.transform.scale 缩小图片
image = pygame.transform.scale(image, (new_width, new_height))
background = pygame.transform.scale(background, (screen_width, screen_height))
sensor = pygame.transform.scale(sensor, (sensor.get_width() * 0.5, sensor.get_height() * 0.5))

# 获取图片的矩形区域，用于控制位置
image_rect = image.get_rect()

# 定义目标坐标列表（这些坐标可以调整）
target_coords = [[100, 100], [500, 500], [1500, 200], [800, 800], [1200, 150]]


# 当前坐标
x, y = target_coords[0]

# 设置一个目标索引
target_index = 0

# 初始化字体对象
font = pygame.font.SysFont('Arial', 24)

# 用于记录路径
path = [(x, y)]  # 路径从起始点开始
# 游戏循环标志
running = True

# 游戏主循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取当前目标坐标
    target_x, target_y = target_coords[target_index]

    # 计算当前坐标和目标坐标之间的距离
    dx = target_x - x
    dy = target_y - y
    distance = math.sqrt(dx**2 + dy**2)

    if distance < step:
        # 如果距离小于一步的距离，就到达目标，切换到下一个目标
        x, y = target_x, target_y
        path.append((x, y))  # 记录到达的目标点
        target_index = (target_index + 1) % len(target_coords)  # 循环使用目标坐标
    else:
        # 计算每一步的方向，按比例更新位置
        direction_x = dx / distance
        direction_y = dy / distance
        x += direction_x * step
        y += direction_y * step
        path.append((x, y))  # 记录当前的坐标

    # 更新图片的位置
    image_rect.topleft = (x-image.get_width() * 0.5, y-image.get_height() * 0.5)

    # 绘制背景
    screen.blit(background, (0, 0))  # 将背景绘制到屏幕上，从(0, 0)开始

    # 绘制飞行路线
    if len(path) > 1:
        pygame.draw.lines(screen, (255, 0, 0), False, path, 2)  # 红色线条表示路径

    # # 绘制目标点标记
    # for target in target_coords:
    #     pygame.draw.circle(screen, (0, 255, 0), target, 10)  # 绿色圆圈表示目标点

    for pos in target_coords:
        screen.blit(sensor, (pos[0]-sensor.get_width() * 0.5, pos[1]-sensor.get_height() * 0.5))

    # 绘制无人机
    screen.blit(image, image_rect)

    # 绘制信息窗口
    # 定义信息框的位置和大小
    info_rect = pygame.Rect(0, screen_height - 100, screen_width, 200)
    pygame.draw.rect(screen, (255, 255, 255), info_rect)  # 绘制白色背景框
    pygame.draw.rect(screen, (0, 0, 0), info_rect, 2)  # 绘制黑色边框

    # 准备要显示的信息
    info_texts = [
        f"Drone Position: ({x:.2f}, {y:.2f})",
        f"Target Position: ({target_x}, {target_y})",
        f"Current Target: {target_index + 1}/{len(target_coords)}",
        f"Step: {step}"
    ]

    # 渲染信息文本并绘制到屏幕
    y_offset = 10  # 文本的垂直偏移
    for text in info_texts:
        label = font.render(text, True, (0, 0, 0))  # 黑色文字
        screen.blit(label, (10, screen_height - 100 + y_offset))
        y_offset += 30  # 调整每行文本之间的间距

    # 刷新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
