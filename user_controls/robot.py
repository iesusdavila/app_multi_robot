from modelo import Modelo
"""
Robot :
    name: str,
    modelo: Modelo,
    control_type: str,
    has_camera: str
"""
class Robot():
    def __init__(self, name: str, modelo: Modelo, control_type: str, has_camera: bool):
        super().__init__()
        self.name = name
        self.control_type = control_type
        self.modelo = modelo
        self.has_camera = has_camera

