### Laura's Speech file

import speech_recognition as sr
import time
import pygame
# create function where it's set to none and once it detects one of our speech words
# chnage that variable and the game logic should be able to handle that change of what power up should happen

# I will have these cloud of words on whether or not they will be detected, every 30 seconds, a row/button will light up letting the player
# know that there is a power up available and they can choose from any of the cloud phrases which power up they want to enable.

# If they don't use the power up after recieving it for 30 seconds, it will just pile on a second, third, number of power ups they have 
# available.
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# print speech ready to indicate program is ready
print("speech ready")
    
#speech_text = recognize_speech_from_mic(recognizer, microphone)


'''
def recognize_and_convert_to_uppercase():
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
        return None

    time.sleep(2)
    while True:
        with chosen_microphone as source:
            print("Say something:")
            audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            # Convert text to uppercase
            text_uppercase = text.upper()
            print("Uppercase:", text_uppercase)

            # Check if any of the words are detected
            if any(word in text_uppercase.split() for word in freeze_words):
                print("Freeze word detected!")

            if any(word in text_uppercase.split() for word in start_words):
                print("Start word detected!")

            if any(word in text_uppercase.split() for word in stop_words):
                print("Stop word detected!")

            if any(word in text_uppercase.split() for word in reverse_words):
                print("Reverse word detected!")

            if any(word in text_uppercase.split() for word in die_words):
                print("Die word detected!")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Call the function to continuously recognize speech and convert to uppercase
recognize_and_convert_to_uppercase()
'''


def speech_recognition_function():
    freeze_words = ["FREEZE", "BREEZE", "ARIES", "FRIES", "JEWELRIES", "PLEASE", "REESE", "TREES", "THREE", "PRAISE", "PRICE", "BRIEF", "FREE", "RACE"]
    start_words = ["START", "STARKS", "STARDUST"]
    stop_words = ["STOP"]
    reverse_words = ["REVERSE", "BROTHERS", "RIVERS"]
    die_words = ["DIE", "BYE", "DIVE"]

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.5
    
    time.sleep(2)
    while True:
        with sr.Microphone() as source:
            try:
                print("Say something!")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                audio = recognizer.listen(source)
                print("Got it! Now to recognize it...")

                audio = recognizer.recognize_google(audio, show_all=True)

                if audio and 'alternative' in audio:
                    speech_text = audio['alternative'][0]['transcript'].upper()
                    print(f"You said: {speech_text}")

                    if any(word in speech_text for word in freeze_words):
                        print("Freeze is recognized!")
                    if any(word in speech_text for word in start_words):
                        print("Start is recognized!")
                    if any(word in speech_text for word in reverse_words):
                        print("Reverse is recognized!")
                    if any(word in speech_text for word in die_words):
                        print("Die is recognized!")
                    if any(word in speech_text for word in stop_words):
                        print("Stopping the game")
                        break

            except sr.UnknownValueError:
                print("Google Web Speech API could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")


if __name__ == "__main__":
    
    # Function to find the index of a microphone by its name
    def find_microphone_index(name):
        for index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
            if name in mic_name:
                return index
        return None
    
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

# print("Activated Power-Up:", power_up)


# Example usage
#speech_text = "I summon the power of fire!"
#detect_speech(speech_text)

# Now 'power_up' variable should hold the value 'fire'
#print("Activated Power-Up:", power_up)


# right before you send it, change the phrase into uppercase. so all the case does is it takes in the player's phrase and then
# we'll deal with it later.

# post the event in my function, # make a function that triggers an event, then the game logic will handle that

