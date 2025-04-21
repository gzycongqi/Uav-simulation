import os
# 隐藏 Pygame 支持提示

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
import random  # 导入随机模块
import threading

#prepare the sensor data
def parse_beam_search_solution(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse coordinates
    coordinates = []
    for line in lines[1:51]:  # Assuming coordinates are in lines 2 to 51
        x, y = map(float, line.strip().split(','))
        coordinates.append((x, y))

    # Parse indices
    indices = []
    for line in lines[52:]:  # Assuming indices start from line 53
        indices.append(int(line.strip()))

    return coordinates, indices

class Tree:
    def __init__(self):
        self.snow=0


class Drone:
    def __init__(self, image_path, initial_position, step=0.5):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
        self.image_rect = self.image.get_rect()
        self.x, self.y = initial_position
        self.step = step
        self.path = [initial_position]
        self.data = 0  # 无人机的数据属性

    def update_position(self, target_coords, target_index, sensors):
        target_x, target_y = target_coords[target_index]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= self.step:
            # 到达目标点，更新位置并切换到下一个目标
            self.x, self.y = target_x, target_y
            self.path.append((self.x, self.y))
            # 向传感器发送随机数据
            sensors[target_index].data += random.randint(1, 10)
            target_index = (target_index + 1) % len(target_coords)
            if target_index == 0:
                target_index=-1
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
    def __init__(self, image_path, scale_factor=0.3):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        self.image_rect = self.image.get_rect()
        # 初始化数据为0
        self.data = 0

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
    def __init__(self, screen_width=1200, screen_height=1000, step=0.5, num_sensors=50):
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
        self.background = pygame.image.load('forest.png')
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

        # 创建无人机实例
        self.drone = Drone('drone.png', initial_position=(100, 100), step=step)

        # 创建数据中心，位置设置为无人机的起始坐标
        self.data_center = DataCenter(initial_position=(self.drone.x, self.drone.y))

        # 使用循环创建多个传感器并随机生成数据
        self.sensors = []
        self.target_coords = []
        for i in range(num_sensors):
            self.sensors.append(Sensor('sensor.png', scale_factor=0.5))
            # 随机生成目标坐标
            # self.target_coords.append([random.randint(100, screen_width - 100), random.randint(100, screen_height - 100)])

        # print("Target Coordinates:", self.target_coords)

        file_path = 'beam_search_solution.txt'
        coordinates, indices = parse_beam_search_solution(file_path)
        print("indice:",indices)
        scale_factor = 800  # Define your scale factor here
        reordered_coordinates = [list(scale_factor * x for x in coordinates[i]) for i in indices]
        self.target_coords = reordered_coordinates
        min_distance = float('inf')
        min_index=-1
        for i, sensor in enumerate(self.sensors):
                dx = self.data_center.x - self.target_coords[i][0]
                dy = self.data_center.y - self.target_coords[i][1]
                distance = math.sqrt(dx**2 + dy**2)
                if distance < min_distance:
                    min_distance = distance
                    min_index = i

        self.target_coords=self.target_coords[min_index:]+self.target_coords[:min_index]




        # 初始化目标索引
        self.target_index = 0

        # 字体设置
        self.font = pygame.font.SysFont('Arial', 24)

    def calculate_distances(self):
        while True:
            for i, sensor in enumerate(self.sensors):
                dx = self.drone.x - self.target_coords[i][0]
                dy = self.drone.y - self.target_coords[i][1]
                distance = math.sqrt(dx**2 + dy**2)
                # print(f"Distance to Sensor {i + 1}: {distance:.2f}")
            pygame.time.wait(1000)  # Wait for 1 second before recalculating

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
        
        print(self.target_coords)
        # Start the distance calculation thread
        distance_thread = threading.Thread(target=self.calculate_distances)
        distance_thread.daemon = True  # Daemonize thread to exit when main program exits
        distance_thread.start()

        # 游戏循环
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 更新无人机位置并传递传感器列表
            self.target_index = self.drone.update_position(self.target_coords, self.target_index, self.sensors)

            # 绘制所有内容
            self.draw()

            # 刷新显示
            pygame.display.flip()

            if(self.target_index==-1):
                break

        pygame.quit()


if __name__ == "__main__":
    simulation = DroneSimulation(num_sensors=50)  # 设置传感器的数量
    simulation.run()
