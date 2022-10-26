from nltk.stem import SnowballStemmer #Stemmer
from nltk.corpus import stopwords #Stopwords
#from BTrees.OOBTree import OOBTree
import string, json

class Indice_Invertido:

    def __init__(self, documentos):
        ''' Recibe un diccionario con los documentos
        '''
        self.stop_words = frozenset(stopwords.words('spanish'))  # lista de stop words
        self._docs = documentos
        self._spanish_stemmer = SnowballStemmer('spanish', ignore_stopwords=False)
        self.__docs_to_docID()
        self.__generar_indice()

    def __docs_to_docID(self):
        ''' Asigna a cada documento un número y guarda dos diccionarios:
        el primero que tiene como clave el nombre del documento y como valor el
        numero de documento docID asociado y el segundo que permite realizar la
        operación inversa y tiene como clave los docID y como valor el nombre del
        documento'''
        self._doc_to_docID = {}
        docID = 0
        for doc in self._docs.keys():
            self._doc_to_docID[doc] = docID
            docID += 1
        self._docID_to_doc = dict((v, k) for k, v in self._doc_to_docID.items())

    def __lematizar_palabra(self, palabra):
        ''' Usa el stemmer para lematizar o recortar la palabra, previamente elimina todos
        los signos de puntuación que pueden aparecer. El stemmer utilizado también se
        encarga de eliminar acentos y pasar todo a minúscula, sino habría que hacerlo
        a mano'''

        palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡")
        # "\x97" representa un guión

        palabra_lematizada = self._spanish_stemmer.stem(palabra)
        return palabra_lematizada

    def __generar_indice(self):
        ''' Genera los pares la lista de pares (palabra, docID)
        '''
        pares = []
        indice = {}
        for doc in self._docs:
            lista_palabras = [palabra for palabra in self._docs[doc].split() if not palabra in self.stop_words]
            lista_palabras = [self.__lematizar_palabra(palabra) for palabra in lista_palabras]

            pares = pares + [(palabra, self._doc_to_docID[doc]) for palabra in lista_palabras]
        # pares = sorted(pares, key = lambda tupla: tupla[0])
        for par in pares:
            posting = indice.setdefault(par[0], set())

            # if par[0] in indice:
            #    posting = indice[par[0]]
            # else:
            #    posting = set()
            #    indice[par[0]] = posting

            posting.add(par[1])

        self._indice = indice

    def buscar(self, palabra):
        salida = []
        palabra_lematizada = self.__lematizar_palabra(palabra)
        if palabra_lematizada in self._indice:
            for docID in self._indice[palabra_lematizada]:
                salida.append(self._docID_to_doc[docID])
        return set(salida)

if __name__ == "__main__":

    fecha_buscada = "2022-10-26"
    palabra = "pokemon"
    m = 2
    lista_ids_tweets = []
    with open(file="file_0.json",mode="r",encoding="utf-8") as file:
        mapas = json.load(file)
        for id_tweet in mapas.keys():
            fecha = mapas[id_tweet]["fecha"]
            if fecha_buscada == fecha:
                mapa = {id_tweet:mapas[id_tweet]["texto"]}
                for resultado in Indice_Invertido(mapa).buscar(palabra):
                    if resultado != None and len(lista_ids_tweets) < m:
                        lista_ids_tweets.append(resultado)
                        print(f"Tweet\n:{mapa[id_tweet]}")
    #print(lista_ids_tweets)
