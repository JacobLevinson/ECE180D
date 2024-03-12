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

# Define constants for the screen width and height
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

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

# speech function to be called


def listen_and_convert():
    # Loop indefinitely to continuously listen for speech input
    while True:
        with microphone as source:
            print("Listening for trigger words...")
            audio_data = recognizer.listen(source)
        
        try:
            # Use PocketSphinx for faster recognition
            recognized_text = recognizer.recognize_sphinx(audio_data, keyword_entries=[(word, 1.0) for word in sum([words[0] for words in trigger_words_actions.values()], [])])
            print("Recognized:", recognized_text)
            
            # Check if any trigger word is detected
            for word_list, action in trigger_words_actions.values():
                detected_words = [word for word in word_list if word in recognized_text]
                if detected_words:
                    pygame.event.post(pygame.event.Event(VOICE_EVENT, action=action))  # Generate custom event with action

        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        # if(trigger_word in text_upper):
        #     custom_event = pygame.event.Event(VOICE)
        #     pygame.event.post(custom_event, phrase = text_upper)



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
            # Add more initialization as needed
        return cls._instance

    #this function is responsible for reverseing the bomb when a valid button press is registered
    def reverse_bomb(self, player_id, bomb_id):
        if (((self.bomb_directions[bomb_id] == TOWARDS_PLAYER1) and player_id == 1)
           or ((self.bomb_directions[bomb_id] == TOWARDS_PLAYER2) and player_id == 2)):
            # Reverse the direction of the bomb
            self.bomb_directions[bomb_id] = -1 * self.bomb_directions[bomb_id]
            
    #this function is used to update the positions of the leds when a bomb explodes. Reset the bomb to middle of field
    def updatePoisitions(self):
        for i in range(0, LED_STRIP_COUNT):
            self.bomb_positions[i] = self.bomb_positions[i] + self.bomb_directions[i]
            if(self.bomb_positions[i] == 0 or self.bomb_positions[i] == LED_STRIP_LENGTH):
                # Explode!
                print(f"Bomb {i} exploded!")
                # Reset bomb position
                self.bomb_positions[i] = LED_STRIP_LENGTH/2




def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/team3/reverseabomb/wristband1", qos=1)
    client.subscribe("ece180d/team3/reverseabomb/wristband2", qos=1)
    client.publish("ece180d/team3/reverseabomb/ledcontroller", qos=1) #publish LED state


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
                if(event.phrase == "STOP"):
                    print("STOP detected")
                    running = False
                elif(event.phrase == "FREEZE"):
                    print("FREEZE detected")
                    if(gameState.powerup_state == "NONE"):
                        gameState.powerup_state = "FREEZE"
#            if spoken_text:
#                if "freeze" in spoken_text:
                    # Trigger attack action in the game
                    # Example: player.attack()
#                elif "defend" in spoken_text:
                    # Trigger defend action in the game
                    # Example: player.defend()
#                    print(f"Voice detected: {event.phrase}")

        #Monitor if boms explode
        gameState.updatePoisitions()                        

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
