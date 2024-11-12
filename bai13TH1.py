import pygame
import random

                # Khởi tạo Pygame
pygame.init()

                 # Thiết lập kích thước màn hình và các màu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Nhặt Hoa Quả")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



                    # Tải ảnh giỏ và các loại hoa quả
basket_img = pygame.image.load(r"D:\Ki 7\Ma nguon mo\TH1\bai13\gio.png")
basket_img = pygame.transform.scale(basket_img, (200, 50)) 
apple_img = pygame.image.load(r"D:\Ki 7\Ma nguon mo\TH1\bai13\tao.png")
apple_img = pygame.transform.scale(apple_img, (100, 100)) 
orange_img = pygame.image.load(r"D:\Ki 7\Ma nguon mo\TH1\bai13\cam.png")
orange_img = pygame.transform.scale(orange_img, (100, 100)) 
flower_img = pygame.image.load(r"D:\Ki 7\Ma nguon mo\TH1\bai13\hh.png")
flower_img = pygame.transform.scale(flower_img, (100, 100))

# Lớp giỏ
class Basket:
    def __init__(self):
        self.image = basket_img
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.speed = 10

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < WIDTH - self.image.get_width():
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Lớp hoa quả
class Fruit:
    def __init__(self, speed):
        self.type = random.choice(['apple', 'orange', 'flower'])
        if self.type == 'apple':
            self.image = apple_img
        elif self.type == 'orange':
            self.image = orange_img
        else:
            self.image = flower_img

        self.x = random.randint(0, WIDTH - self.image.get_width())
        self.y = 0
        self.speed = speed

    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Kiểm tra va chạm
def check_collision(fruit, basket):
    if (fruit.y + fruit.image.get_height() >= basket.y and 
        fruit.x + fruit.image.get_width() > basket.x and 
        fruit.x < basket.x + basket.image.get_width()):
        return True
    return False

# Hiển thị văn bản
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont('Verdana', 30)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
    

# Vòng lặp chính
basket = Basket()
level = 1
score = 0
time_limit = 30000  # 30 giây
target_score = 100
game_over = False
win = False
start_game = False

clock = pygame.time.Clock()
start_ticks = 0

while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_RETURN and not start_game:  # Bắt đầu trò chơi khi nhấn Enter
                start_game = True
                start_ticks = pygame.time.get_ticks()
                score = 0
                level = 1
                fruits = []
                game_over = False
                win = False

    if start_game and not game_over:
        # Điều khiển giỏ
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket.move_left()
        if keys[pygame.K_RIGHT]:
            basket.move_right()

        # Tính thời gian còn lại
        elapsed_time = pygame.time.get_ticks() - start_ticks
        remaining_time = time_limit - elapsed_time

        # Tạo hoa quả mới theo cấp độ
        if random.randint(1, 30) == 1:
            fruit_speed = 3 + level * 2  # Tăng tốc độ rơi theo cấp
            fruits.append(Fruit(fruit_speed))

        # Cập nhật và vẽ hoa quả
        for fruit in fruits[:]:
            fruit.fall()
            fruit.draw()

            # Kiểm tra va chạm
            if check_collision(fruit, basket):
                fruits.remove(fruit)
                score += 10
            elif fruit.y > HEIGHT:
                fruits.remove(fruit)
                score -= 5

        # Vẽ giỏ và điểm số
        basket.draw()
        draw_text(f"Score: {score}", 36, BLACK, 10, 10)
        draw_text(f"Time: {remaining_time // 1000}s", 36, BLACK, 650, 10)
        draw_text(f"Level: {level}", 36, BLACK, 350, 10)

        # Kiểm tra điều kiện qua cấp hoặc kết thúc
        if remaining_time <= 0:
            if score >= target_score:
                level += 1
                if level > 3:
                    win = True
                    game_over = True
                else:
                    start_ticks = pygame.time.get_ticks()
                    fruits.clear()
            else:
                game_over = True

    else:
        # Hiển thị màn hình chờ hoặc kết thúc
        if win:
            draw_text("Bạn chiến thắng!", 64, BLACK, WIDTH // 2 - 150, HEIGHT // 2 - 50)
        elif game_over:
            draw_text("Chơi lại", 64, BLACK, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        else:
            draw_text("Nhấn Enter để bắt đầu", 64, BLACK, WIDTH // 2 - 200, HEIGHT // 2 - 50)

    pygame.display.flip()
    clock.tick(30)
