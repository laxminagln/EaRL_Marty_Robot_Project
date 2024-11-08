import time, cv2, numpy as np, speech_recognition as sr
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from martypy import Marty
from googletrans import Translator

marty = Marty("wifi","192.168.130.38")
translator = Translator()

model = MobileNetV2(weights="imagenet")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        cap.release()
        return None
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        cv2.imshow("Captured Image", frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        cap.release()
        return frame
    else:
        print("Error: Could not capture an image.")
        cap.release()
        return None

def detect_face(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces) > 0

def recognize_object(image):
    image_resized = cv2.resize(image, (224, 224))
    image_array = np.array(image_resized, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)
    predictions = model.predict(image_array)
    decoded_predictions = decode_predictions(predictions, top=1)
    object_name = decoded_predictions[0][0][1]
    print(f"Recognized object: {object_name}")
    return object_name

def translate_to_spanish(text):
    translation = translator.translate(text, dest="es")
    print(f"Translated to Spanish: {translation.text}")
    return translation.text.lower()

def listen_for_spanish():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        marty.speak("Please repeat the name in Spanish")
        print("Listening for pronunciation in Spanish...")
        audio = recognizer.listen(source)
        try:
            user_response = recognizer.recognize_google(audio, language="es")
            print(f"You said: {user_response}")
            return user_response.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("API unavailable or request failed.")
            return None

def language_learning_exercise():
    marty.speak("Please show me an object, and I will recognize it.")
    time.sleep(2)
    image = capture_image()
    if image is None:
        marty.speak("I couldn't capture the image. Please try again.")
        return
    if detect_face(image):
        object_name = "person"
        marty.speak("I see a person.")
    else:
        object_name = recognize_object(image)
    spanish_name = translate_to_spanish(object_name)

    marty.speak(f"This is a {object_name} in English.")
    time.sleep(2)
    marty.speak(f"In Spanish, it is called {spanish_name}.")
    time.sleep(2)
    
    user_response = listen_for_spanish()

    if user_response == spanish_name:
        marty.disco_color(color=(0, 255, 0), add_on="LEDeye", api='led')
        marty.dance()
        marty.speak("Great job! You said it correctly!")
        marty.get_ready()
    else:
        marty.disco_color(color=(255, 0, 0), add_on="LEDeye", api='led')
        marty.kick("left")
        marty.speak(f"Not quite. The correct pronunciation is {spanish_name}.")
        marty.get_ready()

if __name__ == "__main__":
    language_learning_exercise()
