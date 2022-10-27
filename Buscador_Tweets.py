from email.utils import localtime
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType
import json, os


class Programa:

    def __init__(self):
        self.cant_files = None
        self.cant_tweets_por_file = None


    def cargar_tweets_y_persistir(self, consulta, cant_files, cant_tweets_por_file):

        EXPANSIONS = 'author_id,referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,attachments.media_keys,attachments.poll_ids,geo.place_id,entities.mentions.username'
        TWEET_FIELDS = 'author_id,conversation_id,created_at,entities,geo,id,lang,public_metrics,source,text'
        USER_FIELDS = 'created_at,description,entities,location,name,profile_image_url,public_metrics,url,username'
        r = None
        self.cant_files = cant_files
        self.cant_tweets_por_file = cant_tweets_por_file
        
        try:

            o = TwitterOAuth.read_file()

            api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')

            r = api.request('tweets/search/stream/rules', {'add': [{'value': consulta}]})

            if r.status_code != 201:
                exit()

            r = api.request('tweets/search/stream/rules', method_override='GET')

            if r.status_code != 200: exit()

            r = api.request('tweets/search/stream',
                            {'expansions': EXPANSIONS, 'tweet.fields': TWEET_FIELDS, 'user.fields': USER_FIELDS, },
                            hydrate_type=HydrateType.APPEND)

            print(f"Inicio: {(localtime())}\n-- BUSCANDO TWEETS --")

            if r.status_code != 200:
                exit()

            for j in range(cant_files):

                with open(file=f"file_{j}.json", mode="w") as archivo:

                    mapas = {}

                    for i, item in zip(range(cant_tweets_por_file), r):
                        id_usuario = item['data']['author_id']
                        usuario = item['data']['author_id_hydrate']['username']
                        texto = item['data']['text']
                        id_tweet = item["data"]["id"]
                        fecha = item['data']['created_at'][0:10]
                        hora = item['data']['created_at'][11:19]

                        tweet = {"usuario": usuario, "id_usuario": id_usuario, "fecha": fecha, "hora": hora, "texto": texto}
                        mapas[id_tweet] = tweet

                        print(f"Cantidad de tweets cargados: {i}")

                    json.dump(obj=mapas, fp=archivo)

            print("-- BUSQUEDA FINALIZADA --")

        except KeyboardInterrupt:
            print('\nSe interrumpio la ejeccuion del codigo por teclado')
            return r

        except TwitterRequestError as e:
            print(f'\n{e.status_code}')
            for msg in iter(e):
                print(msg)

        except TwitterConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    def cargar_todos_json(self):
        for i in range(self.cant_files):
            with open(file=f"file_{i}.json", mode="r") as archivo:
                mapa_global = json.load(archivo)
                for mapas in mapa_global.values():
                    print(f"El paquete {i} tiene {len(mapas)} tweets cargados y son estos:\n{mapas}\n")

    def cargar_un_json(self, num_file):
        with open(file=f"file_{num_file}.json", mode="r") as archivo:
            mapa_global = json.load(archivo)
            for mapas in mapa_global.values():
                print(f"El paquete {num_file} tiene {len(mapas)} tweets cargados y son estos:\n{mapas}\n")

    def get_size_archivo(self, nombre_archivo):
        return f"Tamaño del archivo cargado es de: {os.path.getsize(f'{nombre_archivo}.json')} kbs"


if __name__ == "__main__":
    p = Programa()
    consulta = '"messi" OR "argentina" lang=es'
    p.cargar_tweets_y_persistir(consulta)
