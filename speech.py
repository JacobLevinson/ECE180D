### Laura's Speech file

import speech_recognition as sr
import time

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
# Define the initial state of the power-up variable
power_up = None

# Function to detect speech words and update the power-up variable
def detect_speech(speech_text):
    global power_up  # Using global variable
    
    # Check if any speech word is present in the speech text
    for word in speech_words:
        if word in speech_text:
            power_up = word  # Update power-up variable
            print("Activated Power-Up:", power_up)
            break
'''
if __name__ == "__main__":

    freeze_words = ["freeze", "breeze", "aries", "fries", "jewelries", "please", "reese", "trees", "three", "praise", "price", "brief", "free", "race"]
    start_words = ["start","starks","stardust"]
    stop_words = ["stop"]
    reverse_words = ["reverse", "brothers", "rivers"]
    die_words = ["die", "bye", "dive"]


    # Create recognizer and mic instances
#    recognizer = sr.Recognizer()
#    microphone = sr.Microphone()
'''
    # Loop indefinitely to continuously listen for speech input
    while True:
        # Adjust recognizer sensitivity to ambient noise and record audio
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # Recognize speech from the audio
        try:
            speech_text = recognizer.recognize_google(audio)
            print("You said:", speech_text)
            detect_speech(speech_text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

print("Activated Power-Up:", power_up)
'''
# Example usage
#speech_text = "I summon the power of fire!"
#detect_speech(speech_text)

# Now 'power_up' variable should hold the value 'fire'
#print("Activated Power-Up:", power_up)


# right before you send it, change the phrase into uppercase. so all the case does is it takes in the player's phrase and then
# we'll deal with it later.

# post the event in my function, # make a function that triggers an event, then the game logic will handle that
'''
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
'''

recognizer = sr.Recognizer()
microphone = sr.Microphone()
trigger_word = "freeze"

while True:
    with sr.Microphone() as source:
        print("Listening for trigger word...")
        audio_data = recognizer.listen(source)
        try:
            # Use PocketSphinx for faster recognition
            recognized_text = recognizer.recognize_sphinx(audio_data, keyword_entries=[(trigger_word, 1.0)])
            print("Recognized:", recognized_text)
            # Check if the trigger word is detected
            if trigger_word in recognized_text:
                print("Trigger word detected! Continuing to listen...")
                # No action needed to stop the loop, it continues
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

# Call the function to start listening for the trigger word
listen_and_detect_trigger("freeze")