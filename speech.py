### Laura's Speech file

import speech_recognition as sr
import time
import pygame



# def speech_recognition_function():
#     freeze_words = ["FREEZE", "BREEZE", "ARIES", "FRIES", "JEWELRIES", "PLEASE", "REESE", "TREES", "THREE", "PRAISE", "PRICE", "BRIEF", "FREE", "RACE"]
#     start_words = ["START", "STARKS", "STARDUST"]
#     stop_words = ["STOP"]
#     reverse_words = ["REVERSE", "BROTHERS", "RIVERS"]
#     die_words = ["DIE", "BYE", "DIVE"]

#     recognizer = sr.Recognizer()
#     recognizer.dynamic_energy_threshold = True
#     recognizer.energy_threshold = 300
#     recognizer.pause_threshold = 0.5
    
#     time.sleep(2)
#     while True:
#         with sr.Microphone() as source:
#             try:
#                 print("Say something!")
#                 recognizer.adjust_for_ambient_noise(source, duration=0.5)

#                 audio = recognizer.listen(source)
#                 print("Got it! Now to recognize it...")

#                 audio = recognizer.recognize_google(audio, show_all=True)

#                 if audio and 'alternative' in audio:
#                     speech_text = audio['alternative'][0]['transcript'].upper()
#                     print(f"You said: {speech_text}")

#                     if any(word in speech_text for word in freeze_words):
#                         print("Freeze is recognized!")
#                     if any(word in speech_text for word in start_words):
#                         print("Start is recognized!")
#                     if any(word in speech_text for word in reverse_words):
#                         print("Reverse is recognized!")
#                     if any(word in speech_text for word in die_words):
#                         print("Die is recognized!")
#                     if any(word in speech_text for word in stop_words):
#                         print("Stopping the game")
#                         break

#             except sr.UnknownValueError:
#                 print("Google Web Speech API could not understand audio")
#             except sr.RequestError as e:
#                 print(f"Could not request results from Google Web Speech API; {e}")


if __name__ == "__main__":

    # Function to find the index of a microphone by its name
    def find_microphone_index(name):
        for index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
            if name in mic_name:
                return index
        return None
def speech_recognition_function():
    # Better to say the power up key words more than once
    freeze_words = ["FREEZE", "BREEZE", "ARIES", "FRIES", "JEWELRIES", "PLEASE", "REESE", "TREES", "THREE",
                     "PRAISE", "PRICE", "BRIEF", "FREE", "RACE","FRIENDS", "MONSTER HIGH", "FREE", "MOVIES", "FREEZER", "SPRINGS", "IS", "WALGREENS",
                      "PLEASE", "GREEN", "SPRINGS", "FACE", "CHRISTMAS MUSIC", "FRESH"]
    start_words = ["START","STARKS","STARDUST", "APRIL 1ST", "CHART","STAR"] # this works pretty good
    stop_words = ["STOP", "STAP", "713"] # this works pretty good
    reverse_words = ["REVERSE", "BROTHERS", "RIVERS", "REVEREND", "PROVERBS", "WEATHER", "REVERSED"]
    slow_words = ["SLOW", "LOW", "HELLO", "CLOSE", "SONGS", "SO", "SOLO", "BLOW", "POST MALONE", "SLOWED"]
    #die_words = ["DIE", "BYE", "DIVE"]

    time.sleep(2)
    while True:
        # Name of the microphone you want to use
        microphone_name = "Microphone (USBAudio1.0)"

        # Find the index of the microphone by its name
        microphone_index = find_microphone_index(microphone_name)

        # Check if the microphone index is found
        if microphone_index is not None:
            # Initialize the chosen microphone by index
            chosen_microphone = sr.Microphone(device_index=microphone_index)
            print(f"Using microphone '{microphone_name}' (index: {microphone_index})")
        else:
            print(f"Microphone '{microphone_name}' not found.")
    
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True  # Enable dynamic energy threshold
        recognizer.energy_threshold = 300  # Adjust this value as needed
        recognizer.pause_threshold = 0.5  # Adjust this value as needed

        with chosen_microphone as source:
            print("Say something!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # This line calibrates the noise level by listening for half a second to capture ambient noise. 


            audio = recognizer.listen(source) # capturing the person's audio
            print("Got it! Now to recognize it...")

            try:
                audio = recognizer.recognize_google(audio, show_all=True) #  This line performs speech recognition using Google Speech Recognition. It sends the captured audio data to Google's servers for processing and attempts to recognize the speech. 
                # The show_all=True parameter is used to request additional recognition results, such as alternative interpretations of the speech.

                if audio and 'alternative' in audio: # This line checks if the recognition result is not empty and if alternative interpretations are available.
                    speech_text = audio['alternative'][0]['transcript'].upper() #  This line extracts the recognized text from the recognition result. It accesses the first alternative interpretation (index 0) and converts the text to uppercase using the upper() method.
                    print(f"You said: {speech_text}")

                    if any(word in speech_text for word in freeze_words):
                        print("Freeze is recognized!")
                    if any(word in speech_text for word in start_words):
                        print("Start is recognized!")
                    if any(word in speech_text for word in reverse_words):
                        print("Reverse is recognized!")
                    if any(word in speech_text for word in slow_words):
                        print("Slow is recognized!")

                    if any(word in speech_text for word in stop_words):
                        print("Stopping the game")
                        #break

            except sr.UnknownValueError:
                print("Google Web Speech API could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")


