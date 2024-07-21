import flet as ft 
from funciones import list_files_in_directory, launch_simulation, gazebo_dir
import threading

# def ExecuteGazebo(page: ft.Page):
#     title = 'Ejecutar Gazebo'

#     configure_archivos = list_files_in_directory(gazebo_dir)
#     gazebo_thread = None
#     stop_event = threading.Event()

#     def execute_gazebo(e):
#         nonlocal gazebo_thread, stop_event
#         stop_event.clear()
#         path = gazebo_dir + '/' + dropdown_archive.value + ".yaml"
#         print(path)
#         gazebo_thread = threading.Thread(target=launch_simulation, args=(path, stop_event))
#         gazebo_thread.start()

#     def kill_gazebo(e):
#         nonlocal gazebo_thread, stop_event
#         if gazebo_thread and gazebo_thread.is_alive():
#             stop_event.set()
#             gazebo_thread.join()
#             print("Simulación detenida")
#         else:
#             print("No hay simulación en ejecución")
#         page.go('/')
#         page.update()

#     dropdown_archive = ft.Dropdown(
#         label="Selecciona el archivo",
#         hint_text='No seleccionado',
#         width=300,
#         options=[ft.dropdown.Option(archivo) for archivo in configure_archivos]
#     )
#     execute_button = ft.ElevatedButton(
#         text='Ejecutar',
#         icon=ft.icons.PLAY_ARROW,
#         on_click=execute_gazebo)
    
#     kill_gz_button = ft.ElevatedButton(
#         text="Detener simulación",
#         icon=ft.icons.STOP,
#         on_click=kill_gazebo
#     )

#     execute_label = ft.Text(
#         value="Ejecutar mundo en gazebo",
#         style=ft.TextStyle(weight=ft.FontWeight.BOLD),
#         size=40)
    
#     def return_home(e):
#         page.go('/')
#         page.update()
    
#     return_home_button = ft.ElevatedButton(
#         text="Regresar a home",
#         icon=ft.icons.HOME_FILLED,
#         on_click=return_home
#     )

#     configure_view = ft.SafeArea(
#         expand=True,
#         content=ft.Column(
#             controls=[
#                 ft.Container(execute_label),
#                 ft.Container(),
#                 ft.Container(dropdown_archive),
#                 ft.Container(execute_button),
#                 ft.Container(kill_gz_button),
#                 ft.Container(return_home_button)
#             ],
#             alignment=ft.MainAxisAlignment.CENTER
#         )
#     )

#     def on_page_load():
#         pass

#     return {
#         "view":configure_view,
#         "title": title,
#         "load": on_page_load
#     }

class GazeboRow(ft.UserControl):
    def __init__(self, name):
        super().__init__()
        self.name = ft.Text(
            value=name)
        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW_ROUNDED,
            on_click=self.play)
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP_CIRCLE_ROUNDED,
            on_click=self.stop)
        self.stop_event = threading.Event()
        self.gazebo_thread = None

    def play(self, e):
        self.stop_event.clear()
        path = gazebo_dir + '/' + self.name.value + ".yaml"
        print(path)
        self.gazebo_thread = threading.Thread(target=launch_simulation, args=(path, self.stop_event))
        self.gazebo_thread.start()

    def stop(self, e):
        if self.gazebo_thread and self.gazebo_thread.is_alive():
            print("stop")
            self.stop_event.set()
            self.gazebo_thread.join()

    def build(self):
        return ft.Row(
            controls=[
                self.name,
                self.play_button,
                self.stop_button
            ],
            width=700,
            height=100,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

def ExecuteGazebo(page: ft.Page):
    title = "Entornos"

    list_gazebo_files = list()

    gazebo_label = ft.Text(
        value="Entornos gazebo",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        size=40)
    
    def go_configure(e):
        page.go("/config_gz")
        page.update()

    add_gazebo = ft.ElevatedButton(
        text="Agregar entorno",
        icon=ft.icons.ADD,
        on_click=go_configure)
    
    def go_home(e):
        page.go("/home")
        page.update()

    return_home = ft.ElevatedButton(
        text="Regresar a home",
        icon=ft.icons.HOME,
        on_click=go_home)
    
    gazebo_listview = ft.ListView(
        height=500,
        width=700)
    
    def build_table(gz_files: list):
        gazebo_listview.controls.clear()
        for file in gz_files:
            gazebo_listview.controls.append(GazeboRow(file))
        page.update()
    
    build_table(list_gazebo_files)
    
    gazebo = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=40,
            controls=[
                ft.Container(
                    content=gazebo_label,
                    alignment=ft.alignment.center),
                ft.Row(
                    controls=[
                        add_gazebo,
                        return_home],
                        alignment=ft.MainAxisAlignment.CENTER),
                gazebo_listview
            ]
        ))

    def on_page_load():
        nonlocal list_gazebo_files
        list_gazebo_files = list_files_in_directory(gazebo_dir)
        build_table(list_gazebo_files)
        page.update()

    return {
        "view":gazebo,
        "title": title,
        "load": on_page_load
    }