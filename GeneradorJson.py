import json


class GeneradorJson:

    # constructor
    def __init__(self, temperaturaStr, humedadStr, fechaStr):
        self.__temperaturaStr = temperaturaStr
        self.__humedadStr = humedadStr
        self.__fechaStr = fechaStr

    # methods
    def escribirJson(self):
        datos = {
            'temperatura': self.__temperaturaStr,
            'humedad': self.__humedadStr,
            'fecha': self.__fechaStr
        }

        cadena_json = json.dumps(datos)
        print(cadena_json)

        # Escritura
        with open('enviarDatos/datos.json', 'w') as f:
            json.dump(datos, f)
