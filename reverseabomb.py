from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import paho.mqtt.client as mqtt
import json
import math
import random
import speech_recognition as sr

# Import the pygame module
import pygame

# Import random for random numbers
import random


# Create recognizer and mic instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# speech function to be called
def listen_and_convert():
    # Loop indefinitely to continuously listen for speech input
    while True:
        with microphone as source:
            audio_data = recognizer.listen(source)

        # Convert AudioData to text
        try:
            text = recognizer.recognize_google(audio_data) # converting AudioData to text
            text_upper = text.upper() # converting the text into all uppercase string
            print("Recognized text:", text_upper)
        except sr.UnknownValueError:  # if not understanding
            print("Sorry, could not understand audio.")
        except sr.RequestError as e: # if not understanding
            print("Could not request results; {0}".format(e))

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *


# Define constants for the screen width and height
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Physical Paremeters
LED_STRIP_LENGTH = 90  # Number of LEDs in each strip
TOWARDS_PLAYER1 = 1
TOWARDS_PLAYER2 = -1

# Create custom events for adding a new enemy and cloud
SLAP_1 = pygame.USEREVENT + 1
SLAP_2 = pygame.USEREVENT + 2
VOICE = pygame.USEREVENT + 3


class GameState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(
                cls, *args, **kwargs)
            # Initialize your singleton instance here
            cls._instance.powerup_state = "NONE"
            cls._instance.bomb_positions = [
                LED_STRIP_LENGTH/2, LED_STRIP_LENGTH/2,
                LED_STRIP_LENGTH/2, LED_STRIP_LENGTH/2,
                LED_STRIP_LENGTH/2, LED_STRIP_LENGTH/2]
            cls._instance.bomb_directions = [
                TOWARDS_PLAYER1, TOWARDS_PLAYER2,
                TOWARDS_PLAYER1, TOWARDS_PLAYER2,
                TOWARDS_PLAYER1, TOWARDS_PLAYER2]
            # Add more initialization as needed
        return cls._instance

    def reverse_bomb(self, player_id, bomb_id):
        if (((self.bomb_directions[bomb_id] == TOWARDS_PLAYER1) and player_id == 1)
           or ((self.bomb_directions[bomb_id] == TOWARDS_PLAYER2) and player_id == 2)):
            # Reverse the direction of the bomb
            self.bomb_directions[bomb_id] = -1 * self.bomb_directions[bomb_id]


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/team3/reverseabomb/wristband1", qos=1)
    client.subscribe("ece180d/team3/reverseabomb/wristband2", qos=1)


def on_message(client, userdata, msg):
    # Process incoming message
    topic = msg.topic
    wristband_id = topic.split('/')[-1]  # Extract wristband ID from topic
    message_content = str(msg.payload.decode(
        "utf-8")).upper()  # Assuming payload is text
    match message_content:
        case "SLAP1":
            print(f"SLAP received from wristband 1")
            custom_event = pygame.event.Event(SLAP_1)
            pygame.event.post(custom_event)
        case "SLAP2":
            print(f"SLAP received from wristband 2")
            custom_event = pygame.event.Event(SLAP_2)
            pygame.event.post(custom_event)
        case "JUMP":
            print(f"JUMP action requested by wristband {wristband_id}")
            # Additional code for JUMP action can go here
        case "RUN":
            print(f"RUN action detected from wristband {wristband_id}")
            # Additional code for RUN action can go here
        case _:
            print(f"Unhandled message: {
                  message_content} from wristband {wristband_id}")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message  
    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    # Setup for sounds, defaults are good
    pygame.mixer.init()
    # Initialize pygame
    pygame.init()
    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load and play our background music
    # pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
    # pygame.mixer.music.play(loops=-1)

    # Load all our sound files
    # Sound sources: Jon Fincher
    # move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
    # move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
    # collision_sound = pygame.mixer.Sound("Collision.ogg")

    # Set the base volume for all sounds
    # move_up_sound.set_volume(0.5)
    # move_down_sound.set_volume(0.5)
    # collision_sound.set_volume(0.5)

    # Variable to keep our main loop running
    running = True

    # Our main loop
    while running:
        # xpos_1, ypos_1, xpos_2, ypos_2 = get_position() # get position of each player

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                running = False

            elif event.type == SLAP_1:
                print("SLAP 1 detected")

            elif event.type == SLAP_2:
                print("SLAP 2 detected")

            elif event.type == VOICE:
                print("Voice detected")
#            if spoken_text:
#                if "freeze" in spoken_text:
                    # Trigger attack action in the game
                    # Example: player.attack()
#                elif "defend" in spoken_text:
                    # Trigger defend action in the game
                    # Example: player.defend()
#                    print(f"Voice detected: {event.phrase}")


        # Send LED state to the LED strips  
                    
        # Fill the screen with sky blue
        screen.fill((135, 206, 250))
        pygame.display.flip()
        # Ensure we maintain a 30 frames per second rate
        clock.tick(10)

    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()


if __name__ == "__main__":
    main()
