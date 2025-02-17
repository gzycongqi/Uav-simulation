import pygame

# 初始化 Pygame
pygame.init()

step=0.5

screen_width, screen_height = 2000, 1000
# 设置屏幕大小
screen = pygame.display.set_mode((screen_width, screen_height))

# 加载图片
image = pygame.image.load('drone.png')  # 替换成你的图片路径
# 加载背景图片
background = pygame.image.load('ground.jpg')  # 替换成你的背景图片路径

# 获取背景图片的尺寸
background_width, background_height = background.get_size()

# 打印背景尺寸
print(f"Background dimensions: {background_width}x{background_height}")

# 设置新的尺寸 (例如将宽度和高度都缩小为原来的 0.1倍)
new_width = int(image.get_width() * 0.1)  # 将宽度缩小为原来的一半
new_height = int(image.get_height() * 0.1)  # 将高度缩小为原来的一半

# 使用 pygame.transform.scale 缩小图片
image = pygame.transform.scale(image, (new_width, new_height))
background = pygame.transform.scale(background, (screen_width, screen_height))

# 获取图片的矩形区域，用于控制位置
image_rect = image.get_rect()
x, y = screen_width/2 , screen_height/2
print(x,y)
image_rect.topleft = (x, y)

# 游戏循环标志
running = True

# 初始化相机（镜头）位置
# camera_x, camera_y = 0, 0

# 游戏主循环
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 键盘控制移动
    keys = pygame.key.get_pressed()  # 获取所有按键的状态
    if keys[pygame.K_LEFT]:  # 左键
        x -= step
        print(x,y)
    if keys[pygame.K_RIGHT]:  # 右键
        x += step
        print(x,y)
    if keys[pygame.K_UP]:  # 上键
        y -= step
        print(x,y)
    if keys[pygame.K_DOWN]:  # 下键
        y += step
        print(x,y)

    # 更新图片的位置
    
    image_rect.topleft = (x, y)

    # 更新游戏状态

    # 计算相机位置，使其跟随图片移动
    # camera_x = x - screen_width // 2  # 镜头水平居中
    # camera_y = y - screen_height // 2  # 镜头垂直居中

    # 绘制背景
    screen.blit(background, (0, 0))  # 将背景绘制到屏幕上，从(0, 0)开始

    # # 绘制背景，按照相机位置进行平移
    # screen.blit(background, (-camera_x, -camera_y))


    # # 绘制缩小后的图片
    # screen.blit(image, image_rect)

    # 绘制可移动的图片，按照相机位置进行平移
    screen.blit(image,image_rect)
    

    
    # 刷新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
