# # utils.speech.py
# import speech_recognition as sr
# # Function to recognize speech from audio input
# def recognize_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Say something...")
#         audio = recognizer.listen(source)
#
#     try:
#         text = recognizer.recognize_google(audio)
#         return text
#     except sr.UnknownValueError:
#         return "Could not understand audio"
#     except sr.RequestError as e:
#         return "Could not request results; {0}".format(e)
import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)
