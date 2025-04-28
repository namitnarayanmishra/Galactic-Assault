import pygame
import sys
import random

pygame.init()


screen_width = 960
screen_height = 539
WHITE = (255, 255, 255)
RED = (255, 0, 0)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galactic Assault")


player_size = 50
player_speed = 5
bullet_speed = 20
enemy_speed = 4
asteroid_speed = 2
boss_speed = 2
background_speed = 1  


spaceship_image = pygame.image.load(r"C:\Users\lenovo\Downloads\Galactic_Assault-main\Galactic_Assault-main\Galactic_Assault\spaceship.png").convert_alpha()
background_image = pygame.image.load(r"C:\Users\lenovo\Downloads\Galactic_Assault-main\Galactic_Assault-main\Galactic_Assault\Background.png").convert()
asteroid_image = pygame.image.load(r"C:\Users\lenovo\Downloads\Galactic_Assault-main\Galactic_Assault-main\Galactic_Assault\asteroid.png").convert_alpha()
enemy_image = pygame.image.load(r"C:\Users\lenovo\Downloads\Galactic_Assault-main\Galactic_Assault-main\Galactic_Assault\enemy.png").convert_alpha()
heart_image = pygame.image.load(r"C:\Users\lenovo\Downloads\Galactic_Assault-main\Galactic_Assault-main\Galactic_Assault\heart.png").convert_alpha()
boss_image = pygame.image.load(r"C:\Users\lenovo\Downloads\Galactic_Assault-main\Galactic_Assault-main\Galactic_Assault\boss.png").convert_alpha()


spaceship_image = pygame.transform.scale(spaceship_image, (player_size, player_size))
spaceship_image.set_colorkey(WHITE)
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
heart_image = pygame.transform.scale(heart_image, (25, 25))
boss_image = pygame.transform.scale(boss_image, (200, 200))  # Skaliere das Bossbild
boss_image.set_colorkey(WHITE)

boss_spawned = False # Standardwert für Boss


class Player:
    def __init__(self):
        self.x = screen_width // 2 - player_size // 2
        self.y = screen_height - player_size * 2
        self.image = spaceship_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.lives = 3
        self.direction = "UP"  # Standardrichtung des Spielers

    def move(self, direction):
        self.direction = direction  # Speichere die aktuelle Bewegungsrichtung
        if direction == "LEFT" and self.x > 0:
            self.x -= player_speed
        if direction == "RIGHT" and self.x < screen_width - player_size:
            self.x += player_speed
        if direction == "UP" and self.y > 0:
            self.y -= player_speed
        if direction == "DOWN" and self.y < screen_height - player_size:
            self.y += player_speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 5, 10)

    def move(self):
        if self.direction == "UP":
            self.y -= bullet_speed
        elif self.direction == "DOWN":
            self.y += bullet_speed
        elif self.direction == "LEFT":
            self.x -= bullet_speed
        elif self.direction == "RIGHT":
            self.x += bullet_speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = asteroid_image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += asteroid_speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(asteroid_image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = enemy_image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.y += enemy_speed
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(enemy_image, (self.x, self.y))


class Boss:
    def __init__(self):
        self.x = screen_width // 2 - 100  
        self.y = -200  
        self.image = boss_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 100  
        self.direction = random.choice(["LEFT", "RIGHT"])  
        self.shoot_timer = 0  

    def move(self, boss_bullets):  
        if self.y < 50:  
            self.y += boss_speed

        elif self.direction == "LEFT":
            self.x -= boss_speed
            if self.x <= 0:  
                self.direction = "RIGHT"
        elif self.direction == "RIGHT":
            self.x += boss_speed
            if self.x >= screen_width - self.rect.width:  
                self.direction = "LEFT"

        
        self.rect.topleft = (self.x, self.y)

        
        self.shoot_timer += 1
        if self.health <= 10 and self.shoot_timer > 10:
            boss_bullets.append(Bullet(self.x + self.rect.width // 2, self.y + self.rect.height, "DOWN"))
            self.shoot_timer = 0
        if self.health <= 40 and self.shoot_timer > 25:
            boss_bullets.append(Bullet(self.x + self.rect.width // 2, self.y + self.rect.height, "DOWN"))
            self.shoot_timer = 0
        if self.shoot_timer > 60:  
            boss_bullets.append(Bullet(self.x + self.rect.width // 2, self.y + self.rect.height, "DOWN"))
            self.shoot_timer = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def check_boss_collision(boss, bullets):
    for bullet in bullets[:]:
        if bullet.rect.colliderect(boss.rect):
            bullets.remove(bullet)
            boss.health -= 1
            if boss.health <= 0:
                return True  
    return False  

boss = None  


class Background:
    def __init__(self):
        self.y1 = 0
        self.y2 = -screen_height

    def move(self):
        self.y1 += background_speed
        self.y2 += background_speed
        if self.y1 >= screen_height:
            self.y1 = -screen_height
        if self.y2 >= screen_height:
            self.y2 = -screen_height

    def draw(self):
        screen.blit(background_image, (0, self.y1))
        screen.blit(background_image, (0, self.y2))


def draw_lives(player):
    for i in range(player.lives):
        screen.blit(heart_image, (screen_width - (i + 1) * 30, 10))

def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def check_collisions(player, asteroids, enemies, bullets, boss_bullets):
    global score
    for asteroid in asteroids[:]:
        if player.rect.colliderect(asteroid.rect):
            player.lives -= 1
            asteroids.remove(asteroid)
        for bullet in bullets[:]:
            if bullet.rect.colliderect(asteroid.rect):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                score += 5

    for enemy in enemies[:]:
        if player.rect.colliderect(enemy.rect):
            player.lives -= 1
            enemies.remove(enemy)
        for bullet in bullets[:]:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10

    for boss_bullet in boss_bullets[:]:
        if player.rect.colliderect(boss_bullet.rect):
            player.lives -= 1
            boss_bullets.remove(boss_bullet)

def spawn_asteroids(asteroids):
    if random.random() < 0.02 and boss is None:
        asteroids.append(Asteroid(random.randint(0, screen_width - 50), -50))

def spawn_enemies(enemies):
    if random.random() < 0.05 and boss is None:
        enemies.append(Enemy(random.randint(0, screen_width - 50), -50))

def game_over_menu(score):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Your Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))

    pygame.display.flip()
    pygame.time.wait(3000)

def main_game():
    global score, boss, boss_spawned  
    clock = pygame.time.Clock()
    player = Player()
    background = Background()

    asteroids = []
    enemies = []
    bullets = []
    boss_bullets = []  
    score = 0
    boss = None
    boss_spawned = False  

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pygame.key.get_pressed()[pygame.K_LEFT]:
                        bullets.append(Bullet(player.x + player_size // 2, player.y + player_size // 2, "LEFT"))
                    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                        bullets.append(Bullet(player.x + player_size // 2, player.y + player_size // 2, "RIGHT"))
                    elif pygame.key.get_pressed()[pygame.K_DOWN]:
                        bullets.append(Bullet(player.x + player_size // 2, player.y + player_size // 2, "DOWN"))
                    else:
                        bullets.append(Bullet(player.x + player_size // 2, player.y + player_size // 2, "UP"))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            player.move("RIGHT")
        if keys[pygame.K_UP]:
            player.move("UP")
        if keys[pygame.K_DOWN]:
            player.move("DOWN")

        background.move()

        for asteroid in asteroids:
            asteroid.move()
        for enemy in enemies:
            enemy.move()
        for bullet in bullets[:]:
            bullet.move()
            if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
                bullets.remove(bullet)

        for boss_bullet in boss_bullets[:]:
            boss_bullet.move()
            if boss_bullet.y > screen_height:
                boss_bullets.remove(boss_bullet)

        check_collisions(player, asteroids, enemies, bullets, boss_bullets)

        screen.fill(WHITE)
        background.draw()

        
        if score >= 100 and not boss_spawned:
            boss = Boss()
            boss_spawned = True

        
        if boss is not None:
            boss.move(boss_bullets)  
            boss.draw()
            if check_boss_collision(boss, bullets):
                score += 50  
                boss = None  

        player.draw()


        for asteroid in asteroids:
            asteroid.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()
        for boss_bullet in boss_bullets:
            boss_bullet.draw()
        draw_lives(player)
        draw_score(score)
        if player.lives <= 0:
            game_over_menu(score)
            game_running = False

        spawn_asteroids(asteroids)
        spawn_enemies(enemies)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_game()
