import os
import pygame
import math

# 隐藏 Pygame 支持提示
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Drone:
    def __init__(self, image_path, initial_position, step=0.5):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
        self.image_rect = self.image.get_rect()
        self.x, self.y = initial_position
        self.step = step
        self.path = [initial_position]

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
    def __init__(self, image_path, scale_factor=0.5):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        self.image_rect = self.image.get_rect()

    def draw(self, screen, position):
        self.image_rect.center = position
        screen.blit(self.image, self.image_rect)


class DroneSimulation:
    def __init__(self, screen_width=2000, screen_height=1000, step=0.5):
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

        # 创建无人机和传感器实例
        self.drone = Drone('drone.png', initial_position=(100, 100), step=step)
        self.sensor = Sensor('sensor.png', scale_factor=0.5)

        # 初始化目标点和目标索引
        self.target_coords = [[100, 100], [500, 500], [1500, 200], [800, 800], [1200, 150]]
        self.target_index = 0

        # 字体设置
        self.font = pygame.font.SysFont('Arial', 24)

    def draw(self):
        # 绘制背景
        self.screen.blit(self.background, (0, 0))

        # 绘制无人机
        self.drone.draw(self.screen)

        # 绘制传感器
        for pos in self.target_coords:
            self.sensor.draw(self.screen, pos)

        # 绘制飞行路径
        if len(self.drone.path) > 1:
            pygame.draw.lines(self.screen, (255, 0, 0), False, self.drone.path, 2)

        # 绘制信息窗口
        info_rect = pygame.Rect(0, self.screen_height - 100, self.screen_width, 200)
        pygame.draw.rect(self.screen, (255, 255, 255), info_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), info_rect, 2)

        # 显示信息
        info_texts = [
            f"Drone Position: ({self.drone.x:.2f}, {self.drone.y:.2f})",
            f"Target Position: ({self.target_coords[self.target_index][0]}, {self.target_coords[self.target_index][1]})",
            f"Current Target: {self.target_index + 1}/{len(self.target_coords)}",
            f"Step: {self.drone.step}"
        ]

        y_offset = 10
        for text in info_texts:
            label = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(label, (10, self.screen_height - 100 + y_offset))
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
    simulation = DroneSimulation()
    simulation.run()
