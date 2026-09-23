import yfinance as yf

from utils.sanitizar import sanitizar


COMPANY_TICKERS = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
}


def obtener_precio_accion(driver, user_input):
    """
    Obtiene el precio de una acción mediante yfinance.
    """

    # El driver se conserva por compatibilidad.
    del driver

    consulta = sanitizar(user_input)
    ticker = None
    empresa_encontrada = None

    # Busca el nombre de la empresa dentro de la consulta.
    for empresa, simbolo in COMPANY_TICKERS.items():
        if empresa in consulta:
            ticker = simbolo
            empresa_encontrada = empresa.title()
            break

    if ticker is None:
        return (
            "No reconocí la empresa. Prueba con Microsoft, Apple, "
            "Google, Amazon, Tesla, Meta, Netflix o Nvidia."
        )

    try:
        accion = yf.Ticker(ticker)
        historial = accion.history(period="5d")

        if historial.empty:
            return (
                f"No se encontraron datos para {empresa_encontrada} "
                f"({ticker})."
            )

        precio = historial["Close"].dropna().iloc[-1]

        try:
            divisa = accion.fast_info["currency"]
        except Exception:
            divisa = "USD"

        return (
            f"El precio actual de la acción de "
            f"{empresa_encontrada} ({ticker}) es "
            f"${precio:,.2f} {divisa}."
        )

    except Exception as error:
        return f"No se pudo obtener el precio de la acción: {error}"