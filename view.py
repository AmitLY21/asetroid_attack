import random as r
import pygame
import math


def main():
    # Init the pygame
    pygame.init()
    clock = pygame.time.Clock()
    # Title & Icon
    icon = pygame.image.load("images/icon.jfif")
    pygame.display.set_caption("Asteroid Attack!")
    pygame.display.set_icon(icon)

    # Create the Screen aka boundary
    width = 700
    height = 500
    screen = pygame.display.set_mode((width, height))
    background = pygame.image.load('images/bg.jfif')

    # Game Over
    over_font = pygame.font.Font('font/ARCADECLASSIC.TTF', 32)
    # Sound
    pygame.mixer.music.load('sound/bg_music.mp3')
    pygame.mixer.music.play(-1)

    # --------------------Score------------------------
    score_value = 0
    font = pygame.font.Font('font/ARCADECLASSIC.TTF', 32)
    textX = 10
    textY = 10
    combo = 1

    def show_score(x, y):
        score = font.render("Score  " + str(score_value), True, [232, 232, 232])
        screen.blit(score, (x, y))

    # --------------------Player------------------------
    player_img = pygame.image.load('images/player' + str(r.randint(1, 2)) + '.png')
    # Start point
    player_height = 64
    player_width = 64
    playerX = width / 2 - 32
    playerY = height - height / 3
    # Movement
    playerY_change = 0
    playerX_change = 0
    player_movement_speed = 3

    def player(x, y):
        screen.blit(player_img, (x, y))

    # --------------------Enemy------------------------
    # Enemy Details
    enemy_img = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 18
    enemy_height = 32
    enemy_width = 32

    def spawn_enemies():
        image_num = 1
        for i in range(num_of_enemies):
            if image_num > 3:
                image_num = 1
            enemy_img.append(pygame.image.load('images/asteroid' + str(image_num) + '.png'))
            image_num += 1
            # Enemy Movement & Start Point
            Xvelocity = r.randint(3, 7)
            Yvelocity = r.uniform(0,1)
            if i % 2 == 0:
                enemyX.append(-r.randint(1, 40))
            else:
                enemyX.append(width + r.randint(1, 40))
            if i % 5 == 0:
                enemyX[i] = (r.randint(1, width))
                enemyY.append(-r.uniform(0, 40))
                enemyY_change.append(Yvelocity * -1)
            else:
                enemyY.append(height + r.randint(1, 40))
                enemyY_change.append(Yvelocity * 10)
            enemyY.append(r.randint(0, height))
            enemyX_change.append(Xvelocity)


    def asteroids(x, y, index):
        screen.blit(enemy_img[index], (x, y))

    def is_collision(enemyX, enemyY, playerX, playerY, dis):
        distance = math.sqrt((enemyX - playerX) ** 2 + (enemyY - playerY) ** 2)
        if distance < dis:
            return True
        return False

    # -------------------------text----------------------
    def message_to_screen(message, antialias, color, pos=(250, 250)):
        text = over_font.render(message, antialias, color)
        screen.blit(text, pos)

    # -------------------------game mode----------------------
    def paused():
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pause = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            screen.fill('black')
            message_to_screen("PAUSED", True, [232, 232, 232], (200, 200))
            message_to_screen("Press c  to continue", True, [232, 232, 232], (200, 250))
            message_to_screen("Press q  to Quit", True, [232, 232, 232], (200, 300))
            pygame.display.update()

    def game_over():
        gameover = True
        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameover = False
                        main()

                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            screen.fill('black')
            message_to_screen("Game Over", True, [232, 232, 232], (200, 200))
            message_to_screen("Score " + str(score_value), True, [232, 232, 232], (200, 250))
            message_to_screen("Press r  to Restart", True, [232, 232, 232], (200, 300))
            message_to_screen("Press q  to Quit", True, [232, 232, 232], (200, 350))
            pygame.display.update()

    # -------------------------game loop----------------------
    running = True
    spawn_enemies()
    while running:
        # bg-color
        screen.fill('#151515')
        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Movement
            # Player
            # Key down: when the key had been pressed changing the values of X & Y
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    playerX_change += player_movement_speed
                if event.key == pygame.K_LEFT:
                    playerX_change -= player_movement_speed
                if event.key == pygame.K_UP:
                    playerY_change -= player_movement_speed
                if event.key == pygame.K_DOWN:
                    playerY_change += player_movement_speed
                if event.key == pygame.K_SPACE:
                    player_movement_speed += 7
                if event.key == pygame.K_ESCAPE:
                    paused()

            # Key up: the keys unpressed and reset the change values to 0 both for up&down or right&left
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0
                if event.key == pygame.K_SPACE:
                    player_movement_speed -= 7

        # Setting player boundary's for x (whole screen width) and y (half of screen height)
        if 0 <= playerX + playerX_change <= width - player_width:
            playerX += playerX_change
        if 10 <= playerY + playerY_change <= height - player_height:
            playerY += playerY_change

        # Enemy Movement -  Setting enemies boundary's moving from side to side
        for i in range(num_of_enemies):
            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            # change direction
            if enemyX[i] <= -30:
                enemyX_change[i] = abs(enemyX_change[i])
                enemyY[i] = r.randint(0, height - 100)
            elif enemyX[i] >= width + enemy_width:
                enemyX_change[i] = abs(enemyX_change[i]) * -1
                enemyY[i] = r.randint(0, height - 100)

            if is_collision(enemyX[i], enemyY[i], playerX, playerY, 32):
                for j in range(num_of_enemies):
                    enemy_img[j] = 2000
                playerY = 2000
                running = False
                game_over()
                break

            asteroids(enemyX[i], enemyY[i], i)

        if pygame.time.get_ticks() % 60 == 0:
            if score_value % 30 == 0:
                combo += 1
            score_value += 1 * combo

        player(playerX, playerY)
        message_to_screen("Life   3", True, [232, 232, 232], (570, 10))
        show_score(textX, textY)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
