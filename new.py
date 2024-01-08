import pygame
import sys
import random
import speech_recognition as sr

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 5  # Lower FPS for slower movement

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice-Controlled Snake Game")

# Snake variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = (1, 0)
snake_growth = False

# Apple variables
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Initialize the speech recognizer
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)

# Helper function to move the snake based on voice commands
def move_snake(command):
    global snake_direction
    if command == "up" and snake_direction != (0, 1):
        snake_direction = (0, -1)
    elif command == "down" and snake_direction != (0, -1):
        snake_direction = (0, 1)
    elif command == "left" and snake_direction != (1, 0):
        snake_direction = (-1, 0)
    elif command == "right" and snake_direction != (-1, 0):
        snake_direction = (1, 0)

# Wait for the "start" command to begin the game
start_command_received = False
while not start_command_received:
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=1)
            command = recognizer.recognize_google(audio).lower()
            if command == "start":
                start_command_received = True
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Could not request results. Check your network connection.")

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Listen for voice commands to control the snake
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=1)
                command = recognizer.recognize_google(audio).lower()
                move_snake(command)
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results. Check your network connection.")

        # Move the snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Check for collision with apple
        if snake[0] == apple:
            snake_growth = True
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

        # Check for collision with the walls or itself
        if (
            snake[0][0] < 0
            or snake[0][0] >= GRID_WIDTH
            or snake[0][1] < 0
            or snake[0][1] >= GRID_HEIGHT
            or snake[0] in snake[1:]
        ):
            game_over = True

        # Snake growth
        if not snake_growth:
            snake.pop()
        else:
            snake_growth = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the snake
        for segment in snake:
            pygame.draw.rect(
                screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

        # Draw the apple
        pygame.draw.rect(
            screen, WHITE, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        pygame.display.flip()

        # Control game speed
        clock.tick(FPS)
    else:
        # Game over screen
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over! Say 'end' to exit.", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        # Wait for the "end" command to exit the game
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=1)
                command = recognizer.recognize_google(audio).lower()
                if command == "end":
                    running = False
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results. Check your network connection.")

# Quit Pygame
pygame.quit()
sys.exit()
