import pygame
import random

# Initialize Pygame
pygame.init()

# Load and set window icon
icon = pygame.image.load("paintballicon.ico")
pygame.display.set_icon(icon)

# How many deaths of player
deathcount = 0  

# Set initial player position
player_x, player_y = 750, 200
normal_speed = 5
sprint_speed = 10

# Camera settings
camera_x = 0  
camera_y = 0

# Stamina settings
max_stamina = 100
stamina = max_stamina
stamina_decrease = 2
stamina_recovery = 1
sprinting = False
was_sprinting = False

# Gravity and jumping
gravity = 1
jump_power = -15
y_velocity = 0
on_ground = False

# Set up display
screen_width, screen_height = 1400, 790
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paintball!")

# Barrier
barrier = pygame.Rect(530, 550, 99, 100)
pygame.draw.rect(screen, (0, 0, 0), (barrier.x - camera_x, barrier.y, barrier.width, barrier.height))

# Load background image
background = pygame.image.load("stock.png").convert()

# Load player image
player_img = pygame.image.load("paintball.png").convert_alpha()
img_width, img_height = player_img.get_size()

# Load sprint sound
pygame.mixer.init()
acc = pygame.mixer.Sound("acceleration.wav")
death = pygame.mixer.Sound("death.wav")

# Define blocks (positions and sizes)
block1 = pygame.Rect(1200, 700, 100, 50)
block2 = pygame.Rect(1600, 600, 120, 50)
block3 = pygame.Rect(2000, 500, 100, 100)
block5 = pygame.Rect(3000, 200, 100, 800)
block4 = pygame.Rect(3400, 450, 100, 100)

# Create a moving block
moving_block = pygame.Rect(2400, 600, 100, 50)  # Initial position
moving_block2 = pygame.Rect(2800, 500, 100, 50)  # Initial position
moving_speed = 3  # Speed of movement
moving_direction1 = 1  # 1 for right, -1 for left
moving_direction2 = 1  # 1 for up, -1 for down
moving_limit_left1 = 2300  # Left boundary
moving_limit_right1 = 2700  # Right boundary
moving_up_limit1 = 300  # Up boundary
moving_down_limit1 = 600  # Down boundary

exit_portal = pygame.Rect(330, 600, 100, 300)
exit_portal_x, exit_portal_y = 330, 600

# Triangle spikes (list of 3 points each)
spike1 = [(1300, 800), (1450, 650), (1600, 800)]  # Triangle pointing up
spike2 = [(1700, 800), (1850, 650), (2000, 800)]  # Another triangle
spike3 = [(2100, 800), (2250, 650), (2400, 800)]  # Another triangle
spike4 = [(2400, 800), (2550, 650), (2700, 800)]  # Another triangle
spike5 = [(2700, 800), (2850, 650), (3000, 800)]  # Another triangle

# Create Laser lines
laser1 = pygame.Rect(3100, 650, 100, 10)

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 40)  # None = default font, 36 = size

# Render the texts
warning_message = font.render("Watch out for spikes!", True, (255, 0, 0))  # Red
up_message = font.render("Press UP to Jump!", True, (0, 0, 0)) 
stamina_message = font.render("Stamina: ", True, (0, 0, 0))
space_message = font.render("Hold X to Sprint!", True, (0, 0, 0))
death_message = font.render("You died!", True, (111, 0, 0))
taunt_message = font.render("Exit Portal! Come here to win!", True, (0, 255, 0))
moving_message = font.render("Not all blocks stay still...", True, (255, 255, 0))

running = True
while running:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    
    # Sprint logic
    if keys[pygame.K_x]:
        if stamina > 0:
            if not was_sprinting:
                acc.play(-1)
            sprinting = True
            stamina -= stamina_decrease
        else:
            sprinting = False
            if stamina < 10:
                acc.stop()
    else:
        if was_sprinting:
            pygame.mixer.stop()
        sprinting = False

    # Stamina recovery
    if not sprinting and stamina < max_stamina:
        stamina += stamina_recovery

    # Set speed
    speed = sprint_speed if sprinting else normal_speed

    # Move player
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    
    # Jumping logic
    if keys[pygame.K_UP] and on_ground:
        y_velocity = jump_power
        on_ground = False

    # Apply gravity
    y_velocity += gravity
    player_y += y_velocity

    # Ground Collision
    if player_y >= screen_height - img_height:
        player_y = screen_height - img_height
        y_velocity = 0
        on_ground = True
    else:
        on_ground = False

    # Block Collision (Landing)
    for block in [block1, block2, block3, block4, block5, moving_block, moving_block2]:
        if player_y + img_height > block.top and player_x + img_width > block.left and player_x < block.right and y_velocity > 0:
            player_y = block.top - img_height
            y_velocity = 0
            on_ground = True

    # Block Collision (Sides)
    for block in [block1, block2, block3, block5, barrier, moving_block, moving_block2]:
        if player_x + img_width > block.left and player_x < block.right and player_y + img_height > block.top and player_y < block.bottom:
            if keys[pygame.K_RIGHT]:
                player_x = block.left - img_width
            elif keys[pygame.K_LEFT]:
                player_x = block.right

    # Barrier Collision
    if player_x + img_width > barrier.left and player_x < barrier.right and player_y + img_height > barrier.top and player_y < barrier.bottom:
        if keys[pygame.K_RIGHT]:
            player_x = barrier.left - img_width
        elif keys[pygame.K_LEFT]:
            player_x = barrier.right

    # Update sprinting state
    was_sprinting = sprinting
    
    # Update the block position
    moving_block.x += moving_speed * moving_direction1
    moving_block2.y += moving_speed * moving_direction2

    # Reverse direction when it reaches limits
    if moving_block.x <= moving_limit_left1 or moving_block.x >= moving_limit_right1:
      moving_direction1 *= -1  # Change direction
    if moving_block2.y <= moving_up_limit1 or moving_block2.y >= moving_down_limit1:
      moving_direction2 *= -1  # Change direction
    # Camera follows the player smoothly
    camera_x = player_x - screen_width // 2 + img_width // 2  
    camera_y = player_y - screen_height // 2 + img_height // 2

    # Prevent the camera from going out of bounds
    camera_y = max(0, min(0, screen_height))

    # ---- DRAW EVERYTHING ----
    screen.fill((0, 0, 0))  
    screen.blit(background, (-camera_x, 0))  # Move background

    def point_in_triangle(px, py, p1, p2, p3):
        # Using Barycentric coordinates
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign((px, py), p1, p2)
        d2 = sign((px, py), p2, p3)
        d3 = sign((px, py), p3, p1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)  # True if inside the triangle
    
    # Get player's bottom-middle position
    player_bottom = (player_x + img_width // 2, player_y + img_height)

    # Check collision with each triangle spike
    for spike in [spike1, spike2, spike3, spike4, spike5]:
        if point_in_triangle(player_bottom[0], player_bottom[1], *spike):
            # Flash effect - make the screen white AFTER DEATH
            death.play()  
            screen.fill((255, 255, 255))
            screen.blit(death_message, (700, 400))
            pygame.display.update()
            pygame.time.delay(300)
            player_x, player_y = 750, 200  # Reset position
            y_velocity = 0
            deathcount += 1

    # Draw blocks (adjust for camera)
    pygame.draw.rect(screen, (0, 0, 0), (block1.x - camera_x, block1.y - camera_y, block1.width, block1.height))
    pygame.draw.rect(screen, (0, 0, 0), (block2.x - camera_x, block2.y - camera_y, block2.width, block2.height))
    pygame.draw.rect(screen, (0, 0, 0), (block3.x - camera_x, block3.y - camera_y, block3.width, block3.height))
    pygame.draw.rect(screen, (0, 255, 0), (exit_portal.x - camera_x, exit_portal.y - camera_y, exit_portal.width, exit_portal.height))
    pygame.draw.rect(screen, (255, 255, 0), (moving_block.x - camera_x, moving_block.y - camera_y, moving_block.width, moving_block.height))
    pygame.draw.rect(screen, (255, 255, 0), (moving_block2.x - camera_x, moving_block2.y - camera_y, moving_block2.width, moving_block2.height))
    pygame.draw.rect(screen, (0, 0, 0), (block5.x - camera_x, block5.y - camera_y, block5.width, block5.height))
    pygame.draw.rect(screen, (0, 0, 0), (block4.x - camera_x, block4.y - camera_y, block4.width, block4.height))

    # Draw triangle spikes (adjust for camera)
    pygame.draw.polygon(screen, (255, 0, 0), [(x - camera_x, y - camera_y) for x, y in spike1])  
    pygame.draw.polygon(screen, (255, 0, 0), [(x - camera_x, y - camera_y) for x, y in spike2])  
    pygame.draw.polygon(screen, (255, 0, 0), [(x - camera_x, y - camera_y) for x, y in spike3])
    pygame.draw.polygon(screen, (255, 0, 0), [(x - camera_x, y - camera_y) for x, y in spike4])
    pygame.draw.polygon(screen, (255, 0, 0), [(x - camera_x, y - camera_y) for x, y in spike5])
    
    # Draw player at the correct position
    screen.blit(player_img, (player_x - camera_x, player_y - camera_y))

    # Draw stamina bar
    stamina_bar_width = 700
    stamina_bar_height = 10
    stamina_fill = (stamina / max_stamina) * stamina_bar_width  
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, stamina_bar_width, stamina_bar_height))  
    pygame.draw.rect(screen, (0, 255, 0), (50, 50, stamina_fill, stamina_bar_height))  
    
    # Inside the game loop (before pygame.display.update()):
    screen.blit(up_message, (1200 - camera_x, 600))  # Draws text
    screen.blit(stamina_message, (50, 10))  # Draws text
    screen.blit(space_message, (1500 - camera_x, 400))  # Draws text
    screen.blit(warning_message, (1400 - camera_x, 200))  # Draws text
    screen.blit(taunt_message, (200 - camera_x, 500))  # Draws text
    screen.blit(moving_message, (2500 - camera_x, 400))  # Draws text

    # Draw death count
    deathcount_message = font.render("Deaths: " + str(deathcount), True, (0, 0, 0))
    screen.blit(deathcount_message, (1250, 10))  # Draws text
    pygame.display.update()  

pygame.quit()
