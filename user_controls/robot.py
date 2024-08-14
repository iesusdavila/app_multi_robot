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
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK
                        )
                    ),
                    bgcolor=ft.colors.GREY_200,
                    padding=10,
                    expand=1,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Text(
                        value=self.modelo.nombre,
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            size=14,
                            weight=ft.FontWeight.NORMAL,
                            color="black"
                        )
                    ),
                    padding=10,
                    expand=2,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREY_200
                ),
                ft.Container(
                    content=ft.Text(
                        value=self.control_type,
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(
                            size=14,
                            weight=ft.FontWeight.NORMAL,
                            color="black"
                        )
                    ),
                    padding=10,
                    expand=2,
                    bgcolor=ft.colors.GREY_200,
                    alignment=ft.alignment.center
                ),
            ],
            height=45,
            width=700,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
    
    def yaml_configure(self) -> dict:
        return {
            'name': self.name,
            'urdf_path': self.modelo.rutaURDF,
            'sdf_path': self.modelo.rutaSDF,
            'nav_param_path': self.modelo.nav_path,
            'has_camera': self.has_camera
        }

