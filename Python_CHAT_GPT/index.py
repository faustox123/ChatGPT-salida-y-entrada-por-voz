import speech_recognition as sr
import openai
import pyttsx3

openai.api_key = "TU_KEY_DE_OPENAI"

#ingresamos el texto que deseamos
#texto = input("\nQue deseas preguntar:")

#----------------------------
#generar sentencias por voz
def abrir_microfono():
    sr.Microphone(device_index = 0)
    
    #creamos objeto
    r = sr.Recognizer()
    r.energy_threshold=2000
    r.dynamic_energy_threshold = False
    
    with sr.Microphone() as source:
            print('ESCUCHANDO.....:')
            #reduce noise
            r.adjust_for_ambient_noise(source)
            #take voice input from the microphone
            audio = r.listen(source)
            try:
                phrase = r.recognize_google(audio,language="es-MX")
                print(phrase)
                return phrase
            except TimeoutException as msg:
                print(msg)
            except WaitTimeoutError:
                print("listening timed out while waiting for phrase to start")
                quit()
            # speech is unintelligible
            except LookupError:
                print("Could not understand what you've requested.")
            else:
                print("Your results will appear in the default browser. Good bye for now...")


#Guardamos la sentencia de texto en una variable para luego pasarla a la IA
texto = abrir_microfono()

completion = openai.Completion.create(engine = "text-davinci-003",
                                      prompt = texto,
                                      max_tokens = 2048)

#imprimimos el resultado
salida=completion.choices[0].text
print(salida)

with open("contenido.txt","w") as file:
    file.write(salida)
    file.close()

#abrimos el archivo
book = open(r"contenido.txt")
book_text = book.readlines()
engine = pyttsx3.init()

for line in book_text:
    engine.say(line)
    engine.runAndWait()
