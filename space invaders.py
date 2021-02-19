import pygame
import sys
import random

WIDTH = 800
HEIGHT = 600

FPS = 60

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)


def collision(x1, y1, x2, y2, x3, y3, x4, y4):
    if max(x1, x3) <= min(x2, x4) and max(y1, y3) <= min(y2, y4):
        return True
    else:
        return False


class Player:
    speed = 3
    width = 76
    height = 36

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.bullets = list()
        self.cooldown_time = 75
        self.lives = 3

    def move_right(self):
        self.x += self.speed
        if self.x + self.width > WIDTH:
            self.x -= self.speed

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def shoot_bullet(self):
        bullet = Bullet(self.x + int(self.width // 2) - int(Bullet.width // 2), self.y - 1 - Bullet.height)
        self.bullets.append(bullet)

    def cooldown(self):
        return (self.timer % self.cooldown_time == 0)

    def update_lives(self):
        self.lives -= 1

    def render(self, background):
        pygame.draw.rect(background, COLOR_RED, pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(background, COLOR_RED, pygame.Rect(self.x + self.width // 2 - 5, self.y - 10, 10, 10))
        for bullet in self.bullets:
            bullet.move_up()
            bullet.render(background)


class Bullet:
    speed = 7
    width = 6
    height = 12

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def render(self, background):
        pygame.draw.rect(background,
                         COLOR_WHITE,
                         pygame.Rect(self.x, self.y, Bullet.width, Bullet.height))


class Bunker:
    health_points = 5
    width = 100
    height = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update_hp(self):
        self.health_points -= 1

    def render(self, background):
        pygame.draw.rect(background,
                         COLOR_GREEN,
                         pygame.Rect(self.x, self.y, Bunker.width, Bunker.height))


class Invader:
    redInvader = pygame.image.load("Assets\RedInvader.png")

    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.ignore = False

    def move_x(self, direction_x):
        if not self.ignore:
            self.x = self.x + pow(-1, direction_x) * self.speed_x

    def move_y(self, direction_y):
        if not self.ignore:
            self.y = self.y + pow(-1, direction_y) * self.speed_y

    def start_ignore(self):
        self.x = 800
        self.y = 600

        self.ignore = True

    def render(self, background):
        if not self.ignore:
            background.blit(self.redInvader, (self.x, self.y))


class Invaders:
    speed_x = 2
    speed_y = 10

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.position = [[100, 35], [600 + Invader.redInvader.get_width(), 210 + Invader.redInvader.get_height()]]
        self.invaders = list()
        self.direction_x = 0
        self.direction_y = 0
        self.timer = 0
        self.cooldown_time = 75
        self.bullets = list()
        for i in range(0, n):
            l = list()
            for j in range(0, m):
                l.append(Invader(60 * (j + 1), 35 * (i + 1), self.speed_x, self.speed_y))
            self.invaders.append(l)

    def move_x(self):
        self.position[0][0] += self.speed_x * pow(-1, self.direction_x)
        self.position[1][0] += self.speed_x * pow(-1, self.direction_x)
        x1 = 999
        y1 = 999
        x2 = 0
        y2 = 0
        for i in range(0, len(self.invaders)):
            for j in range(0, len(self.invaders[i])):
                self.invaders[i][j].move_x(self.direction_x)
                if self.invaders[i][j].ignore == False:
                    x1 = min(x1, self.invaders[i][j].x)
                    y1 = min(y1, self.invaders[i][j].y)
                    x2 = max(x2, self.invaders[i][j].x + Invader.redInvader.get_width())
                    y2 = max(y2, self.invaders[i][j].y + Invader.redInvader.get_height())
        if x1 != self.position[0][0] or y1 != self.position[0][1]:
            self.position[0][0] = x1
            self.position[0][1] = y1
        if x2 != self.position[1][0] or y2 != self.position[1][1]:
            self.position[1][0] = x2
            self.position[1][1] = y2
        if self.position[1][0] > WIDTH or self.position[0][0] < 0:
            self.direction_x = 1 if self.direction_x == 0 else 0
            self.move_y()
        for bullet in self.bullets:
            bullet.move_down()

    def move_y(self):
        self.position[0][1] += self.speed_y * pow(-1, self.direction_y)
        self.position[1][1] += self.speed_y * pow(-1, self.direction_y)
        for i in range(0, len(self.invaders)):
            for j in range(0, len(self.invaders[i])):
                self.invaders[i][j].move_y(self.direction_y)
        if self.position[1][1] > 385 or self.position[0][1] < 30:
            self.direction_y = 1 if self.direction_y == 0 else 0
        for bullet in self.bullets:
            bullet.move_down()

    def render(self, background):
        for i in range(0, len(self.invaders)):
            for j in range(0, len(self.invaders[i])):
                self.invaders[i][j].render(background)
        for bullet in self.bullets:
            bullet.render(background)

    def cooldown(self):
        return (self.timer % self.cooldown_time == 0)

    def win_condition(self):
        for row in self.invaders:
            for invader in row:
                if invader.ignore == False:
                    return False
        return True

    def attack(self,sound):
        k = 0
        i = 0
        sem = 0
        while sem == 0:
            sem = 0
            i = 0
            k = random.randrange(0, self.m)
            for j in range(0, self.n):
                if self.invaders[j][k].ignore == False:
                    sound.play()
                    sem = 1
                    i = j
        self.bullets.append(Bullet(self.invaders[i][k].x + Invader.redInvader.get_width() / 2 - Bullet.width / 2,
                                   self.invaders[i][k].y + Invader.redInvader.get_height() + 1))


def main():
    # Initialize imported pygame modules
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)
    # Set the window's caption
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.Surface((WIDTH, HEIGHT))
    background = background.convert()
    background.fill(COLOR_BLACK)
    bullet_sound1 = pygame.mixer.Sound("Sound\\bullet1.wav")
    bullet_sound2 = pygame.mixer.Sound("Sound\\bullet2.wav")
    hit_sound1 = pygame.mixer.Sound("Sound\hit1.wav")
    hit_sound2 = pygame.mixer.Sound("Sound\hit2.wav")
    hit_sound3 = pygame.mixer.Sound("Sound\hit3.wav")
    lost_sound = pygame.mixer.Sound("Sound\lost.wav")
    win_sound = pygame.mixer.Sound("Sound\win.wav")
    music = pygame.mixer.music.load("Sound\music.wav")

    # Blit everything to screen
    screen.blit(background, (0, 0))

    # Update the screen
    pygame.display.flip()
    running = True
    score = 0
    high_score = 0
    STATE = "MENU"

    while running:
        pygame.mixer.music.play(-1)
        running2 = True
        bunkers = list()
        for i in range(1, 6):
            bunkers.append(Bunker(i * 50 + (i - 1) * Bunker.width, 400))
        enemies = Invaders(5, 9)
        player = Player(382, 550)
        score = 0
        time_start = pygame.time.get_ticks()

        while running2:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if STATE == "MENU":
                background.fill(COLOR_BLACK)
                start_img = pygame.image.load("Assets\start_screen.jpg")
                screen.blit(start_img, (WIDTH // 2 - start_img.get_width() // 2, HEIGHT // 2 - start_img.get_height() // 2))
                pygame.display.flip()
                keys_pressed = pygame.key.get_pressed()
                if True in keys_pressed:
                    STATE = "PLAY"

            if STATE == "GAME OVER":
                if score > high_score:
                    high_score = score
                mouse_pos = pygame.mouse.get_pos()
                mouse_press = pygame.mouse.get_pressed()
                background.fill(COLOR_BLACK)
                game_over_img = pygame.image.load("Assets\game_over.jpg")
                play_again_img = pygame.image.load("Assets\play_again.png")
                play_again_img = pygame.transform.scale(play_again_img, (250, 100))
                score_text = font.render("YOUR SCORE: " + str(score), True, COLOR_WHITE)
                high_score_text = font.render("HIGH SCORE: " + str(high_score), True, COLOR_WHITE)
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() / 2, HEIGHT // 2))
                screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 15))
                background.blit(game_over_img,
                                (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 2 - game_over_img.get_height()))
                background.blit(play_again_img, (WIDTH // 2 - play_again_img.get_width() // 2, HEIGHT // 2 + 45))
                pygame.display.flip()
                screen.blit(background, (0, 0))
                if mouse_pos[0] >= WIDTH // 2 - play_again_img.get_width() // 2 and mouse_pos[
                    0] <= WIDTH // 2 - play_again_img.get_width() // 2 + play_again_img.get_width() and mouse_pos[
                    1] >= HEIGHT // 2 + 45 and mouse_pos[1] <= HEIGHT // 2 + 45 + play_again_img.get_height() and \
                        mouse_press[0]:
                    running2 = False
                    del bunkers
                    del player

            if STATE == "YOU WIN":

                high_score = score
                mouse_pos = pygame.mouse.get_pos()
                mouse_press = pygame.mouse.get_pressed()
                background.fill(COLOR_BLACK)
                you_win_img = pygame.image.load("Assets\you_win.png")
                play_again_img = pygame.image.load("Assets\play_again.png")
                play_again_img = pygame.transform.scale(play_again_img, (250, 100))
                score_text = font.render("YOUR SCORE: " + str(score), True, COLOR_WHITE)
                high_score_text = font.render("HIGH SCORE: " + str(high_score), True, COLOR_WHITE)
                screen.blit(you_win_img,
                            (WIDTH // 2 - you_win_img.get_width() // 2, HEIGHT // 2 - you_win_img.get_height()))
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
                screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 15))
                background.blit(play_again_img, (WIDTH // 2 - play_again_img.get_width() // 2, HEIGHT // 2 + 45))
                pygame.display.flip()
                screen.blit(background, (0, 0))
                if mouse_pos[0] >= WIDTH // 2 - play_again_img.get_width() // 2 and mouse_pos[
                    0] <= WIDTH // 2 - play_again_img.get_width() // 2 + play_again_img.get_width() and mouse_pos[
                    1] >= HEIGHT // 2 + 45 and mouse_pos[1] <= HEIGHT // 2 + 45 + play_again_img.get_height() and \
                        mouse_press[0]:
                    running2 = False
                    del bunkers
                    del player
            if STATE == "PLAY":
                if enemies.win_condition():
                    STATE = "YOU WIN"
                    win_sound.play()
                    continue
                current_score = font.render("Score: " + str(score), True, COLOR_GREEN)
                current_lives = font.render("Lives: " + str(player.lives), True, COLOR_GREEN)
                screen.blit(current_lives, (735, 0))
                screen.blit(current_score, (0, 0))
                background.fill(COLOR_BLACK)
                if not player.cooldown():
                    player.timer += 1
                if not enemies.cooldown():
                    enemies.timer += 1
                player.render(background)
                for bunker in bunkers:
                    bunker.render(background)
                    for bullet in player.bullets:
                        if collision(bunker.x, bunker.y, bunker.x + bunker.width, bunker.y + bunker.height, bullet.x,
                                     bullet.y, bullet.x + bullet.width, bullet.y + bullet.height):
                            hit_sound3.play()
                            bunker.update_hp()
                            player.bullets.remove(bullet)
                            if bunker.health_points == 0:
                                bunkers.remove(bunker)
                    for bullet in enemies.bullets:
                        if collision(bunker.x, bunker.y, bunker.x + bunker.width, bunker.y + bunker.height, bullet.x,
                                     bullet.y, bullet.x + bullet.width, bullet.y + bullet.height):
                            hit_sound3.play()
                            bunker.update_hp()
                            enemies.bullets.remove(bullet)
                            if bunker.health_points == 0:
                                bunkers.remove(bunker)

                for i in range(0, len(enemies.invaders)):
                    for j in range(0, len(enemies.invaders[i])):
                        for bullet in player.bullets:
                            if collision(enemies.invaders[i][j].x, enemies.invaders[i][j].y,
                                         enemies.invaders[i][j].x + enemies.invaders[i][j].redInvader.get_width(),
                                         enemies.invaders[i][j].y + enemies.invaders[i][j].redInvader.get_height(),
                                         bullet.x, bullet.y, bullet.x + bullet.width, bullet.y + bullet.height):
                                hit_sound1.play()
                                enemies.invaders[i][j].start_ignore()
                                score += 25
                                player.bullets.remove(bullet)
                                break
                for bullet in enemies.bullets:
                    if collision(player.x, player.y, player.x + player.width, player.y + player.height, bullet.x,
                                 bullet.y, bullet.x + bullet.width, bullet.y + bullet.height):
                        hit_sound2.play()
                        player.update_lives()
                        enemies.bullets.remove(bullet)
                        if player.lives == 0:
                            lost_sound.play()
                            STATE = "GAME OVER"

                enemies.move_x()
                enemies.render(background)
                if enemies.cooldown():
                    enemies.attack(bullet_sound2)
                    enemies.timer += 1
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_a]:
                    player.move_left()
                if keys_pressed[pygame.K_d]:
                    player.move_right()
                if keys_pressed[pygame.K_SPACE] and player.cooldown():
                    bullet_sound1.play()
                    player.shoot_bullet()
                    player.timer += 1
                pygame.display.flip()
                screen.blit(background, (0, 0))
        STATE = "PLAY"


if __name__ == '__main__':
    main()
