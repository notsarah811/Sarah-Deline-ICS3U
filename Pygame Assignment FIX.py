import re

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

player_size = 50
enemy_size = 30
player_x = 587
player_y = 387
speed = 5
bullet_speed = 10
bullet_active = False
bullet_cooldown = 300  # Time between shots in milliseconds
last_bullet_time = 0
enemy_speed = 2.5
score = 0
lives = 3
cont = False

v = pygame.draw.polygon(screen, (255, 0, 0), [(200, 0), (500, 0), (500, 50), (250, 50)], 250)

cacti_borders = [
    (200, 0, 300, 50),
    (200, 0, 50, 300),
    (700, 0 , 300, 50),
    (950, 50, 50, 250),
    (200, 750, 300, 50),
    (200, 500, 50, 300),
    (700, 750, 300, 50),
    (950, 500, 50, 300)
]

cacti_pillars = [
    (400, 200, 80, 80),
    (720, 200, 80, 80),
    (400, 520, 80, 80),
    (720, 520, 80, 80)
]

bullets = []

enemies = []
enemy_spawn_locations = [
    (200, 400),
    (600, 0),
    (970, 400),
    (600, 770)
]

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

        # Move horizontally
        if enemy_x < player_x:
            enemy[0] += enemy_speed
        elif enemy_x > player_x:
            enemy[0] -= enemy_speed

        if enemy_border_collision(enemy, cacti_borders):
            enemy[0] = enemy_x

        # Update enemy position
        enemy_x = enemy[0]
        enemy_y = enemy[1]

        # Move vertically
        if enemy_y < player_y:
            enemy[1] += enemy_speed
        elif enemy_y > player_y:
            enemy[1] -= enemy_speed

        if enemy_border_collision(enemy, cacti_borders):
            enemy[1] = enemy_y

def enemy_shooting ():
    pass
    
def check_cacti_collision(player, cacti_borders):
        for cacti in cacti_borders:
            if player.colliderect(cacti):
                return True
        return False

def enemy_border_collision(enemy, cacti_borders):
    for cacti in cacti_borders:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)
        if enemy_rect.colliderect(cacti):
            return True
    return False

def check_border_collision(player, left_border, right_border):
    if player.colliderect(left_border or right_border):
                return True
    return False

def lose_life(player_x, player_y, lives,bullets, enemies):
        player_x = 587
        player_y = 387
        bullets.clear()
        enemies.clear()
        return player_x, player_y, lives - 1

def enemy_collision(player, enemies):
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)
        if player.colliderect(enemy_rect):
            return True
    return False

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
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_x += speed
            

        # Move right
        if keys[pygame.K_d]:
            player_x += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_x -= (speed)
            
        # Move up
        if keys[pygame.K_w]:
            player_y -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_y += (speed)
                        
                
        # Move down
        if keys[pygame.K_s]:
            player_y += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_y -= (speed)
                        
   
   # Keep the player within the screen boundaries
    if player_x < 200:
        player_x = 200

    if player_x > 1000 - player_size:
        player_x = 1000 - player_size

    if player_y < 0:
        player_y = 0

    if player_y > SCREEN_HEIGHT - player_size:
        player_y = SCREEN_HEIGHT - player_size

        # Update the player rectangle
    player = pygame.Rect(player_x, player_y, player_size, player_size)

    player_image = pygame.image.load("temp sprite.jpeg")
    enemy_image = pygame.image.load("temp sprite.jpeg")
    player_image = pygame.transform.scale(player_image, (player_size, player_size))
    enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))





    
    # Draw the background
    screen.fill(SAND)

    #==========DRAWING SECTION================
    
    left_border = pygame.draw.rect(screen, BLACK, (0, 0, 200, 10000))
    right_border = pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 200, 0, 200, 10000))
    if not won:
        for cacti in cacti_borders:
            pygame.draw.rect(screen, GREEN, cacti)

    font = pygame.font.Font(None, 50)
    text_score = font.render(f"Score = {score}", True, WHITE)
    screen.blit(text_score, (20, 20))

    font = pygame.font.Font(None, 50)
    text_score = font.render(f"Lives = {lives}", True, WHITE)
    screen.blit(text_score, (20, 100))

    player = pygame.Rect(player_x, player_y, player_size, player_size)
    screen.blit(player_image, (player_x, player_y))

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
        random_enemy_spawn_chance = 0.015  # 1.5% chance to spawn an enemy each frame
        if random.random() < random_enemy_spawn_chance and len(enemies) < 5:
            spawn_location = random.choice(enemy_spawn_locations)
            enemy_x = spawn_location[0]
            enemy_y = spawn_location[1]
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
                    
            screen.blit(enemy_image, (enemy[0], enemy[1]))

    if enemy_collision(player, enemies) == True:
        player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)

    # ======== END ========
   
    if score >= 10:
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
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_x += speed
            

        # Move right
        if keys[pygame.K_d]:
            player_x += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_x -= (speed)
            
        # Move up
        if keys[pygame.K_w]:
            player_y -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_y += (speed)
                        
                
        # Move down
        if keys[pygame.K_s]:
            player_y += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_y -= (speed)
                        
   
   # Keep the player within the screen boundaries
    if player_x < 200:
        player_x = 200

    if player_x > 1000 - player_size:
        player_x = 1000 - player_size

    if player_y < 0:
        player_y = 0

    if player_y > SCREEN_HEIGHT - player_size:
        player_y = SCREEN_HEIGHT - player_size

        # Update the player rectangle
    player = pygame.Rect(player_x, player_y, player_size, player_size)

    if won == True and not lvl_2_won:
        for cacti in cacti_borders:
                    pygame.draw.rect(screen, GREEN, cacti)
        for cactus in cacti_pillars:
            pygame.draw.rect(screen, GREEN, cactus)
        
        
       

    if won == True and cont == True and not lvl_2_won:
        random_enemy_spawn_chance = 0.015  # 1.5% chance to spawn an enemy each frame
        if random.random() < random_enemy_spawn_chance and len(enemies) < 5:
            spawn_location = random.choice(enemy_spawn_locations)
            enemy_x = spawn_location[0]
            enemy_y = spawn_location[1]
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
#
# Close Pygame
pygame.quit()