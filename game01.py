import os
# 隐藏 Pygame 支持提示

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
import random  # 导入随机模块


class Drone:
    def __init__(self, image_path, initial_position, step=0.5):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
        self.image_rect = self.image.get_rect()
        self.x, self.y = initial_position
        self.step = step
        self.path = [initial_position]
        self.data = 0  # 无人机的数据属性

    def update_position(self, target_coords, target_index):
        target_x, target_y = target_coords[target_index]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.step:
            # 到达目标点，更新位置并切换到下一个目标
            self.x, self.y = target_x, target_y
            self.path.append((self.x, self.y))
            target_index = (target_index + 1) % len(target_coords)
        else:
            # 按比例更新位置
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * self.step
            self.y += direction_y * self.step
            self.path.append((self.x, self.y))

        # 更新图像位置
        self.image_rect.topleft = (self.x - self.image.get_width() * 0.5, self.y - self.image.get_height() * 0.5)

        return target_index

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)


class Sensor:
    def __init__(self, image_path, scale_factor=0.5, sensor_data=None):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        self.image_rect = self.image.get_rect()
        # 生成随机的数据，如果没有传入数据，则随机生成一个0-100之间的整数
        self.data = sensor_data if sensor_data is not None else random.randint(0, 100)


    def draw(self, screen, position):
        self.image_rect.center = position
        screen.blit(self.image, self.image_rect)


class DataCenter:
    def __init__(self, initial_position, image_path='data_center.png'):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.image_rect = self.image.get_rect()
        self.x, self.y = initial_position
        self.data=0

    def draw(self, screen):
        self.image_rect.topleft = (self.x - self.image.get_width() * 0.5, self.y - self.image.get_height() * 0.5)
        screen.blit(self.image, self.image_rect)


class DroneSimulation:
    def __init__(self, screen_width=2000, screen_height=1000, step=0.5, num_sensors=5):
        # 初始化 Pygame
        pygame.init()

        # 设置窗口标题和图标
        pygame.display.set_caption("Drone Simulation")
        icon = pygame.image.load('plane.png')
        pygame.display.set_icon(icon)

        # 初始化屏幕
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height + 100))

        # 加载背景
        self.background = pygame.image.load('ground.jpg')
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        # 创建无人机实例
        self.drone = Drone('drone.png', initial_position=(100, 100), step=step)

        # 创建数据中心，位置设置为无人机的起始坐标
        self.data_center = DataCenter(initial_position=(self.drone.x, self.drone.y))

        # 使用循环创建多个传感器并随机生成数据
        self.sensors = []
        self.target_coords = []
        for i in range(num_sensors):
            sensor_data = random.randint(0, 100)  # 每个传感器的数据是0-100之间的随机数
            self.sensors.append(Sensor('sensor.png', scale_factor=0.5, sensor_data=sensor_data))
            # 随机生成目标坐标
            self.target_coords.append([random.randint(100, screen_width - 100), random.randint(100, screen_height - 100)])

        # 初始化目标索引
        self.target_index = 0

        # 字体设置
        self.font = pygame.font.SysFont('Arial', 24)

    def draw(self):
        # 绘制背景
        self.screen.blit(self.background, (0, 0))

        # 绘制数据中心
        self.data_center.draw(self.screen)

        # 绘制无人机
        self.drone.draw(self.screen)

        # 绘制传感器并传递数据给无人机
        for i, sensor in enumerate(self.sensors):
            sensor_pos = self.target_coords[i]
            sensor.draw(self.screen, sensor_pos)

        # 绘制飞行路径
        if len(self.drone.path) > 1:
            pygame.draw.lines(self.screen, (255, 0, 0), False, self.drone.path, 2)

        # 绘制信息窗口
        info_rect = pygame.Rect(0, self.screen_height - 100, self.screen_width, 200)
        pygame.draw.rect(self.screen, (255, 255, 255), info_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), info_rect, 2)

        # 显示信息
        base_info_texts = [
            f"Drone Position: ({self.drone.x:.2f}, {self.drone.y:.2f})",
            f"Current Target: {self.target_index + 1}/{len(self.target_coords)}",
            f"Step: {self.drone.step}",
            f"Data Center: {self.data_center.data}",
            f"Drone Data: {self.drone.data}",
        ]

        sensor_info_texts = []

        # 显示每个传感器的数据
        for i, sensor in enumerate(self.sensors):
            sensor_info_texts.append(f"Sensor {i + 1} Data: {sensor.data}")

        y_offset = 10
        for text in base_info_texts:
            label = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(label, (10, self.screen_height - 100 + y_offset))
            y_offset += 30

        y_offset = 10
        for text in sensor_info_texts:
            label = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(label, (300, self.screen_height - 100 + y_offset))
            y_offset += 30

    def run(self):
        # 游戏循环
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 更新无人机位置
            self.target_index = self.drone.update_position(self.target_coords, self.target_index)

            # 绘制所有内容
            self.draw()

            # 刷新显示
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    simulation = DroneSimulation(num_sensors=5)  # 设置传感器的数量
    simulation.run()
