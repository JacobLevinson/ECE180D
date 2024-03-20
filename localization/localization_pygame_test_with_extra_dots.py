import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
PINK = (255, 105, 180)
NEON_GREEN = (57, 255, 20)
ARBITRARY_COLOR_1 = (0, 0, 255)  # Blue
ARBITRARY_COLOR_2 = (0, 255, 255)  # Cyan

# Dot class
class Dot:
    def __init__(self, color, radius, speed):
        self.color = color
        self.radius = radius
        self.speed = speed
        self.x = random.randint(radius, SCREEN_WIDTH - radius)
        self.y = random.randint(radius, SCREEN_HEIGHT - radius)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def move(self):
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

        # Bounce off the edges
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.direction_x *= -1
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.direction_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Create Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Dots")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Create dots
radius = 20
speed = 3
pink_dot = Dot(PINK, radius, speed)
green_dot = Dot(NEON_GREEN, radius, speed)
blue_dot = Dot(ARBITRARY_COLOR_1, radius, speed)
cyan_dot = Dot(ARBITRARY_COLOR_2, radius, speed)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move dots
    pink_dot.move()
    green_dot.move()
    blue_dot.move()
    cyan_dot.move()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw dots
    pink_dot.draw(screen)
    green_dot.draw(screen)
    blue_dot.draw(screen)
    cyan_dot.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
