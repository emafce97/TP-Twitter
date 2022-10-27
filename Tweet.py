class Tweet:

    def __init__(self,usuario,texto,fecha):
        self.usuario = usuario
        self.texto = texto
        self.fecha = fecha

    def __str__(self):
        return f"---------------\nUSUARIO: {self.usuario}\nTWEET: {self.texto}\nFECHA: {self.fecha}\n---------------"

if __name__ == "__main__":
    pass