import speech_recognition as sr
import martypy
from googletrans import Translator
import time

# Initialize Marty, Google Translate
marty = martypy.Marty("wifi","192.168.130.38")  # Replace with your Marty's IP address
translator = Translator()

# Function to listen to user's voice input in English
def listen_for_english():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        marty.speak("Listening for an English sentence")
        print("Listening for an English sentence...")
        time.sleep(3)
        audio = recognizer.listen(source)
        #time.sleep(5)

        try:
            # Convert speech to text using Google's Speech Recognition API
            user_sentence = recognizer.recognize_google(audio, language="en")
            print(f"You said: {user_sentence}")
            return user_sentence.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("API unavailable or request failed.")
            return None

# Function to listen for the user's response in Spanish
def listen_for_spanish():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        marty.speak("Listening for pronunciation in Spanish")
        print("Listening for pronunciation in Spanish...")
        time.sleep(3)
        audio = recognizer.listen(source)

        try:
            # Convert speech to text in Spanish using Google's Speech Recognition API
            user_response = recognizer.recognize_google(audio, language="es")
            print(f"You said: {user_response}")
            return user_response.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("API unavailable or request failed.")
            return None

# Function to translate text from English to Spanish
def translate_to_spanish(text):
    translation = translator.translate(text, dest='es')
    print(f"Translated to Spanish: {translation.text}")
    return translation.text.lower()

# Main function for the language learning exercise
def language_learning_exercise():
    # Step 1: Listen for an English sentence from the user
    english_sentence = listen_for_english()
    time.sleep(7)
    if not english_sentence:
        marty.speak("I couldn't understand. Please try again.")
        return 0

    # Step 2: Translate the sentence to Spanish
    spanish_translation = translate_to_spanish(english_sentence)

    # Step 3: Marty speaks the Spanish translation
    marty.speak(f"The translation is: {spanish_translation}")
    time.sleep(5)

    # Step 4: Listen for the user's pronunciation in Spanish
    print("Please repeat the sentence back in Spanish.")
    user_response = listen_for_spanish()
    time.sleep(7)

    # Step 5: Compare user response to the correct translation
    if user_response == spanish_translation:
        # Correct pronunciation
        marty.disco_color(color=(0, 255, 0), add_on="LEDeye", api='led') # Show green color for incorrect answer
        marty.speak("Great job! You said it correctly!")
        marty.celebrate()  # Marty dances for correct answer
        marty.get_ready()
        return 1
    else:
        marty.disco_color(color=(255, 0, 0), add_on="LEDeye", api='led')  # Show red color for incorrect answer
        marty.kick("left")  # Marty kick action
        marty.speak(f"Not quite. The correct pronunciation is: {spanish_translation}. Let's try again.")
        marty.get_ready()
        return 0

# Run the language learning exercise
if __name__ == "__main__":
    language_learning_exercise()
    marty.disco_color(color=(0, 0, 0), add_on="LEDeye", api='led')
