from user_controls.modelo import Modelo
import flet as ft
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

    def build(self):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        value=self.name, 
                        expand= 1,
                        text_align=ft.TextAlign.CENTER),
                    bgcolor="gray",
                    border=ft.border.all(1),
                    expand=1),
                ft.Text(value=self.modelo.nombre, expand= 1.5, text_align=ft.TextAlign.CENTER),
                ft.Text(value=self.control_type, expand=1, text_align=ft.TextAlign.CENTER)
            ],
            height=30,
            width=300
        )
    
    def yaml_configure(self) -> dict:
        return {
            'name': self.name,
            'urdf_path': self.modelo.rutaURDF,
            'sdf_path': self.modelo.rutaSDF,
            'nav_param_path': ""
        }
