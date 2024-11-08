import speech_recognition as sr
import subprocess
from martypy import Marty
import time

# Initialize Marty
marty = Marty("wifi","192.168.130.38")  # Replace with your Marty's IP address
marty.get_ready()


# Function to recognize speech and interpret user's choice for mode
def recognize_mode_choice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        marty.speak("Hello Learner!, I am Marty Earl. Let's learn Spanish.")
        print("Hello Learner!, I am Marty Earl. Let's learn Spanish.")
        marty.speak("Please select the mode of learning.")
        print("Please select the mode of learning.")
        marty.speak("Say 'Translate' to learn with translation, or 'Image' to learn with an image.")
        print("Say 'Translate' to learn with translation, or 'Image' to learn with an image.")
        time.sleep(10)
        print("Listening for mode selection...")
        audio = recognizer.listen(source)
        
        try:
            user_input = recognizer.recognize_google(audio).lower()
            print(f"Recognized speech: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Speech Recognition API is unavailable.")
            return None

# Function to ask user if they want to continue and interpret response
def ask_to_continue():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        marty.speak("Would you like to continue learning? Please say 'yes' to continue or 'no' to stop.")
        time.sleep(3)
        print("Listening for continuation response...")
        audio = recognizer.listen(source)
        
        try:
            user_input = recognizer.recognize_google(audio).lower()
            print(f"Recognized speech: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Speech Recognition API is unavailable.")
            return None

def main():
    mode = None  # Track the selected mode
    
    while True:
        # Get user's choice via voice for the first time or continue with the same mode
        if mode is None:
            choice = recognize_mode_choice()
            if choice is None:
                marty.speak("I couldn't understand you. Please try again.")
                continue
            
            if "translate" in choice:
                mode = "translate"
                marty.speak("You selected Translate mode. Starting translation exercise.")
            elif "image" in choice:
                mode = "image"
                marty.speak("You selected Image mode. Starting image recognition exercise.")
            else:
                marty.speak("I couldn't understand your choice. Please say 'Translate' or 'Image'.")
                continue
        
        # Run the selected mode
        if mode == "translate":
            subprocess.run(["python", "voice_input.py"])
        elif mode == "image":
            subprocess.run(["python", "image_input.py"])

        # Prompt user for continuation after mode execution
        user_response = ask_to_continue()
        if user_response is None:
            marty.speak("I couldn't understand your response. Let's try again.")
            continue  # Retry if no clear response is detected
        elif "yes" in user_response:
            marty.speak("Continuing with the same mode.")
            time.sleep(1)
        elif "no" in user_response:
            marty.speak("Thank you for learning with me! Goodbye.")
            break
        else:
            marty.speak("I didn't understand that. Please say 'yes' to continue or 'no' to stop.")

if __name__ == "__main__":
    marty.disco_color(color=(0, 0, 0), add_on="LEDeye", api='led')
    main()
