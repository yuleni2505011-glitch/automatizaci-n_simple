import unittest

from main import procesar_input
from utils.sanitizar import sanitizar
from funciones_agente.obtener_clima import obtener_clima
from funciones_agente.obtener_precio_accion import obtener_precio_accion


class TestChatbot(unittest.TestCase):

    def test_sanitizar_minusculas(self):
        resultado = sanitizar("CLIMA EN GUADALAJARA")
        self.assertEqual(resultado, "clima en guadalajara")

    def test_sanitizar_acentos(self):
        resultado = sanitizar("Precio de la ACCIÓN")
        self.assertEqual(resultado, "precio de la accion")

    def test_detectar_clima(self):
        resultado = procesar_input("clima en guadalajara")
        self.assertEqual(resultado, obtener_clima)

    def test_detectar_precio(self):
        resultado = procesar_input(
            "precio de la accion de microsoft"
        )
        self.assertEqual(resultado, obtener_precio_accion)

    def test_consulta_desconocida(self):
        resultado = procesar_input("hola como estas")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()