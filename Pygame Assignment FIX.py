import pygame # type: ignore
import random
import time

#==========PYGAME SETUP================

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Assignment")

#==========GAME SETUP================

#colours
WHITE = (255, 255, 255)
SAND = (194, 178, 128)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

#player stats
player_size = 50
enemy_size = 30
player_x = 587
player_y = 387
speed = 5
score = 0
lives = 3

#bullet stats
bullet_speed = 10
bullet_active = False
bullet_cooldown = 300  # Time between shots in milliseconds
last_bullet_time = 0

#enemy stats
enemy_speed = 2.5
enemy_spawn_rate = 0.015

#powerups
selection = 0
extra_life = 0
coffee = 0
slow = 0
slowed = False

powerup_spawn = 0.1

#timer setup + game stats
cont = False
time_limit = 60 #time limit in seconds
start_time = time.time()
running = True
won = False
lvl_2_won = False
clock = pygame.time.Clock()

powerups = []
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




#===========FUNCTION SETUP===========

def enemy_movement (): #enemy movement function that moves the enemies towards the player + checks for collisions with borders
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

def enemy_shooting (): #enemy shooting function that shoots bullets towards the player
    pass
    
def check_cacti_collision(player, cacti_borders): #collision detection function that checks if the player is colliding with any cacti
        for cacti in cacti_borders:
            if player.colliderect(cacti):
                return True
        return False

def enemy_border_collision(enemy, cacti_borders): #collision detection function that checks if the enemy is colliding with any cacti
    for cacti in cacti_borders:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)
        if enemy_rect.colliderect(cacti):
            return True
    return False

def check_border_collision(player, left_border, right_border): #collision detection function that checks if the player is colliding with the left or right border
    if player.colliderect(left_border or right_border):
                return True
    return False

def lose_life(player_x, player_y, lives,bullets, enemies): #function that resets the player position and removes a life
        player_x = 587
        player_y = 387
        bullets.clear()
        enemies.clear()
        return player_x, player_y, lives - 1

def enemy_collision(player, enemies): #collision detection function that checks if the player is colliding with any enemies
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

        if event.type == pygame.KEYDOWN:

            # Select powerup
            if event.key == pygame.K_1 and extra_life > 0:
                selection = 1

            elif event.key == pygame.K_2 and coffee > 0:
                selection = 2

            elif event.key == pygame.K_3 and slow > 0:
                selection = 3

            # Use selected powerup
            elif event.key == pygame.K_SPACE:

                if selection == 1 and extra_life > 0:
                    extra_life -= 1
                    lives += 1
                    selection = 0

                elif selection == 2 and coffee > 0:
                    coffee -= 1
                    selection = 0

                elif selection == 3 and slow > 0:
                    slow -= 1
                    slowed = True
                    selection = 0
    # Get the keys being pressed
    keys = pygame.key.get_pressed()
   
    #==========PLAYER MOVEMENT================
    if not won:

        # Move left
        if keys[pygame.K_a]:
            player_x -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders) == True: #checks collision function, kills player if true
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True: #keeps player in game borders
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

    player_image = pygame.image.load("Character Sprite.png")
    enemy_image = pygame.image.load("temp sprite.jpeg")
    player_image = pygame.transform.scale(player_image, (player_size, player_size))
    enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

    
    #========== TIMER ================
    #https://www.youtube.com/watch?v=juSH7hmYUGA
    elapsed_time = time.time() - start_time
    remaining_time = time_limit - int(elapsed_time)

    #==========DRAWING SECTION================
    #Draw the background
    screen.fill(SAND)

    #Edge borders + cacti borders
    left_border = pygame.draw.rect(screen, BLACK, (0, 0, 200, 10000))
    right_border = pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 200, 0, 200, 10000))
    if not won:
        for cacti in cacti_borders:
            pygame.draw.rect(screen, GREEN, cacti)

    #Score counter
    font = pygame.font.Font(None, 50)
    text_score = font.render(f"Score = {score}", True, WHITE)
    screen.blit(text_score, (20, 20))

    #Lives counter
    font = pygame.font.Font(None, 50)
    text_score = font.render(f"Lives = {lives}", True, WHITE)
    screen.blit(text_score, (20, 100))

    extra_lives_txt = font.render(f"Ex. Life = {extra_life}", True, RED if selection == 1 else WHITE)
    coffee_txt = font.render(f"Coffee = {coffee}", True, RED if selection == 2 else WHITE)
    slow_txt = font.render(f"Slow = {slow}", True, RED if selection == 3 else WHITE)

    screen.blit(extra_lives_txt, (20, 200))
    screen.blit(coffee_txt, (20, 250))
    screen.blit(slow_txt, (20, 300))

    #Player Sprite
    player = pygame.Rect(player_x, player_y, player_size, player_size)
    
    screen.blit(player_image, (player_x, player_y))


   

    

    #Timer Display
    timer = pygame.draw.rect(screen, RED, ( 295, 30, remaining_time * 10, 15))
    timer_background = pygame.draw.rect(screen, WHITE, (295, 30, 600, 15), 2)

    #==========SHOOTING SECTION================
    current_time = pygame.time.get_ticks()
    if current_time - last_bullet_time >= bullet_cooldown: #so that the player can only shoot a bullet every 300 milliseconds
        if keys[pygame.K_UP]:
            bullets.append([player_x, player_y, "up"]) #adds a bullet to the bullets list with the player's current position and direction shooting
            last_bullet_time = current_time #resets cooldown

        elif keys[pygame.K_DOWN]:
            bullets.append([player_x, player_y, "down"])
            last_bullet_time = current_time

        elif keys[pygame.K_LEFT]:
            bullets.append([player_x, player_y, "left"])
            last_bullet_time = current_time

        elif keys[pygame.K_RIGHT]:
            bullets.append([player_x, player_y, "right"])
            last_bullet_time = current_time

    for bullet in bullets: #checks direction of bullet and moves it accordingly
        if bullet[2] == "up": 
            bullet[1] -= bullet_speed
        elif bullet[2] == "down":
            bullet[1] += bullet_speed
        elif bullet[2] == "left":
            bullet[0] -= bullet_speed
        elif bullet[2] == "right":
            bullet[0] += bullet_speed

        pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], 15, 15)) #draws the bullet on the screen

    #only keeps bullets that are within the screen boundaries, removes bullets that go off-screen
    bullets = [bullet for bullet in bullets if 200 < bullet[0] < 1000-15 and 0 < bullet[1] < SCREEN_HEIGHT]

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

    if remaining_time <= 30:
        enemy_spawn_rate = 0.02

    if not won: #only spawns enemies if the player has not won yet
        if random.random() < enemy_spawn_rate and len(enemies) < 5: #restricts the number of enemies on screen to 5
            spawn_location = random.choice(enemy_spawn_locations) #picks which side to spawn enemy at
            enemy_x = spawn_location[0]
            enemy_y = spawn_location[1]
            enemies.append([enemy_x, enemy_y]) #adds the enemy to the enemies list with the spawn location

        enemy_movement () #calls enemy movement function to move the enemies towards the player

            
        for enemy in enemies: #enemy + bullet collision
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30) #creates hitbox for the enemy to check for collisions

            
            for bullet in bullets: #creates hitbox for the bullet to check for collisions with the enemy
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 15, 15)

                if bullet_rect.colliderect(enemy_rect): #checks if the bullet is colliding with the enemy, if so, removes both the bullet and the enemy and adds 1 to the score
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1

                    #powerup spawn
                    if random.random() < powerup_spawn and len(powerups) <= 10:
                        if random.randint(1,100) > 1 and random.randint(1,100) < 20 and len(powerups) <= 10:
                            powerups.append([enemy[0], enemy[1], "extra_life"])
                        if random.randint(1,100) > 20 and random.randint(1,100) < 60 and len(powerups) <= 10:
                            powerups.append([enemy[0], enemy[1], "coffee"])
                        if random.randint(1,100) > 60 and random.randint(1,100) < 100 and len(powerups) <= 10:
                            powerups.append([enemy[0], enemy[1], "slow"])
                    
            screen.blit(enemy_image, (enemy[0], enemy[1]))


    if enemy_collision(player, enemies) == True: #enemy + player collision
        player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
    
    #========== POWER-UPS ==========
    
    for powerup in powerups[:]: # Iterate over a copy of the list to avoid modifying it while iterating
        powerup_rect = pygame.Rect(powerup[0], powerup[1], 20, 20)
        # Draw powerup
        pygame.draw.rect(screen, WHITE, powerup_rect)

        # Check if player collects powerup
        if player.colliderect(powerup_rect):
            if powerup[2] == "extra_life":
                extra_life += 1
            elif powerup[2] == "coffee":
                coffee += 1
            elif powerup[2] == "slow":
                slow += 1
            powerups.remove(powerup)

    if slowed == True:
            for enemy in enemies:
                tinted_sprite = enemy_image.copy()
                tinted_sprite.fill((82, 105, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted_sprite, (enemy[0], enemy[1]))

                enemy_speed = 1.5
                if time.time() - start_time >= 10:  # Check if 10 seconds have passed since the slow effect started
                    slowed = False  # Reset the slowed state
                    enemy_speed = 2.5  # Reset enemy speed to normal



    # ======== END ========
   
    if remaining_time <= 0: #checks if the time runs out and if so, the player has won
        won = True
        font = pygame.font.Font(None, 100)

        #level complete text
        level_complete = font.render("You Completed This Level!", True, GREEN)
        screen.blit(level_complete, (SCREEN_WIDTH // 2 - level_complete.get_width() // 2, SCREEN_HEIGHT // 2 - level_complete.get_height() // 2))
        level_continue = font.render("Press SPACE to Continue", True, GREEN)
        screen.blit(level_continue, (SCREEN_WIDTH // 2 - level_continue.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        if keys[pygame.K_SPACE]:#checks if the player presses space to continue to the next level
            cont = True
            lvl_2_won = False

            #reset game stats for next level
            score = 0
            bullets.clear()
            enemies.clear()
            player_x = 587
            player_y = 387
            time_remaining = time_limit
            start_time = time.time()


#======== LEVEL 2 PLAYER MOVEMENT ========
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
                        
       #======== LVL 2 TIMER ======== 
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - int(elapsed_time)

        

   
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
        
    timer = pygame.draw.rect(screen, RED, ( 295, 30, remaining_time * 10, 15))
    timer_background = pygame.draw.rect(screen, WHITE, (295, 30, 600, 15), 2)
       

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