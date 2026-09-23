import re
import sys
from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion


def procesar_input(user_input):
    """
    Determina qué función debe ejecutar el chatbot.
    """

    if "clima" in user_input or "temperatura" in user_input:
        return obtener_clima

    if (
        "precio" in user_input
        or "accion" in user_input
        or "valor" in user_input
    ):
        return obtener_precio_accion

    return None
# Importamos las funciones de lógica de negocio desde nuestro paquete de funciones
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from funciones_agente.obtener_clima import obtener_clima
# Importamos utilidades para limpiar el texto del usuario
from utils.sanitizar import sanitizar

def chatbot():
    """
    Función principal que inicia el chatbot interactivo por consola.
    Maneja el ciclo de vida del chat, recibe el input del usuario y 
    determina qué acción realizar basándose en expresiones regulares.
    """
    print("*** Chatbot v1.0.0***")
    print("Hola, soy el Chatbot v1.0.0. Puedo ayudarte a obtener precios de acciones o indicarte")
    print("la temperatura actual en cualquier ciudad del mundo.")
    print("Me puedes hacer preguntas, por ejemplo ¿cuál es el precio de una acción de Microsoft?")
    print("¿cuál es la temperatura actual en la Ciudad de México?\n")

    # Ciclo infinito para mantener el chat activo hasta que el usuario decida salir
    while True:
        try:
            # Obtener y limpiar espacios en blanco del input del usuario
            user_input = input("--> ").strip()
            if not user_input:
                continue
            
            # Comprobar si el usuario desea finalizar la conversación
            if user_input.lower() in ["salir", "exit", "quit", "adiós", "adios"]:
                print(">>> ¡Hasta luego!")
                break

            # Reglas para detectar intención de precio de acción (mejoradas)
            # Buscamos patrones como "precio de apple", "accion de tesla", etc.
            stock_match = re.search(r"(?:precio|stock|acción|accion)\s+(?:de\s+)?(?:la\s+|el\s+)?(?:acción\s+|accion\s+)?(?:de\s+)?([\w\s]+)", user_input, re.IGNORECASE)
            
            # Reglas para detectar intención de clima
            # Buscamos patrones como "clima en oaxaca", "temperatura de madrid", etc.
            weather_match = re.search(r"(?:temperatura|clima|tiempo)\s+(?:(?:en|de)\s+)?([\w\s?]+)", user_input, re.IGNORECASE)

            # Caso 1: El usuario pregunta por acciones
            if stock_match:
                # El agente espera (driver, user_input). Pasamos None como driver en esta versión simple.
                price = obtener_precio_accion(None, user_input)
                if price:
                    print(f">>> {price}")
                else:
                    print(">>> Lo siento, no pude encontrar el precio de la acción.")
            
            # Caso 2: El usuario pregunta por el clima
            elif weather_match:
                # El agente espera (driver, user_input)
                temp = obtener_clima(None, user_input)
                if temp:
                    print(f">>> {temp}")
                else:
                    print(">>> Lo siento, no pude obtener el clima.")
            
            # Caso 3: No se detecta ninguna intención conocida
            else:
                print(">>> No estoy seguro de cómo ayudarte con eso. Prueba preguntando por el precio de una acción o el clima en una ciudad.")

        except KeyboardInterrupt:
            # Capturar Ctrl+C para salir elegantemente
            print("\n>>> ¡Hasta luego!")
            break
        except Exception as e:
            # Capturar cualquier otro error inesperado para evitar que el programa se cierre
            print(f">>> Ocurrió un error: {e}")

# Punto de entrada principal del script
if __name__ == "__main__":
    chatbot()