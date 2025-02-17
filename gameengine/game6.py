import os
import pygame
import math

# 隐藏 Pygame 支持提示
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

        # 加载资源
        self.image = pygame.image.load('drone.png')
        self.background = pygame.image.load('ground.jpg')
        self.sensor = pygame.image.load('sensor.png')

        # 设置图像缩放
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.sensor = pygame.transform.scale(self.sensor, (int(self.sensor.get_width() * 0.5), int(self.sensor.get_height() * 0.5)))

        # 初始化位置和目标点
        self.x, self.y = 100, 100
        self.target_coords = [[100, 100], [500, 500], [1500, 200], [800, 800], [1200, 150]]
        self.target_index = 0
        self.step = step

        # 路径记录
        self.path = [(self.x, self.y)]

        # 字体设置
        self.font = pygame.font.SysFont('Arial', 24)

        # 获取无人机图像的矩形区域
        self.image_rect = self.image.get_rect()

    def update_position(self):
        # 获取目标点
        target_x, target_y = self.target_coords[self.target_index]

        # 计算当前位置到目标点的距离
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.step:
            # 到达目标点，更新位置并切换到下一个目标
            self.x, self.y = target_x, target_y
            self.path.append((self.x, self.y))
            self.target_index = (self.target_index + 1) % len(self.target_coords)
        else:
            # 按比例更新位置
            direction_x = dx / distance
            direction_y = dy / distance
            self.x += direction_x * self.step
            self.y += direction_y * self.step
            self.path.append((self.x, self.y))

    def draw(self):
        # 更新图像位置
        self.image_rect.topleft = (self.x - self.image.get_width() * 0.5, self.y - self.image.get_height() * 0.5)

        # 绘制背景
        self.screen.blit(self.background, (0, 0))

        # 绘制飞行路径
        if len(self.path) > 1:
            pygame.draw.lines(self.screen, (255, 0, 0), False, self.path, 2)

        # 绘制传感器位置
        for pos in self.target_coords:
            self.screen.blit(self.sensor, (pos[0] - self.sensor.get_width() * 0.5, pos[1] - self.sensor.get_height() * 0.5))

        # 绘制无人机
        self.screen.blit(self.image, self.image_rect)

        # 绘制信息窗口
        info_rect = pygame.Rect(0, self.screen_height - 100, self.screen_width, 200)
        pygame.draw.rect(self.screen, (255, 255, 255), info_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), info_rect, 2)

        # 显示信息
        info_texts = [
            f"Drone Position: ({self.x:.2f}, {self.y:.2f})",
            f"Target Position: ({self.target_coords[self.target_index][0]}, {self.target_coords[self.target_index][1]})",
            f"Current Target: {self.target_index + 1}/{len(self.target_coords)}",
            f"Step: {self.step}"
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
            self.update_position()

            # 绘制所有内容
            self.draw()

            # 刷新显示
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    simulation = DroneSimulation()
    simulation.run()
