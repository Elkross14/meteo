# Código de ejemplo para ver cómo se llamaría a la dirección necesaria
# del servidor y la clave de acceso. Por motivos de seguridad esto es
# solo un ejemplo y no representan la clave real del servidor.
DOMINIO = "http://pabloduran.test/recibirMeteo/"
CLAVE_SERVIDOR = "4hdaH24bqQIPjufZYKJL" + "/"


class AccesoWeb:
    '''Contiene los parámetros necesarios para acceder a la web'''

    @classmethod
    def get_dominio(cls):
        '''Devuelve la ruta del dominio usado con una barra al final'''

        return DOMINIO

    @classmethod
    def get_clave_servidor(cls):
        '''Devuelve la clave de acceso al servidor'''

        return CLAVE_SERVIDOR
