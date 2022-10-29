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
    
    # Funciona
    def buscar_palabra(self, palabra):
        """Busca una palabra"""

        set_tweets = set()
        for i in range(2):
            with open(file=f"file_{i}.json",mode="r",encoding="utf-8") as file:
                documentos = json.load(file)
                lista_documentos = []
                for id_tweet in documentos.keys():
                    mapa = { id_tweet : documentos[id_tweet]["texto"] }
                    lista_documentos.append(mapa)
                resultados = indice_invertido_btree(lista_documentos).buscar(palabra)
                for i in resultados:
                    set_tweets.add(i)

        return set_tweets

    # FUNCIONA
    def buscar_palabra_frases_1(self):

        palabras_buscadas = input("Ingrese las palabras a buscar: ").split(",")
        palabras_evitadas = input("Ingrese las palabras a evitar: ").split(",")

        set_comparador = set()

        for i in range(2):
            with open(file=f"file_{i}.json", mode="r", encoding="utf-8") as file:
                documentos = json.load(file)
                lista_documentos = []
                for id_tweet in documentos.keys():
                    mapa = {id_tweet: documentos[id_tweet]["texto"]}
                    lista_documentos.append(mapa)
                indice = Indice_Invertido(lista_documentos)
                for palabra in palabras_buscadas:
                    if len(set_comparador) == 0:
                        set_comparador = indice.buscar(palabra)
                    else:
                        set_comparador = set_comparador.intersection(indice.buscar(palabra))
        return set_comparador

    # FUNCIONA
    def buscar_palabra_frases_2(self):

        palabras_buscadas = input("Ingrese las palabras a buscar: ").split(",")
        palabras_evitadas = input("Ingrese las palabras a evitar: ").split(",")

        set_comparador = set()

        for palabra in palabras_buscadas:
            if len(set_comparador) == 0:
                set_comparador = self.buscar_palabra(palabra)
            else:
                set_comparador.intersection(self.buscar_palabra(palabra))
        return set_comparador

    def __imprimir_tweet(self,tweets):
        for i in tweets:
            print(i)

if __name__ == "__main__":
    p = Programa()
    #print(p.buscar_palabra("pizza"))
    #print(p.buscar_palabra_frases())
    print(p.buscar_palabra_frases_1())

if __name__ == "__main__":
    p = Programa()
    p.run()
