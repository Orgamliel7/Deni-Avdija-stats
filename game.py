import pygame
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooting Basketball Game")

# Load images
current_dir = os.path.dirname(os.path.abspath(__file__))
background_image = pygame.image.load(os.path.join(current_dir, "static", "basketball_court.jpg"))
basket_image = pygame.image.load(os.path.join(current_dir, "static", "basket.png"))
ball_image = pygame.image.load(os.path.join(current_dir, "static", "basketball.png"))

# Set up game variables
basket_width, basket_height = basket_image.get_size()
basket_x = (screen_width - basket_width) // 2
basket_y = 20

ball_width, ball_height = ball_image.get_size()
ball_x = (screen_width - ball_width) // 2
ball_y = basket_y + basket_height + 10

initial_ball_speed = 10
ball_speed = initial_ball_speed
ball_angle = 45  # Initial angle of the shot in degrees
ball_velocity_x = ball_speed * math.cos(math.radians(ball_angle))
ball_velocity_y = -ball_speed * math.sin(math.radians(ball_angle))
ball_acceleration = 0.1
is_dragging = False
is_shot = False

# Color bar variables
color_bar_width = 200
color_bar_height = 20
color_bar_x = (screen_width - color_bar_width) // 2
color_bar_y = screen_height - color_bar_height - 10
color_bar_speed = 5
color_bar_value = 0
color_bar_direction = 1
color_bar_visible = False

# Shot counters
successful_shots = 0
missed_shots = 0

# Font
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

def draw_color_bar():
    global color_bar_value, color_bar_direction

    color_bar_value += color_bar_speed * color_bar_direction
    if color_bar_value > 255:
        color_bar_value = 255
        color_bar_direction = -1
    elif color_bar_value < 0:
        color_bar_value = 0
        color_bar_direction = 1

    # Draw the color bar
    pygame.draw.rect(screen, RED, (color_bar_x, color_bar_y, color_bar_width // 3, color_bar_height))
    pygame.draw.rect(screen, YELLOW, (color_bar_x + color_bar_width // 3, color_bar_y, color_bar_width // 3, color_bar_height))
    pygame.draw.rect(screen, GREEN, (color_bar_x + 2 * color_bar_width // 3, color_bar_y, color_bar_width // 3, color_bar_height))

    # Draw the moving arrow
    arrow_x = color_bar_x + (color_bar_width * color_bar_value // 255)
    pygame.draw.polygon(screen, PURPLE, [(arrow_x, color_bar_y - 10), (arrow_x - 10, color_bar_y), (arrow_x + 10, color_bar_y)])

def reset_ball():
    global ball_x, ball_y, ball_speed, ball_velocity_x, ball_velocity_y, is_shot
    ball_x = (screen_width - ball_width) // 2
    ball_y = basket_y + basket_height + 10
    ball_speed = initial_ball_speed
    ball_velocity_x = ball_speed * math.cos(math.radians(ball_angle))
    ball_velocity_y = -ball_speed * math.sin(math.radians(ball_angle))
    is_shot = False

def check_successful_shot():
    global successful_shots
    if basket_x < ball_x < basket_x + basket_width and \
            basket_y < ball_y < basket_y + basket_height:
        successful_shots += 1
        reset_ball()

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ball_x <= pygame.mouse.get_pos()[0] <= ball_x + ball_width and \
                    ball_y <= pygame.mouse.get_pos()[1] <= ball_y + ball_height:
                is_dragging = True
                color_bar_visible = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:
                is_dragging = False
                color_bar_visible = False
                if 170 <= color_bar_value <= 255:
                    is_shot = True
                else:
                    missed_shots += 1
                    reset_ball()

    # Move the ball if it's not dragging
    if is_shot:
        ball_x += ball_velocity_x
        ball_y += ball_velocity_y
        ball_velocity_y += ball_acceleration

    # Reset the ball position if it's missed
    if ball_y > screen_height:
        missed_shots += 1
        reset_ball()

    # Check if the ball enters the basket
    check_successful_shot()

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw basket
    screen.blit(basket_image, (basket_x, basket_y))

    # Draw ball
    screen.blit(ball_image, (round(ball_x), round(ball_y)))

    # Draw shot counters
    successful_text = font.render(f"Successful Shots: {successful_shots}", True, YELLOW)
    missed_text = font.render(f"Missed Shots: {missed_shots}", True, YELLOW)
    screen.blit(successful_text, (10, 10))
    screen.blit(missed_text, (10, 50))

    # Draw color bar
    if color_bar_visible:
        draw_color_bar()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
