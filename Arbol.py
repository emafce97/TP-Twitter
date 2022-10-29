from nltk.stem import SnowballStemmer  # Stemmer
from nltk.corpus import stopwords  # Stopwords
from BTrees.OOBTree import OOBTree
import string


class indice_invertido_btree:

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
        for doc in self._docs:
            for id_tweet, texto in doc.items():
                self._doc_to_docID[id_tweet] = docID
                docID += 1
        self._docID_to_doc = dict((v, k) for k, v in self._doc_to_docID.items())

    def __lematizar_palabra(self, palabra):
        '''No vamos a usar el stemmer para no perder parte de la palabra y poder
        realizar búsquedas con comodines, en este caso más que lematizar la operación
        es acondicionar la palabra, pasando todo a mínuscula, eliminando acentos y signos
        de puntuación'''

        reemplazos = (("á", "a"), ("é", "e"), ("ó", "o"), ("ú", "u"), ("í", "i"))
        palabra = palabra.lower()
        palabra = palabra.strip(string.punctuation + "»" + "\x97" + "¿" + "¡")
        for a, b in reemplazos:
            palabra = palabra.replace(a, b)

        # palabra_lematizada = self._spanish_stemmer.stem(palabra)
        palabra_lematizada = palabra
        return palabra_lematizada

    def __generar_indice(self):
        ''' Genera los pares la lista de pares (palabra, docID) ordenada por palabra
        '''
        pares = []

        # Cambiamos el diccionario de python por un diccionario sobre árboles B
        indice = OOBTree()

        for doc in self._docs: # [{"id_1" : "texto1"},{"id_2" : "texto2"}]
            for id_tweet,texto in doc.items():
                lista_palabras = [palabra for palabra in texto.split() if not palabra in self.stop_words]
                lista_palabras = [self.__lematizar_palabra(palabra) for palabra in lista_palabras]
                pares = pares + [(palabra, self._doc_to_docID[id_tweet]) for palabra in lista_palabras]

        for par in pares:
            posting = indice.setdefault(par[0], set())
            posting.add(par[1])
        self._indice = indice

    def __buscar(self, palabra):
        alfabeto = 'abcdefghijklmnñopqrstuvwxyz'

        ultimo = palabra[-1]
        palabra_final = palabra[:-1] + alfabeto[(alfabeto.find(ultimo) + 1) % len(alfabeto)]
        palabras = set()
        claves = list(self._indice.keys())
        # minKey Devuelve la menor clave del árbol que sea mayor o igual a la palabra
        # que recibe como argumento
        menor = claves.index(self._indice.minKey(palabra))
        mayor = claves.index(self._indice.minKey(palabra_final))
        palabras = set(claves[menor:mayor])

        return palabras

    def buscar(self, palabra):
        '''Búsqueda con comodines, solo soporta comodín al final de la palabra'''
        palabras = set()
        resultados = set()
        palabra_lematizada = self.__lematizar_palabra(palabra)

        if palabra.find("*") == -1:  # palabra sin comodin
            if palabra_lematizada in self._indice:
                palabras.add(palabra_lematizada)
        elif palabra[-1] == "*":  # comodín al final
            palabras = self.__buscar(palabra[:-1])

        for pal in palabras:
            for docID in self._indice[pal]:
                resultados = resultados | {self._docID_to_doc[docID]}

        #return palabras, resultados
        return resultados