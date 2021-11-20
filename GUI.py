from tkinter import *
import sounddevice as sd
import speech_recognition as sr
import soundfile as sf
import re
import cv2
from pytesseract import *
import os
from gtts import gTTS
from PIL import ImageTk,Image
import gc
from PIL import Image,ImageTk


def convert_audio():
    fs = 44100
    duration = 2  # seconds
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, dtype='float64')
    print("Recording Audio")

    sd.wait()
    print("Audio recording complete , Play Audio")

    sd.play(myrecording, fs)
    sd.wait()
    print("Play Audio Complete")
    sf.write("sound.wav", myrecording,fs)

    r = sr.Recognizer()
    with sr.AudioFile("sound.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)

    text = re.sub("(.{65})", "\\1\n", text, 0, re.DOTALL)
    print(text)

def cam_convert():
    img = cv2.VideoCapture()
    # The device number might be 0 or 1 depending on the device and the webcam
    img.open(0, cv2.CAP_DSHOW)
    while (True):
        ret, frame = img.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    img.release()
    cv2.destroyAllWindows()

    pytesseract.tesseract_cmd = r'C:\Users\3shry\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    res = pytesseract.image_to_string(frame)

    # Language we want to use
    language = 'en'

    myobj = gTTS(text=res, lang=language, slow=False)

    myobj.save("output.mp3")

    # Play the converted file
    os.system("start output.mp3")

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    img = img.resize((1200, 650), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=NW, image=img)

    gc.collect()
    form.mainloop()


def main():

    ################GUI##################
    #img = Image.open("1200px-International_Symbol_for_Deafness.svg.png")
    #img = ImageTk.PhotoImage(img)
    #canvas.create_image(10, 10, anchor=NW, image=img)

    Speak_butt = Button(text="   Speak   ", command=convert_audio)
    Speak_butt.place(x=450, y=600)

    Convert_butt = Button(text="   Convert   ", command=cam_convert)
    Convert_butt.place(x=700, y=600)

    form.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    form = Tk()
    canvas = Canvas(form, width=1200, height=650)
    canvas.pack()

    main()

