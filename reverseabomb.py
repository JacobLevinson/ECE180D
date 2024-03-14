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
import time

# Import the pygame module
import pygame

# Import random for random numbers
import random

# Define constants for the screen width and height
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

PLAYER1_ROW = 0
PLAYER2_ROW = 0
# Physical Paremeters
LED_STRIP_LENGTH = 90  # Number of LEDs in each strip
LED_STRIP_COUNT = 6  # Number of LED strips
TOWARDS_PLAYER1 = 1
TOWARDS_PLAYER2 = -1

# Create custom events for adding a new enemy and cloud
SLAP_1 = pygame.USEREVENT + 1
SLAP_2 = pygame.USEREVENT + 2
VOICE_EVENT = pygame.USEREVENT + 3


# Define the lists of trigger words and their associated actions
trigger_words_actions = {
    "freeze": (["freeze", "breeze", "aries", "fries", "jewelries", "please", "reese", "trees", "three", "praise", "price", "brief", "free", "race"], "FREEZE_ACTION"),
    "start": (["start", "starks", "stardust"], "START_ACTION"),
    "stop": (["stop"], "STOP_ACTION"),
    "reverse": (["reverse", "brothers", "rivers"], "REVERSE_ACTION"),
    "die": (["die", "bye", "dive"], "DIE_ACTION")
}

# Initialize the recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

time.sleep(2)
# speech function to be called
def listen_and_convert():
    time.sleep(2)
    # Loop indefinitely to continuously listen for speech input
    while True:
        with microphone as source:
            print("Listening for trigger words...")
            audio_data = recognizer.listen(source)
        
        try:
            # Use PocketSphinx for faster recognition
            recognized_text = recognizer.recognize_sphinx(audio_data, keyword_entries=[(word, 1.0) for word in sum([words[0] for words in trigger_words_actions.values()], [])])
            recognized_text_upper = recognized_text.upper()  # Convert recognized text to uppercase
            print("Recognized:", recognized_text_upper)
            
            # Check if any trigger word is detected
            for word_list, action in trigger_words_actions.values():
                detected_words = [word for word in word_list if word in recognized_text_upper]
                if detected_words:
                    pygame.event.post(pygame.event.Event(VOICE_EVENT, action=action))  # Generate custom event with action

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        
        
#GameState class handles the gameplay *********************************************************

class GameState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(
                cls, *args, **kwargs)
        # Initialize your singleton instance here
        
            #no powerups at start
            cls._instance.powerup_state = "NONE" 
            
            #set initial positions of leds to middle of the field this is a 6-element array 
            cls._instance.bomb_positions = [
                LED_STRIP_LENGTH/2, LED_STRIP_LENGTH/2,
                LED_STRIP_LENGTH/2, LED_STRIP_LENGTH/2,
                LED_STRIP_LENGTH/2, LED_STRIP_LENGTH/2]
            
            #send half of the bombs toward each player. 6-element array for each row
            cls._instance.bomb_directions = [
                TOWARDS_PLAYER1, TOWARDS_PLAYER2,
                TOWARDS_PLAYER1, TOWARDS_PLAYER2,
                TOWARDS_PLAYER1, TOWARDS_PLAYER2]
            
            # Player Scores (lower is better) + 1 when you explode
            cls._instance.player1_score = 0
            cls._instance.player2_score = 0

        return cls._instance

    #this function is responsible for reverseing the bomb when a valid button press is registered
    def reverse_bomb(self, player_id, bomb_id):
        if (((self.bomb_directions[bomb_id] == TOWARDS_PLAYER1) and player_id == 1)
           or ((self.bomb_directions[bomb_id] == TOWARDS_PLAYER2) and player_id == 2)):
            # Reverse the direction of the bomb
            self.bomb_directions[bomb_id] = -1 * self.bomb_directions[bomb_id]
        else:
            print(f"Invalid reverse bomb request from player {player_id} for bomb {bomb_id}")

    def updatePoisitions(self, ledState):
        for i in range(0, LED_STRIP_COUNT):
            self.bomb_positions[i] = self.bomb_positions[i] + \
                self.bomb_directions[i]

            if (self.bomb_positions[i] <= 0 or self.bomb_positions[i] >= LED_STRIP_LENGTH):
                # Explode!
                # Update player scores
                if(self.bomb_directions[i] == TOWARDS_PLAYER1):
                    self.player1_score += 1
                else:
                    self.player2_score += 1
                print(f"Bomb {i} exploded!")
                # Reset bomb position
                self.bomb_positions[i] = LED_STRIP_LENGTH/2
                ledState.colors[i] = ["red" for _ in range(LED_STRIP_LENGTH)]
            else:
                ledState.colors[i][int(self.bomb_positions[i])] = "red"

# This class is to manage the current positions of the leds. *********************************


class LEDState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LEDState, cls).__new__(
                cls, *args, **kwargs)

            # Initialize your singleton instance here
            # Here we have an initialization of a 2D List, the first list is for the specific led strip
            # and the second list is for the index of the specific led in the strip
            # initially, set all leds to off a.k.a "black"
            cls._instance.colors = [
                ["black" for _ in range(LED_STRIP_LENGTH)] for _ in range(LED_STRIP_COUNT)]
        return cls._instance

    def send_LED_state(self, client, gameState, strip_length, strip_count):
        # Create a dictionary to store LED states for each strip
        led_state_dict = {}

        # Set LEDs at bomb positions to a different color (e.g., "red")
        for strip_index, pixel in enumerate(gameState.bomb_positions):
            # Convert position to an integer (assuming it's a float)
            pixel = int(pixel)

            # Ensure the position is within the LED strip length
            pixel = max(0, min(pixel, strip_length - 1))

            # Update the dictionary with LED states
            led_state_dict[f"LED_Strip_{strip_index}"] = {
                "pixels": self._instance.colors[strip_index]}
            # Outputs in the form of:
            #   "LED_Strip_0": {"pixels": ["black", "black", ...]},
            #   "LED_Strip_1": {"pixels": ["black", "black", ...]},

        # Convert the dictionary to a JSON string
        led_state_json = json.dumps(led_state_dict, indent=2)

        # Publish the LED state to the LED controller topic
        client.publish("ece180d/team3/reverseabomb/ledcontroller",
                       led_state_json, qos=1)




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
    gameState = GameState()
    ledState = LEDState()
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
    slap_sound = pygame.mixer.Sound("sounds/karate-chop.mp3")
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
        #Reset LED state
        for i in range(0, LED_STRIP_COUNT):
            ledState.colors[i] = ["black" for _ in range(LED_STRIP_LENGTH)]

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
                slap_sound.play()
                gameState.reverse_bomb(1, 0)
            elif event.type == SLAP_2:
                print("SLAP 2 detected")
                slap_sound.play()
                gameState.reverse_bomb(2, 0)
            elif event.type == VOICE_EVENT:
                print("Voice detected")
                if(event.action == "STOP_ACTION"):
                    print("STOP detected")
                    running = False
                elif(event.action == "FREEZE_ACTION"):
                    print("FREEZE detected")
                    if(gameState.powerup_state == "NONE"):
                        gameState.powerup_state = "FREEZE"
                elif event.action == "START_ACTION":
                    print("START detected")

                elif event.action == "REVERSE_ACTION":
                    print("REVERSE detected")

                elif event.action == "DIE_ACTION":
                    print("DIE detected")


        #Monitor if bombs explode
        gameState.updatePoisitions(ledState)

        # Send LED state to the LED strips
        
                    
        # DEMO SECTION: Just show LEDs in pygame window
        for i in range(0, LED_STRIP_COUNT):
            for j in range(0, LED_STRIP_LENGTH):
                pygame.draw.rect(screen, ledState.colors[i][j], [j*10, i*10, 10, 10])
        # Fill the screen with sky blue
        pygame.display.flip()
        # Ensure we maintain a 30 frames per second rate
        clock.tick(10)

    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()


if __name__ == "__main__":
    main()
