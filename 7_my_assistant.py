import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import requests
from weather_key import key_weather



def audio_a_texto():
        
    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.pause_threshold = 0.8

        print("Esperant el missatge...")

        audio = r.listen(source)

        try:
            
            text = r.recognize_google(audio, language="es")

            print("Has dicho:", text)

            return text
        
        except sr.UnknownValueError:
            
            print("No te he entendido")
            return "Error"
        
        except sr.RequestError:

            print("Problemas en el hardware")
            return "Error"
        
        except:
            print("Error indeterminado")
            return "Error"    

def respuesta_PC(text):

    engine = pyttsx3.init()

    # rate = engine.getProperty("rate")
    engine.setProperty("rate", 160)

    # volume = engine.getProperty("volume")
    engine.setProperty("volume", 50)
    
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)

    engine.say(text)

    engine.runAndWait()

# respuesta_PC("Buenas tardes a todo el mundo")

def pedir_dia():
    dia = datetime.date.today()

    dia_semana = dia.weekday()
    
    dict_dias_semana = {0:"Lunes",1:"Martes",2:"Miercoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}

    respuesta_PC(f"Hoy es {dict_dias_semana[dia_semana]}")

def pedir_hora():
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} con {hora.minute} minutos y {hora.second} segundos"
    respuesta_PC(hora)

def saludo_inicial():

    hora = datetime.datetime.now()

    if 6 < hora.hour < 14:
        ahora = "Buenos dias"
    elif 14<= hora.hour < 20:
        ahora = "Buenas tardes"
    else:
        ahora = "Buenas noches"
    
    respuesta_PC(f"{ahora}, soy Helena, tu asistente personal.")
    respuesta_PC("¿En que puedo ayudarte?")

def funcion_ppal():

    saludo_inicial()

    while True:

        petición = audio_a_texto().lower()
        print(petición)

        if "abre youtube" in petición:
            respuesta_PC("Ahora mismo abriré youtube")
            webbrowser.open("http://www.youtube.com")

            continue

        elif "adiós elena" == petición:
            respuesta_PC("programa finalizado, hasta pronto")
            break
        
        elif "abre coursera" in petición:
            respuesta_PC("Ahora mismo abriré coursera")
            webbrowser.open("https://www.coursera.org/programs/2023-es-esp-py-hbh2l")
            continue

        elif "¿Que hora és?" in petición:
            pedir_hora()
            continue

        elif "¿Que día és?" in petición:
            pedir_dia()
            continue

        elif "Busca en la wikipedia" in petición:
            respuesta_PC("Buscando en la wikipedia...")
            peticion = peticion.replace("busca en la wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(peticion, sentences = 1)
            respuesta_PC("Sgún la wikipedia...")
            respuesta_PC(resultado)
        
        elif "qué tiempo hace en" in petición:

            ciutat = petición.replace("qué tiempo hace en", "")

            url = f"https://api.openweathermap.org/data/2.5/weather?q={ciutat}&appid={key_weather}&units=metric&lang=es"

            res = requests.get(url)
            data = res.json()

            temp_actual = data["main"]["temp"]
            temp_minima = data["main"]["temp_min"]
            temp_maxima =data["main"]["temp_max"]
            humedad = data["main"]["humidity"]
            tiempo = data["weather"][0]["description"]



            respuesta_PC(f"La temperatura actual en {ciutat} es {temp_actual}º, la temperatura minima es {temp_minima}º y la maxima es {temp_maxima}º con una humedad del {humedad}%")
            respuesta_PC(f"El tiempo en {ciutat} es {tiempo}")

        else:
            respuesta_PC("No entiendo lo que dices")




funcion_ppal()
