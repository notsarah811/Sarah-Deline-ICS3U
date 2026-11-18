import pygame # type: ignore
import random
import time

#==========PYGAME SETUP================

pygame.init()
pygame.mixer.init()

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
speed = 3.5
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
rapid_fire = 0
round_shot = 0
slow = 0
gold = 0

coffee_active = False
coffee_start_time = 0

rapid_fire_active = False
rapid_fire_start_time = 0

round_shot_active = False
round_shot_start_time = 0

slowed = False
slow_start_time = 0

powerup_spawn = 0.1

#music
current_music = ""
volume_level = 50
pygame.mixer.music.set_volume(volume_level / 100)
volume_slider_min = 414
volume_slider_max = 605
volume_slider_y = 565
volume_slider_x = 509

#start screen
main_menu = True
game_started = False
settings_menu = False
how_to_play_menu = False



#timer setup + game stats
cont = False
time_limit = 60 #time limit in seconds
start_time = time.time()
running = True
passing = False
lvl_1_won = False
lvl_2_won = False
game_won = False
game_lost = False
clock = pygame.time.Clock()

bottom_border = pygame.Rect(0, 795, 1200, 5)

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

extra_lives_img = pygame.image.load("Extra Lives.png")
extra_lives_img = pygame.transform.scale(extra_lives_img, (50, 50))

coffee_img = pygame.image.load("Coffee.png")
coffee_img = pygame.transform.scale(coffee_img, (50, 50))

rapid_fire_img = pygame.image.load("Rapid Fire.png")
rapid_fire_img = pygame.transform.scale(rapid_fire_img, (50, 50))

round_shot_img = pygame.image.load("Round Shot.png")
round_shot_img = pygame.transform.scale(round_shot_img, (50, 50))

slow_img = pygame.image.load("Slow.png")
slow_img = pygame.transform.scale(slow_img, (50, 50))

selection_img = pygame.image.load("Selection.png")
selection_img = pygame.transform.scale(selection_img, (60, 60))



texture = pygame.image.load("sand texture.png")
texture = pygame.transform.scale(texture, (300, 300))
cacti_texture = pygame.image.load("cactus 4.png")
cacti_texture = pygame.transform.scale(cacti_texture, (50, 50))



left_bullet = pygame.image.load("Lbullet.png")
up_bullet = pygame.image.load("Ubullet.png")
right_bullet = pygame.image.load("Rbullet.png")
down_bullet = pygame.image.load("Dbullet.png")

left_bullet = pygame.transform.scale(left_bullet, (25, 20))
up_bullet = pygame.transform.scale(up_bullet, (20, 25))
right_bullet = pygame.transform.scale(right_bullet, (25, 20))
down_bullet = pygame.transform.scale(down_bullet, (20, 25))




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
    
def check_cacti_collision(player, cacti_borders, cacti_pillars): #collision detection function that checks if the player is colliding with any cacti
        for cacti in cacti_borders:
            if player.colliderect(cacti):
                return True
        if lvl_1_won == True:
            for cacti in cacti_pillars:
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

def draw_background():

    for x in range(0, SCREEN_WIDTH, 300):
        for y in range(0, SCREEN_HEIGHT, 300):

            screen.blit(texture, (x, y))

def draw_cacti_borders(): 
    for cacti in cacti_borders:
        for x in range(cacti[0], cacti[0] + cacti[2], 50):
            for y in range(cacti[1], cacti[1] + cacti[3], 50):
                screen.blit(cacti_texture, (x, y))

    if lvl_1_won:
        for cacti in cacti_pillars:
            for x in range(cacti[0], cacti[0] + cacti[2], 50):
                        for y in range(cacti[1], cacti[1] + cacti[3], 50):
                            screen.blit(cacti_texture, (x, y))

#==========GAME LOOP================
while running:

    #======== MUSIC =========
    if game_started == False:
        music_choice = "Menu Music.mp3"

    elif game_won == True:
        music_choice = "Victory Music.mp3"

    else:
        music_choice = "Game Music.mp3"

    if music_choice != current_music:
        pygame.mixer.music.load(music_choice)
        pygame.mixer.music.play(-1)
        current_music = music_choice

    pygame.mixer.music.set_volume(volume_level / 100)
    #========= SETUP ==========
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
                
            elif event.key == pygame.K_3 and rapid_fire > 0:
                selection = 3
                
            elif event.key == pygame.K_4 and round_shot > 0:
                selection = 4
               
            elif event.key == pygame.K_5 and slow > 0:
                selection = 5
                
            # Use selected powerup
            elif event.key == pygame.K_SPACE:

                if selection == 1 and extra_life > 0:
                    extra_life -= 1
                    lives += 1
                    selection = 0

                elif selection == 2 and coffee > 0:
                    coffee -= 1
                    selection = 0
                    coffee_active = True
                    coffee_start_time = time.time()

                elif selection == 3 and rapid_fire > 0:
                    rapid_fire -= 1
                    selection = 0
                    rapid_fire_active = True
                    rapid_fire_start_time = time.time()

                elif selection == 4 and round_shot > 0:
                    round_shot -= 1
                    selection = 0
                    round_shot_active = True
                    round_shot_start_time = time.time()

                elif selection == 5 and slow > 0:
                    slow -= 1
                    slowed = True
                    slow_start_time = time.time()
                    selection = 0
    # Get the keys being pressed
    keys = pygame.key.get_pressed()
   

    if game_started == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True

    #========= TITLE SCREEN ==========
    if main_menu == True and game_started == False:

        screen.fill(SAND)
        title_screen_image = pygame.image.load("Title Screen.png")
        title_screen_image = pygame.transform.scale(title_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(title_screen_image, (0, 0))

        play_button = pygame.Rect(413, 365, 376, 78)
        settings_button = pygame.Rect(413, 463, 376, 68)
        how_to_play_button = pygame.Rect(413, 548, 376, 67)
        quit_button = pygame.Rect(413, 631, 376, 68)

        if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        game_started = True
                        main_menu = False
                        start_time = time.time()
                    elif settings_button.collidepoint(event.pos):
                        settings_menu = True
                        main_menu = False
                    elif how_to_play_button.collidepoint(event.pos):
                        how_to_play_menu = True
                        main_menu = False
                    elif quit_button.collidepoint(event.pos):
                        running = False

    #========= SETTINGS SCREEN ==========
    if settings_menu:
        screen.fill(SAND)

        settings_screen = pygame.image.load("Settings Menu.png")
        settings_screen = pygame.transform.scale(settings_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(settings_screen, (0, 0))

        volume_slider = pygame.image.load("Volume Slider.png")
        volume_slider = pygame.transform.scale(volume_slider, (50, 75))
        screen.blit(volume_slider, (volume_slider_x, volume_slider_y))

        # Close (X) button
        exit_button = pygame.Rect(1090, 15, 95, 100)

        # Volume decrease button
        volume_down_button = pygame.Rect(200, 575, 55, 55)

        # Volume increase button
        volume_up_button = pygame.Rect(650, 575, 55, 55)

        # Quit button
        quit_button = pygame.Rect(758, 547, 252, 90)

        # Back button
        back_button = pygame.Rect(454, 662, 292, 70)
        if event.type == pygame.MOUSEBUTTONDOWN:

            if exit_button.collidepoint(event.pos):
                settings_menu = False
                main_menu = True

            elif settings_menu:
                if volume_down_button.collidepoint(event.pos):
                    if volume_level > 0 and volume_slider_x > volume_slider_min:
                        volume_slider_x -= 10
                        volume_level -= 1
                        

                elif volume_up_button.collidepoint(event.pos):
                    if volume_level < 100 and volume_slider_x < volume_slider_max:
                        volume_slider_x += 10
                        volume_level += 1

            # Update slider position
            
            screen.blit(volume_slider, (volume_slider_x, volume_slider_y))

            if quit_button.collidepoint(event.pos):
                running = False

            elif back_button.collidepoint(event.pos):
                settings_menu = False
                main_menu = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                settings_menu = False
                main_menu = True

    #========= HOW TO PLAY SCREEN ==========
    if how_to_play_menu:
        screen.fill(SAND)
        exit_button = pygame.Rect(1085, 20, 125, 125)

        how_to_play_screen = pygame.image.load("How to Play.png")
        how_to_play_screen = pygame.transform.scale(how_to_play_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(how_to_play_screen, (0, 0))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.collidepoint(event.pos):
                how_to_play_menu = False
                main_menu = True

    if game_started == True:
        

        #==========PLAYER MOVEMENT================

            # Move left
        if keys[pygame.K_a]:
            player_x -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders, cacti_pillars) == True: #checks collision function, kills player if true
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True: #keeps player in game borders
                player_x += speed

            # Move right
        if keys[pygame.K_d]:
            player_x += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders, cacti_pillars) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_x -= (speed)
                
            # Move up
        if keys[pygame.K_w]:
            player_y -= speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders, cacti_pillars) == True:
                player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
            if check_border_collision(player, left_border, right_border) == True:
                player_y += (speed)        
                    
            # Move down
        if keys[pygame.K_s]:
            player_y += speed
            player = pygame.Rect(player_x, player_y, player_size, player_size)
            if check_cacti_collision(player, cacti_borders, cacti_pillars) == True:
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
        enemy_image = pygame.image.load("Enemy Sprite.webp")
        player_image = pygame.transform.scale(player_image, (player_size, player_size))
        enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

        
        #========== TIMER ================
        #https://www.youtube.com/watch?v=juSH7hmYUGA
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - int(elapsed_time)

        #==========DRAWING SECTION================
        #-----Fonts-----
        little_font = pygame.font.SysFont("georgia", 20, bold=True)
        main_font = pygame.font.SysFont("georgia", 30, bold=True)
        title_font = pygame.font.SysFont("impact", 40,)


        #-----Draw the background-----
        screen.fill(SAND)
        draw_background()

        #-----Edge borders + cacti borders-----
        left_border = pygame.draw.rect(screen, BLACK, (0, 0, 200, 10000))
        right_border = pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 200, 0, 200, 10000))  
        draw_cacti_borders()
            
        #-----Score counter-----
        text_score = main_font.render(f"Score = {score}", True, WHITE)
        screen.blit(text_score, (20, 20))

        #-----Lives counter-----
        text_score = main_font.render(f"Lives = {lives}", True, WHITE)
        screen.blit(text_score, (20, 75))


        #-----Powerup Counters-----
        #Ex Lives
        screen.blit(extra_lives_img, (20, 200))
        extra_lives_counter = little_font.render(f"{extra_life}", True, WHITE)
        screen.blit(extra_lives_counter, (65, 250))

        #Coffee
        screen.blit(coffee_img, (20, 275))
        coffee_counter = little_font.render(f"{coffee}", True, WHITE)
        screen.blit(coffee_counter, (65, 325))

        #Rapid Fire
        screen.blit(rapid_fire_img, (20, 350))
        rapid_fire_counter = little_font.render(f"{rapid_fire}", True, WHITE)
        screen.blit(rapid_fire_counter, (65, 400))

        #Round Shot
        screen.blit(round_shot_img, (20, 425))
        round_shot_counter = little_font.render(f"{round_shot}", True, WHITE)
        screen.blit(round_shot_counter, (65, 475))

        #Slow
        screen.blit(slow_img, (20, 500))
        slow_counter = little_font.render(f"{slow}", True, WHITE)
        screen.blit(slow_counter, (65, 550))



        #-----Player Sprite-----
        player = pygame.Rect(player_x, player_y, player_size, player_size)
        
        screen.blit(player_image, (player_x, player_y))


        #------Timer Display-----
        if not lvl_1_won and not game_lost:
            timer = pygame.draw.rect(screen, RED, ( 305, 30, remaining_time * 10, 15))
            timer_background = pygame.draw.rect(screen, WHITE, (305, 30, 600, 15), 2)



       
        
        

        #==========SHOOTING SECTION================
        if round_shot_active == True:
            if time.time() - round_shot_start_time >= 10:
                round_shot_active = False
        
        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time >= bullet_cooldown: #so that the player can only shoot a bullet every 300 milliseconds
            if round_shot_active == True:
                if time.time() - round_shot_start_time < 10:
                    if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:

                        bullets.append([player_x + 5, player_y, "up"])
                        bullets.append([player_x - 5, player_y, "up"])

                        bullets.append([player_x + 5, player_y, "down"])
                        bullets.append([player_x - 5, player_y, "down"])

                        bullets.append([player_x, player_y + 5, "left"])
                        bullets.append([player_x, player_y - 5, "left"])

                        bullets.append([player_x, player_y + 5, "right"])
                        bullets.append([player_x, player_y - 5, "right"])

                        last_bullet_time = current_time
                else: round_shot_active = False
            
            else: 
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
                screen.blit((up_bullet), (bullet[0], bullet[1],))
            elif bullet[2] == "down":
                bullet[1] += bullet_speed
                screen.blit((down_bullet), (bullet[0], bullet[1],))
            elif bullet[2] == "left":
                bullet[0] -= bullet_speed
                screen.blit((left_bullet), (bullet[0], bullet[1],))
            elif bullet[2] == "right":
                bullet[0] += bullet_speed
                screen.blit((right_bullet), (bullet[0], bullet[1],))


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

        if not lvl_1_won and not game_lost: #only spawns enemies if the player has not won yet
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
                        if random.random() < powerup_spawn and len(powerups) < 10:
                            powerup_number = random.randint(1, 100)

                            if powerup_number <= 20:
                                powerups.append([enemy[0], enemy[1], "extra_life"])
                            elif powerup_number <= 40:
                                powerups.append([enemy[0], enemy[1], "coffee"])
                            elif powerup_number <= 60:
                                powerups.append([enemy[0], enemy[1], "rapid_fire"])
                            elif powerup_number <= 80:
                                powerups.append([enemy[0], enemy[1], "round_shot"])
                            else:
                                powerups.append([enemy[0], enemy[1], "slow"])
                screen.blit(enemy_image, (enemy[0], enemy[1]))

                if slowed == True:
                    for enemy in enemies:
                                    tinted_sprite = enemy_image.copy()
                                    tinted_sprite.fill((82, 105, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
                                    screen.blit(tinted_sprite, (enemy[0], enemy[1]))
                    


        if enemy_collision(player, enemies) == True: #enemy + player collision
            player_x, player_y,lives = lose_life(player_x,player_y,lives,bullets, enemies)
        
        #========== POWER-UPS ==========
        
        if selection == 1:
            screen.blit(selection_img, (15, 195))

        elif selection == 2:
            screen.blit(selection_img, (15, 270))

        elif selection == 3:
            screen.blit(selection_img, (15, 345))

        elif selection == 4:
            screen.blit(selection_img, (15, 420))

        elif selection == 5:
            screen.blit(selection_img, (15, 495))

        for powerup in powerups[:]: # Iterate over a copy of the list to avoid modifying it while iterating
            powerup_rect = pygame.Rect(powerup[0], powerup[1], 20, 20)
            if powerup[2] == "extra_life":
                extra_lives_drop = pygame.transform.scale(extra_lives_img, (20, 20))
                screen.blit(extra_lives_drop, (powerup[0], powerup[1]))
            elif powerup[2] == "coffee":
                coffee_drop = pygame.transform.scale(coffee_img, (20, 20))
                screen.blit(coffee_drop, (powerup[0], powerup[1]))
            elif powerup[2] == "rapid_fire":
                rapid_fire_drop = pygame.transform.scale(rapid_fire_img, (20, 20))
                screen.blit(rapid_fire_drop, (powerup[0], powerup[1]))
            elif powerup[2] == "round_shot":
                round_shot_drop = pygame.transform.scale(round_shot_img, (20, 20))
                screen.blit(round_shot_drop, (powerup[0], powerup[1]))
            elif powerup[2] == "slow":
                slow_drop = pygame.transform.scale(slow_img, (20, 20))
                screen.blit(slow_drop, (powerup[0], powerup[1]))

            # Check if player collects powerup
            if player.colliderect(powerup_rect):
                if powerup[2] == "extra_life":
                    extra_life += 1
                elif powerup[2] == "coffee":
                    coffee += 1
                elif powerup[2] == "rapid_fire":
                    rapid_fire += 1
                elif powerup[2] == "round_shot":
                    round_shot += 1
                elif powerup[2] == "slow":
                    slow += 1
                powerups.remove(powerup)


        if coffee_active == True:
            if time.time() - coffee_start_time < 10:
                speed = 5
            else:
                coffee_active = False
                speed = 3.5  
        else:
            speed = 3.5

        if rapid_fire_active == True:
            if time.time() - rapid_fire_start_time < 10:
                bullet_cooldown = 150
                bullet_speed = 40
            else:
                rapid_fire_active = False
                bullet_cooldown = 300
                bullet_speed = 10
        else:
            bullet_cooldown = 300
            bullet_speed = 10

        
                        
            

        if slowed == True:
            if time.time() - slow_start_time < 10:
                enemy_speed = 1.5
            else:
                slowed = False
                enemy_speed = 2.5  
        else:
            enemy_speed = 2.5  # Reset enemy speed to normal if not slowed
            
        # ======== END LVL 1 ========
    
        if remaining_time <= 0 and lvl_1_won == False and lvl_2_won == False and game_lost == False: #checks if the time runs out and if so, the player has won
            lvl_1_won = True
            passing = True
            gold = score / 10
            round (gold)
            score = 0
            bullets.clear()
            enemies.clear()
            player_x = 587
            player_y = 387
            
        if lvl_1_won == True and passing == True and lvl_2_won == False and game_lost == False:
            #level complete text
            level_complete = title_font.render("LEVEL COMPLETE!", True, BLACK)
            screen.blit(level_complete, (475, 50))

            continue_arrow = pygame.image.load("Down Arrow.png")
            continue_arrow = pygame.transform.scale(continue_arrow, (50, 100))
            screen.blit(continue_arrow, (575, 700))

            
            if player.colliderect(bottom_border): #checks if the player crosses to next level
                passing = False
                lvl_2_won = False

                #reset game stats for next level
                player_x = 587
                player_y = 387
                time_remaining = time_limit
                start_time = time.time()


    #======== LEVEL 2 ========
        """
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
                            
                    
                    """
        
        #======== LVL 2 TIMER ======== 
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - int(elapsed_time)

        if lvl_1_won == True and lvl_2_won == False and game_lost == False:
            timer = pygame.draw.rect(screen, RED, ( 305, 30, remaining_time * 10, 15))
            timer_background = pygame.draw.rect(screen, WHITE, (305, 30, 600, 15), 2)


        #======= LVL 2 ENEMIES ========

        if lvl_1_won:
            
            if remaining_time <= 30:
                        enemy_spawn_rate = 0.02

            if not passing and not lvl_2_won and game_lost == False:
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
                        if random.random() < powerup_spawn and len(powerups) < 10:
                            powerup_number = random.randint(1, 100)

                            if powerup_number <= 20:
                                powerups.append([enemy[0], enemy[1], "extra_life"])
                            elif powerup_number <= 40:
                                powerups.append([enemy[0], enemy[1], "coffee"])
                            elif powerup_number <= 60:
                                powerups.append([enemy[0], enemy[1], "rapid_fire"])
                            elif powerup_number <= 80:
                                powerups.append([enemy[0], enemy[1], "round_shot"])
                            else:
                                powerups.append([enemy[0], enemy[1], "slow"])
                        
                screen.blit(enemy_image, (enemy[0], enemy[1]))

                if slowed == True:
                    for enemy in enemies:
                                    tinted_sprite = enemy_image.copy()
                                    tinted_sprite.fill((82, 105, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
                                    screen.blit(tinted_sprite, (enemy[0], enemy[1]))



        if remaining_time <= 0 and lvl_1_won == True and lvl_2_won == False and passing == False: #checks if the time runs out and if so, the player has won
            lvl_2_won = True
            passing = True
            gold = score / 10
            round (gold)
            score = 0
            bullets.clear()
            enemies.clear()
            player_x = 587
            player_y = 387
                    
        if lvl_1_won == True and passing == True and lvl_2_won == True:
            #level complete text
            level_complete = title_font.render("LEVEL COMPLETE!", True, BLACK)
            screen.blit(level_complete, (475, 50))
        
            continue_arrow = pygame.image.load("Down Arrow.png")
            continue_arrow = pygame.transform.scale(continue_arrow, (50, 100))
            screen.blit(continue_arrow, (575, 700))
        
        if player.colliderect(bottom_border):
            passing = False
            game_won = False

            # Reset player position
            player_x = 587
            player_y = 387

        # Draw and check chest separately
        if lvl_2_won == True and passing == False:

            chest_rect = pygame.Rect(560, 500, 80, 80)

            chest_img = pygame.image.load("Chest.png")
            chest_img = pygame.transform.scale(chest_img, (80, 80))
            screen.blit(chest_img, (560, 500))

            # Update player rectangle using current position
            player = pygame.Rect(player_x, player_y, player_size, player_size)

            if player.colliderect(chest_rect):
                game_won = True

        if game_won == True:
            game_complete = title_font.render("GAME COMPLETE!", True, BLACK)
            screen.blit(game_complete, (475, 390))


        if lives < 0:
            game_lost = True
            game_over = title_font.render("GAME OVER!", True, RED)
            screen.blit(game_over, (490, 390))
            player_x = 600
            player_y = 400



    # Update the display
    pygame.display.flip()

    # Limit the game to 60 FPS
    clock.tick(60)
#
# Close Pygame
pygame.quit()