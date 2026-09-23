# Módulo encargado de la integración con servicios meteorológicos externos
import re
import requests
import urllib3


# Oculta la advertencia producida al utilizar verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def obtener_clima(driver, user_input):
    """
    Obtiene la temperatura actual utilizando el servicio wttr.in.

    Argumentos:
        driver: Instancia de Selenium WebDriver.
        user_input: Texto ingresado por el usuario.

    Retorna:
        La temperatura o un mensaje de error.
    """

    # Se conserva el argumento por compatibilidad, aunque aquí no se utiliza.
    del driver

    # Elimina únicamente las palabras completas, sin alterar la ciudad.
    city = re.sub(
        r"\b(clima|temperatura|actual|cual|es|el|la|en|de)\b",
        "",
        user_input.lower(),
    )

    city = " ".join(city.split()).strip("¿?., ")

    if not city:
        return "No pude reconocer la ciudad. Ejemplo: clima en Guadalajara."

    try:
        response = requests.get(
            f"https://wttr.in/{city}",
            params={"format": "%t"},
            timeout=15,
            verify=False,
        )

        if response.status_code == 200:
            temperatura = response.text.strip()
            return f"La temperatura actual en {city.title()} es {temperatura}."

        return (
            "No se pudo obtener el clima para esa ubicación. "
            f"Código de error: {response.status_code}."
        )

    except requests.exceptions.Timeout:
        return "El servicio del clima tardó demasiado en responder."

    except requests.exceptions.ConnectionError:
        return "No se pudo establecer conexión con el servicio del clima."

    except requests.exceptions.RequestException as error:
        return f"Error de red al obtener el clima: {error}"