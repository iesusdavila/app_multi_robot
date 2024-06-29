import flet as ft
from funciones import obtain_model_list, add_model
from user_controls.modelo import Modelo
from user_controls.file_selector import FileSelector

def ModeloView(page: ft.Page):
    title = 'Modelo'
    modelo_list = obtain_model_list('/home/robot/app_multirobot/app_multi_robot/models_register.yaml')
    modelo_table = ft.ListView(
        expand=1, 
        spacing=10, 
        padding=20, 
        auto_scroll=False, 
        height=100, 
        width=300,)

    def construir_tabla(modelo_list: list):
        modelo_table.controls.clear()
        for modelo in modelo_list:
            fila = ft.Container(
                        content=ft.Text(
                            value=modelo.nombre,
                            color=ft.colors.ON_SECONDARY,
                            text_align=ft.TextAlign.CENTER),
                        bgcolor=ft.colors.random_color(),
                        height=60,
                        width=250,
                        alignment=ft.alignment.center)
            modelo_table.controls.append(fila)
        page.update()
    
    construir_tabla(modelo_list)
    modelos_label = ft.Text(
        value="Modelos disponibles",
        size=40, 
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        text_align=ft.TextAlign.CENTER)
    nombre_input = ft.TextField(label="Nombre del modelo")
    urdf_input = ft.Text(
        value="Ruta URDF",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    urdf_picker = FileSelector()
    sdf_input = ft.Text(
        value="Ruta SDF",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    sdf_picker = FileSelector()
    nav_path_input = ft.Text(
        value="Ruta archivo navegacion",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    nav_picker = FileSelector()

    def on_page_load():
        pass

    def save_model(e):
        nuevo_modelo = Modelo(
            nombre_input.value,
            urdf_picker.file_path_text,
            sdf_picker.file_path_text,
            nav_picker.file_path_text)
        add_model(nuevo_modelo)
        modelo_list = obtain_model_list('/home/robot/app_multirobot/app_multi_robot/models_register.yaml')
        construir_tabla(modelo_list)
        nombre_input.value = ''
        urdf_picker.file_path_label.value = "Seleccionar archivos"
        urdf_picker.file_path_text = ""
        sdf_picker.file_path_label.value = "Seleccionar archivos"
        sdf_picker.file_path_text = ""
        nav_picker.file_path_label.value = "Seleccionar archivos"
        nav_picker.file_path_text = ""
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        nombre_input.value = ''
        urdf_picker.file_path_label.value = "Seleccionar archivos"
        urdf_picker.file_path_text = ""
        sdf_picker.file_path_label.value = "Seleccionar archivos"
        sdf_picker.file_path_text = ""
        nav_picker.file_path_label.value = "Seleccionar archivos"
        nav_picker.file_path_text = ""
        page.dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Agregar Nuevo Modelo"),
        content=ft.Container(
            ft.Column(controls=[
                nombre_input,
                urdf_input,
                urdf_picker,
                sdf_input,
                sdf_picker,
                nav_path_input,
                nav_picker
            ],
            spacing=15),
            width=500,
            height=350
        ),
        actions=[
            ft.TextButton("Guardar", on_click=save_model),
            ft.TextButton("Cancelar", on_click=close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def show_add_model_dialog(e):
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    def go_home(e):
        page.go('/home')
        page.update() 

    button_go_home = ft.ElevatedButton(
        text="Regresar a Home", 
        on_click=go_home)
    button_add_model = ft.ElevatedButton(
        text="Agregar Modelo", 
        on_click=show_add_model_dialog)
    
    modelo_view = ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.Container(
                    modelos_label,
                    alignment=ft.alignment.center),
                ft.Row(
                    controls=[
                        ft.Container(expand=1),
                        ft.Container(modelo_table, expand=2),
                        ft.Column(
                            controls=[
                                button_add_model,
                                button_go_home
                            ],
                            expand=1
                        )
                    ]
                )
            ]
        )
    )
    return {
        "view": modelo_view,
        "title": title,
        "load": on_page_load
    }
