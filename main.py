import pygame
import os
import random
import matplotlib.pyplot as plt

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
# BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60

# ship speed
VEL = 5

# bullet speed
BULLET_VEL = 7

# parm for AI
VEL_AI = 7
BULLET_COOLDOWN_AI = FPS * 0.5
MAX_BULLETS_AI = 10
AI_HEALTH = 10

# parm for testing/player
GODMODE = 0
MAX_BULLETS = 3
PLAYER_HEALTH = 10

if GODMODE == 1:
    MAX_BULLETS = 10

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, rect_ai):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # pygame.draw.rect(WIN, WHITE, rect_ai)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(yellow, choose_direction_x, choose_direction_y):
    if choose_direction_x == 1 and yellow.x - VEL_AI > 0:  # LEFT
        yellow.x -= VEL_AI
    if choose_direction_x == 2 and yellow.x + VEL_AI + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL_AI
    if choose_direction_y == 3 and yellow.y - VEL_AI > 0:  # UP
        yellow.y -= VEL_AI
    if choose_direction_y == 4 and yellow.y + VEL_AI + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL_AI


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            if GODMODE == 0:
                pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
                         2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    RECT_MULTIPLY = 5
    x_formula = yellow.x - SPACESHIP_WIDTH * (RECT_MULTIPLY - 1) / 2
    y_formula = yellow.y - SPACESHIP_HEIGHT * (RECT_MULTIPLY - 1) / 2
    rect_ai = pygame.Rect(x_formula, y_formula,
                          SPACESHIP_WIDTH * RECT_MULTIPLY, SPACESHIP_HEIGHT * RECT_MULTIPLY)
    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()

    last_shot = 0
    tick_number = 0
    red_health = PLAYER_HEALTH
    yellow_health = AI_HEALTH

    current_direction_x, current_direction_y = 0, 0
    choose_direction_y, choose_direction_x = 0, 0

    decision_statistics = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                plt.hist(decision_statistics)
                plt.show()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()

        if yellow.y + SPACESHIP_WIDTH >= red.y >= yellow.y - SPACESHIP_WIDTH:
            if last_shot >= BULLET_COOLDOWN_AI:
                if len(yellow_bullets) < MAX_BULLETS_AI:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                last_shot = 0

        x_formula = yellow.x - SPACESHIP_WIDTH * (RECT_MULTIPLY - 1) / 2
        y_formula = yellow.y - SPACESHIP_HEIGHT * (RECT_MULTIPLY - 1) / 2

        away_top, away_bottom, away_left, away_right = 0, 0, 0, 0

        if tick_number % 10 == 0:
            # assigned random number in case not a single if case worked
            choose_direction_x, choose_direction_y = random.randint(1, 4), random.randint(1, 4)

            for bullet in red_bullets:
                if rect_ai.colliderect(bullet):
                    decision_statistics.append(1)
                    if bullet.y < yellow.y:
                        away_top += 1
                    else:
                        away_bottom += 1

                    if bullet.x < yellow.x:
                        away_left += 1
                    else:
                        away_right += 1

                    if away_top > away_bottom:
                        choose_direction_y = 4
                    elif away_top == away_bottom:
                        choose_direction_y = random.randint(3, 4)
                    else:
                        choose_direction_y = 3

                    if away_left > away_right:
                        choose_direction_x = 2
                    elif away_left == away_right:
                        choose_direction_x = random.randint(1, 2)
                    else:
                        choose_direction_x = 1

                elif random.randint(1, 3) in (1, 2):
                    decision_statistics.append(2)
                    if red.y < yellow.y:
                        if yellow.y < 20:
                            choose_direction_y = 4
                        else:
                            choose_direction_y = 3
                    elif red.y > yellow.y:
                        if yellow.y < SPACESHIP_WIDTH + 20:
                            choose_direction_y = 3
                        else:
                            choose_direction_y = 4
                else:
                    decision_statistics.append(3)
                    choose_direction_y = random.randint(1, 4)

            current_direction_x = choose_direction_x
            current_direction_y = choose_direction_y

            # decision_statistics.append(decision_choose)

        keys_pressed = pygame.key.get_pressed()

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        yellow_handle_movement(yellow, choose_direction_x=current_direction_x, choose_direction_y=current_direction_y)

        red_handle_movement(keys_pressed, red)

        rect_ai.x = x_formula
        rect_ai.y = y_formula

        winner_text = ""
        if red_health <= 0:
            winner_text = "AI (Yellow) Wins!"

        if yellow_health <= 0:
            winner_text = "Player (Red) Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, rect_ai)

        last_shot += 1
        tick_number += 1
        if tick_number == FPS:
            tick_number = 0
        made_a_move = 0

    main()


if __name__ == "__main__":
    main()
