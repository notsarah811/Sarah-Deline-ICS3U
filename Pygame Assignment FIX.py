import pygame # type: ignore
import random

#==========PYGAME SETUP================

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Assignment")

#==========GAME SETUP================

WHITE = (255, 255, 255)
SAND = (194, 178, 128)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)


player_size = 25
player_x = 587
player_y = 387
speed = 5
bullet_speed = 10
bullet_active = False
bullet_cooldown = 300  # Time between shots in milliseconds
last_bullet_time = 0
enemy_speed = 1.5
score = 0
cont = False

v = pygame.draw.polygon(screen, (255, 0, 0), [(200, 0), (500, 0), (500, 50), (250, 50)], 250)


cacti_borders = [
    [(200, 0), (500, 0), (500, 50), (250, 50), (250, 300), (200, 300)],
    [(1000, 0), (700, 0), (700, 50), (950, 50), (950, 300), (1000, 300)],
    [(200, 800), (500, 800), (500, 750), (250, 750), (250, 500), (200, 500)],
    [(1000, 800), (700, 800), (700, 750), (950, 750), (950, 500), (1000, 500)],
]

cacti_pillars = [
    (400, 200, 80, 80),
    (720, 200, 80, 80),
    (400, 520, 80, 80),
    (720, 520, 80, 80)
]

bullets = []

enemies = []


walls = 0


running = True
won = False
lvl_2_won = False
clock = pygame.time.Clock()

#===========FUNCTION SETUP===========

def enemy_movement ():
    for enemy in enemies:
                enemy_x = enemy[0]
                enemy_y = enemy[1]
    
                if enemy_x < player_x:
                    enemy[0] += enemy_speed
                elif enemy_x > player_x:
                    enemy[0] -= enemy_speed
    
                if enemy_y < player_y:
                    enemy[1] += enemy_speed
                elif enemy_y > player_y:
                    enemy[1] -= enemy_speed

def enemy_shooting ():
    pass
    

#==========GAME LOOP================
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys being pressed
    keys = pygame.key.get_pressed()

    #Collision detection function
   

    if not won:

        # Move left
        if keys[pygame.K_a]:
            player_x -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            

        # Move right
        if keys[pygame.K_d]:
            player_x += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            
        # Move up
        if keys[pygame.K_w]:
            player_y -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            
                
        # Move down
        if keys[pygame.K_s]:
            player_y += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            
   
   # Keep the player within the screen boundaries
    if player_x < 0:
        player_x = 0

    if player_x > SCREEN_WIDTH - player_size:
        player_x = SCREEN_WIDTH - player_size

    if player_y < 0:
        player_y = 0

    if player_y > SCREEN_HEIGHT - player_size:
        player_y = SCREEN_HEIGHT - player_size

        # Update the player rectangle
    player = pygame.Rect(player_x, player_y, player_size, player_size)

    
    # Draw the background
    screen.fill(SAND)

    #==========DRAWING SECTION================
    
    left_border = pygame.draw.rect(screen, BLACK, (0, 0, 200, 10000))
    right_border = pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 200, 0, 200, 10000))
    if not won:
        for cacti in cacti_borders:
            pygame.draw.polygon(screen, GREEN, cacti)

    font = pygame.font.Font(None, 50)
    text_score = font.render(f"Score = {score}", True, WHITE)
    screen.blit(text_score, (20, 20))

    player = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.rect(screen, RED, player)

    #==========SHOOTING SECTION================
    current_time = pygame.time.get_ticks()
    if current_time - last_bullet_time >= bullet_cooldown:
        if keys[pygame.K_UP]:
            bullets.append([player_x, player_y, "up"])
            last_bullet_time = current_time

        elif keys[pygame.K_DOWN]:
            bullets.append([player_x, player_y, "down"])
            last_bullet_time = current_time

        elif keys[pygame.K_LEFT]:
            bullets.append([player_x, player_y, "left"])
            last_bullet_time = current_time

        elif keys[pygame.K_RIGHT]:
            bullets.append([player_x, player_y, "right"])
            last_bullet_time = current_time

    for bullet in bullets:

        if bullet[2] == "up":
            bullet[1] -= bullet_speed

        elif bullet[2] == "down":
            bullet[1] += bullet_speed

        elif bullet[2] == "left":
            bullet[0] -= bullet_speed

        elif bullet[2] == "right":
            bullet[0] += bullet_speed

        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], 15, 15))

    bullets = [bullet for bullet in bullets if
            200 < bullet[0] < 1000-15 and
            0 < bullet[1] < SCREEN_HEIGHT]

    """ In case above method isn't allowed, this code can be used. It is currently commented out.

    if keys[pygame.K_UP]:
        bullet_direction = "up"
        if not bullet_active:
                    # Reset bullet position to the player's position when fired
                    bullet_x = player_x  # Adjust as needed to center it
                    bullet_y = player_y
                    bullet_active = True
    elif keys[pygame.K_DOWN]:
        bullet_direction = "down"
        if not bullet_active:
                    # Reset bullet position to the player's position when fired
                    bullet_x = player_x  # Adjust as needed to center it
                    bullet_y = player_y
                    bullet_active = True
    elif keys[pygame.K_LEFT]:
        bullet_direction = "left"
        if not bullet_active:
                    # Reset bullet position to the player's position when fired
                    bullet_x = player_x  # Adjust as needed to center it
                    bullet_y = player_y
                    bullet_active = True
    elif keys[pygame.K_RIGHT]:
        bullet_direction = "right"
        if not bullet_active:
                    # Reset bullet position to the player's position when fired
                    bullet_x = player_x  # Adjust as needed to center it
                    bullet_y = player_y
                    bullet_active = True


    if bullet_active:
        if bullet_direction == "up":
            bullet_y -= bullet_speed
        elif bullet_direction == "down":
            bullet_y += bullet_speed
        elif bullet_direction == "left":
            bullet_x -= bullet_speed
        elif bullet_direction == "right":
            bullet_x += bullet_speed

        # Check boundaries (If it goes off-screen, deactivate it)
    if bullet_x >= SCREEN_WIDTH or bullet_y >= SCREEN_HEIGHT or bullet_y <= 0 or bullet_x <= 0:                      
        bullet_active = False

    if bullet_active:
        pygame.draw.rect(screen, BLUE, (bullet_x, bullet_y, 15, 15)) 

        bullet_rect = pygame.Rect(bullet_x,bullet_y,15,15)

    """


    # ======== ENEMY SECTION ========
    # Enemy movement and behavior can be added here

    if not won:
        random_enemy_spawn_chance = 0.01  # 1% chance to spawn an enemy each frame
        if random.random() < random_enemy_spawn_chance and len(enemies) < 5:  # Limit the number of enemies on screen
            enemy_x = random.randint(200, SCREEN_WIDTH - 200 - 30)  # Enemy width is 30
            enemy_y = random.randint(0, SCREEN_HEIGHT - 30)  # Enemy height is 30
            enemies.append([enemy_x, enemy_y])

        enemy_movement ()

            
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)

            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 15, 15)

                if bullet_rect.colliderect(enemy_rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    
            pygame.draw.rect(screen, BLACK, (enemy[0], enemy[1], 30, 30))

    # ======== END ========
   
    if score >= 5:
        won = True
        font = pygame.font.Font(None, 100)
        level_complete = font.render("You Completed This Level!", True, GREEN)
        screen.blit(level_complete, (SCREEN_WIDTH // 2 - level_complete.get_width() // 2, SCREEN_HEIGHT // 2 - level_complete.get_height() // 2))
        level_continue = font.render("Press SPACE to Continue", True, GREEN)
        screen.blit(level_continue, (SCREEN_WIDTH // 2 - level_continue.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        if keys[pygame.K_SPACE]:
            cont = True
            lvl_2_won = False
            score = 0
            bullets.clear()
            enemies.clear()
            player_x = 587
            player_y = 387

    if not lvl_2_won:
            # Move left
            if keys[pygame.K_a]:
                player_x -= speed
                player = pygame.Rect(player_x, player_y, player_size, player_size)
                
    
            # Move right
            if keys[pygame.K_d]:
                player_x += speed
                player = pygame.Rect(player_x, player_y, player_size, player_size)
                
            # Move up
            if keys[pygame.K_w]:
                player_y -= speed
                player = pygame.Rect(player_x, player_y, player_size, player_size)
                
                    
            # Move down
            if keys[pygame.K_s]:
                player_y += speed
                player = pygame.Rect(player_x, player_y, player_size, player_size)

    if won == True and not lvl_2_won:
        for cacti in cacti_borders:
            pygame.draw.polygon(screen, GREEN, cacti)
        # Replace line 323 with a loop:
        for cactus in cacti_pillars:
            pygame.draw.rect(screen, GREEN, cactus)
        
        
        #cacti_border_ctl = pygame.draw.rect(screen, GREEN, (400, 200, 80, 80))
        #cacti_border_ctr = pygame.draw.rect(screen, GREEN, (720, 200, 80, 80))
        #cacti_border_cbl = pygame.draw.rect(screen, GREEN, (400, 520, 80, 80))
        #cacti_border_cbr = pygame.draw.rect(screen, GREEN, (720, 520, 80, 80))

    if won == True and cont == True and not lvl_2_won:
        random_enemy_spawn_chance = 0.01  # 1% chance to spawn an enemy each frame
        if random.random() < random_enemy_spawn_chance and len(enemies) < 5:  # Limit the number of enemies on screen
            enemy_x = random.randint(200, SCREEN_WIDTH - 200 - 30)  # Enemy width is 30
            enemy_y = random.randint(0, SCREEN_HEIGHT - 30)  # Enemy height is 30
            enemies.append([enemy_x, enemy_y])
    
        enemy_movement ()
    
                
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)
    
            for bullet in bullets:
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 15, 15)
    
                if bullet_rect.colliderect(enemy_rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                        
            pygame.draw.rect(screen, BLACK, (enemy[0], enemy[1], 30, 30))    


    # Update the display
    pygame.display.flip()

    # Limit the game to 60 FPS
    clock.tick(60)

# Close Pygame
pygame.quit()