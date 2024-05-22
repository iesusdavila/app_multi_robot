class Modelo():
    def __init__(self, nombre, rutaURDF, rutaSDF, imagen):
        self.nombre = nombre
        self.rutaURDF = rutaURDF
        self.rutaSDF = rutaSDF
        self.imagen = imagen

        def to_string(self):
            data = {
                self.nombre: {
                    "rutaURDF": self.rutaSDF,
                    "rutaSDF": self.rutaSDF,
                    "image": self.image
                }
            }
            return data
        
        def is_completed(self):
            if self.nombre == "" or self.rutaURDF == "" or self.rutaSDF == "" or self.imagen == "":
                return False
            else:
                return True
        

