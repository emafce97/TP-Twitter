from Tweet import Tweet
#from Indice_Invertido import Indice_Invertido
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
                self.__imprimir_tweet(self.buscar_tweets(int(datos[0]),datos[2],datos[1]))

            elif opcion == 2:
                datos = input("Ingrese el valor de m y la fecha (aaaa-dd-mm): ").split(",")
                self.__imprimir_tweet(self.buscar_tweets(int(datos[0]),datos[1]))

            elif opcion == 3:
                pass

            elif opcion == 4:
                print("Saliendo...")
                termino = True

    def buscar_tweets(self, m, fecha, usuario = None):
        """ Busca una M cantidad de tweets de un usuario dado una fecha especifica """

        lista_tweets = []

        for i in range(1):
            with open(file=f"file_{i}.json", mode="r", encoding="utf-8") as archivo:
                documentos = json.load(archivo)
                for id_tweet in documentos.keys():
                    texto_tweet = documentos[id_tweet]["texto"]
                    fecha_tweet = documentos[id_tweet]["fecha"]
                    if fecha == fecha_tweet and len(lista_tweets) < m:
                        if usuario == None:
                            usuario_tweet = documentos[id_tweet]["usuario"]
                            lista_tweets.append(Tweet(usuario_tweet,texto_tweet,fecha_tweet))
                        else:
                            lista_tweets.append(Tweet(usuario, texto_tweet, fecha_tweet))

        return lista_tweets

    def __imprimir_tweet(self,tweets):
        for i in tweets:
            print(i)

if __name__ == "__main__":
    p = Programa()
    p.run()
