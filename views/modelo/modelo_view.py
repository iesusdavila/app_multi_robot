import flet as ft
from funciones import obtain_model_list, add_model
from user_controls.modelo import Modelo

def ModeloView(page: ft.Page):
    title = 'Modelo'
    modelo_list = obtain_model_list('/home/robot/app_multirobot/app_multi_robot/models_register.yaml')
    modelo_table = ft.Column()

    def construir_tabla(modelo_list: list):
        modelo_table.controls.clear()
        for modelo in modelo_list:
            fila = ft.Row(controls=[
                ft.Text(modelo.nombre),
                ft.Text(modelo.rutaURDF),
                ft.Text(modelo.rutaSDF),
                ft.Image(src=modelo.imagen, width=50, height=50)])
            modelo_table.controls.append(fila)
        page.update()
    
    construir_tabla(modelo_list)
    modelos_label = ft.Text("Modelos disponibles")
    nombre_input = ft.TextField(label="Nombre del modelo")
    urdf_input = ft.TextField(label="Ruta URDF")
    sdf_input = ft.TextField(label="Ruta SDF")
    imagen_input = ft.TextField(label="Imagen")

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                file_name = file.name
                file_content = file.read()
                
                # Guardar el archivo en una ubicación específica
                save_path = f"/ruta/deseada/{file_name}"
                with open(save_path, 'wb') as f:
                    f.write(file_content)
                
                # Mostrar la imagen cargada en la interfaz
                page.controls.append(ft.Image(src=f"/ruta/deseada/{file_name}"))
                page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    upload_button = ft.ElevatedButton(text="Cargar Imagen", on_click=lambda _: file_picker.pick_files())

    def on_page_load():
        pass

    def save_model(e):
        nuevo_modelo = Modelo(
            nombre_input.value,
            urdf_input.value,
            sdf_input.value,
            imagen_input.value
        )
        add_model(nuevo_modelo)
        modelo_list = obtain_model_list('/home/robot/app_multirobot/app_multi_robot/example2.yaml')
        construir_tabla(modelo_list)
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def show_add_model_dialog(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Agregar Nuevo Modelo"),
            content=ft.Column(controls=[
                nombre_input,
                urdf_input,
                sdf_input,
                imagen_input
            ]),
            actions=[
                ft.TextButton("Guardar", on_click=save_model),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    button_add_model = ft.ElevatedButton(text="Agregar Modelo", on_click=show_add_model_dialog)

    modelo_view = ft.SafeArea(
        content=ft.Column(
            controls=[
                modelos_label,
                modelo_table,
                button_add_model
            ]
        )
    )

    return {
        "view": modelo_view,
        "title": title,
        "load": on_page_load
    }
