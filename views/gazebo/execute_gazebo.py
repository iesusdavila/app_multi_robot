import flet as ft 
from funciones import list_files_in_directory, launch_simulation, configure_package
import threading

def ExecuteGazebo(page: ft.Page):
    title = 'Ejecutar Gazebo'

    configure_archivos = list_files_in_directory(configure_package())
    gazebo_thread = None
    stop_event = threading.Event()

    def execute_gazebo(e):
        nonlocal gazebo_thread, stop_event
        stop_event.clear()
        path = configure_package() + '/' + dropdown_archive.value + ".yaml"
        print(path)
        gazebo_thread = threading.Thread(target=launch_simulation, args=(path, stop_event))
        gazebo_thread.start()

    def kill_gazebo(e):
        nonlocal gazebo_thread, stop_event
        if gazebo_thread and gazebo_thread.is_alive():
            stop_event.set()
            gazebo_thread.join()
            print("Simulación detenida")
        else:
            print("No hay simulación en ejecución")
        page.go('/')

    dropdown_archive = ft.Dropdown(
        label="Selecciona el archivo",
        hint_text='No seleccionado',
        width=300,
        options=[ft.dropdown.Option(archivo) for archivo in configure_archivos]
    )
    execute_button = ft.ElevatedButton(
        text='Ejecutar',
        icon=ft.icons.PLAY_ARROW,
        on_click=execute_gazebo)
    
    kill_gz_button = ft.ElevatedButton(
        text="Detener simulación",
        icon=ft.icons.STOP,
        on_click=kill_gazebo
    )

    execute_label = ft.Text(
        value="Ejecutar mundo en gazebo",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        size=40)

    configure_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Container(execute_label),
                ft.Container(),
                ft.Container(dropdown_archive),
                ft.Container(execute_button),
                ft.Container(kill_gz_button)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    def on_page_load():
        pass

    return {
        "view":configure_view,
        "title": title,
        "load": on_page_load
    }
