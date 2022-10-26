from Tweet import Tweet
from Indice_Invertido import Indice_Invertido
import json


class Programa:

    def run(self):
        """Menu del programa"""
        termino = False
        while not termino:

            print(".:: Menu de opciones ::."
                  "\n1-Buscar M tweets de un usuario en una fecha determinada"
                  "\n2-Buscar los M primeros tweets en una fecha determinada"
                  "\n3-Buscar tweets con una palabra o frase"
                  "\n4-Salir")

            opcion = int(input("Ingrese el valor de su opcion: "))

            if opcion == 1:

                datos = input("Ingrese el valor de m,del usuario y la fecha (aaaa-dd-mm): ").split(",")
                for tweet in self.buscar_m_tweets_usuario_fecha(int(datos[0]),datos[1],datos[2]):
                    print(tweet)

            elif opcion == 2:
                datos = input("Ingrese el valor de m y la fecha (aaaa-dd-mm): ").split(",")
                for tweet in self.buscar_m_tweets_fecha(int(datos[0]),datos[1]):
                    print(tweet)

            elif opcion == 3:
                pass

            elif opcion == 4:
                termino = True

    def buscar_m_tweets_usuario_fecha(self, m, usuario, fecha):
        """
        Busca una M cantidad de tweets de un usuario dado una fecha especifica
        """
        lista_tweets = []

        for i in range(1):
            with open(file=f"file_{i}.json", mode="r", encoding="utf-8") as archivo:
                documentos = json.load(archivo)
                for id_tweet in documentos.keys():
                    usuario_tweet = documentos[id_tweet]["usuario"]
                    texto_tweet = documentos[id_tweet]["texto"]
                    fecha_tweet = documentos[id_tweet]["fecha"]
                    if usuario_tweet == usuario and fecha_tweet == fecha and len(lista_tweets) < m:
                        lista_tweets.append(Tweet(usuario_tweet, texto_tweet, fecha_tweet))

        return lista_tweets

    def buscar_m_tweets_fecha(self,m,fecha):
        """
        Busca una M cantidad de tweets de todos los usuarios dada una fecha determinada
        """

        lista_tweets = []

        for i in range(1):
            with open(file=f"file_{i}.json", mode="r", encoding="utf-8") as archivo:
                documentos = json.load(archivo)
                for id_tweet in documentos.keys():
                    usuario_tweet = documentos[id_tweet]["usuario"]
                    texto_tweet = documentos[id_tweet]["texto"]
                    fecha_tweet = documentos[id_tweet]["fecha"]
                    if fecha_tweet == fecha and len(lista_tweets) < m:
                        lista_tweets.append(Tweet(usuario_tweet, texto_tweet, fecha_tweet))

        return lista_tweets

    def buscar_m_tweets_palabra(self,m,palabra):
        """
        Busca una m cantidad de veces los tweets que contenga la palabra buscada
        """

        lista_tweets = []

        for i in range(1):
            with open(file=f"file_{i}.json", mode="r", encoding="utf-8") as archivo:
                documentos = json.load(archivo)
                for id_tweet in documentos.keys():
                    usuario_tweet = documentos[id_tweet]["usuario"]
                    texto_tweet = documentos[id_tweet]["texto"]
                    fecha_tweet = documentos[id_tweet]["fecha"]
                    for solucion in Indice_Invertido({id_tweet : texto_tweet}).buscar(palabra):
                        if len(lista_tweets) < m:
                            lista_tweets.append(Tweet(usuario_tweet,texto_tweet,fecha_tweet))
                            #print(f"--------\nID_TWEET: {solucion}\nTweet: {texto_tweet}")

        return lista_tweets

    def buscar_m_tweets_frase(self,m,frase):

        palabras = frase.split()
        if len(palabras) == 1:
            self.buscar_m_tweets_palabra(m,palabras)
        else:
            pass #Terminar

# CONSULTA BOOLEANA DEL EJERCICIO 2 DE LA GUIA 5, SIRVE DE GUIA PERO HAY QUE MODIFICCARLO PARA QUE FUNCIONE ACA

    def consultar(self,indice_invertido):

        '''Realiza consultas al indice_invertido, en caso de consultar por una única palabra
        devuelve los documentos en los que aparece, y en en caso de consultar por varias palabras
        (separadas por blancos) busca alguna de las palabras (OR) y todas las palabras (AND)
        '''

        palabras = input("Ingrese la o las palabras a buscar: ").split(",")
        if len(palabras) == 1:
            return f"Como la palabra es una sola, la misma se encuentra en los siguientes archivos:\n{indice_invertido.buscar(palabras[0])}"
        else:
            opcion = int(input(
                "Elija una opcion:\n1-Ver coincidencia de archivos de todas las palabras\n2-Ver coincidencia de por lo menos una palabra\nSu opcion: "))
            if opcion == 1:
                set_comparador = indice_invertido.buscar(palabras[0])
                for i in range(1, len(palabras)):
                    set_comparador = set_comparador & indice_invertido.buscar(palabras[i])
                return f"Todas las palabras aparecen juntas en los siguientes archivos:\n{set_comparador}"
            elif opcion == 2:
                return f"Alguna de las palabras aparece en el o los siguientes archivos:\n{indice_invertido.buscar(palabras[0])}"

if __name__ == "__main__":
    p = Programa()
    print(p.buscar_m_tweets_frase(1,"Messi is no"))
