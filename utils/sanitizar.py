import unicodedata


def sanitizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)

    texto_sin_acentos = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto_sin_acentos