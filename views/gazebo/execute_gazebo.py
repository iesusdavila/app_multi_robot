import flet as ft 
from funciones import list_files_in_directory, launch_simulation

def ExecuteGazebo(page: ft.Page):
    title = 'Ejecutar Gazebo'

    configure_archivos = list_files_in_directory('/home/robot/multirobot_ws/src/multi_robot/multi_robot_bringup/config')

    def execute_gazebo(e):
        path = '/home/robot/multirobot_ws/src/multi_robot/multi_robot_bringup/config/' + dropdown_archive.value + ".yaml"
        launch_simulation(path)
        page.go('/')
        page.update()
        
    
    dropdown_archive = ft.Dropdown(
        label="Selecciona el archivo",
        hint_text='No seleccionado',
        options=[ft.dropdown.Option(archivo) for archivo in configure_archivos]
    )
    execute_button = ft.ElevatedButton(
        text='Ejecutar',
        icon=ft.icons.WC_OUTLINED,
        on_click=execute_gazebo)

    configure_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            controls=[
                dropdown_archive,
                execute_button
            ]
        )
    )

    def on_page_load():
        pass

    return {
        "view":configure_view,
        "title": title,
        "load": on_page_load
    }