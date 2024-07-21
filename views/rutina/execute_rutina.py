import flet as ft
from funciones import list_files_in_directory, launch_rutina, rutina_dir
import threading

class RutinaRow(ft.UserControl):
    def __init__(self, name):
        super().__init__()
        self.name = ft.Text(
            value=name)
        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW_ROUNDED,
            on_click=self.play)
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP_CIRCLE_ROUNDED)
        self.stop_event = threading.Event()
        self.rutina_thread = None

    def play(self, e):
        self.stop_event.clear()
        path = rutina_dir + '/' + self.name.value + ".yaml"
        self.rutina_thread = threading.Thread(target=launch_rutina, args=(path, self.stop_event))
        self.rutina_thread.start()

    def stop(self, e):
        if self.rutina_thread and self.rutina_thread.is_alive():
            self.stop_event.set()
            self.rutina_thread.join()

    def build(self):
        return ft.ResponsiveRow(
            controls=[
                self.name,
                self.play_button,
                self.stop_button
            ],
            # width=700,
            # height=100,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

def ExecuteRutina(page: ft.Page):
    title = 'Rutinas'
    
    list_rutina_files = list()

    rutina_label = ft.Text(
        value="Rutinas",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        size=40)
    
    def go_config_rutina(e):
        page.go("/config_rutina")
        page.update()

    add_rutina = ft.ElevatedButton(
        text="Agregar rutina",
        icon=ft.icons.ADD,
        on_click=go_config_rutina)
    
    def go_home(e):
        page.go("/home")
        page.update()

    return_home = ft.ElevatedButton(
        text="Regresar a home",
        icon=ft.icons.HOME,
        on_click=go_home)
    
    rutina_listview = ft.ListView(
        height=500,
        width=700)
    
    def build_table(gz_files: list):
        rutina_listview.controls.clear()
        for file in gz_files:
            rutina_listview.controls.append(RutinaRow(file))
        page.update()
    
    build_table(list_rutina_files)
    
    rutina_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=40,
            controls=[
                ft.Container(
                    content=rutina_label,
                    alignment=ft.alignment.center),
                ft.Row(
                    controls=[
                        add_rutina,
                        return_home],
                        alignment=ft.MainAxisAlignment.CENTER),
                rutina_listview
            ]
        ))

    def on_page_load():
        nonlocal list_rutina_files
        list_rutina_files = list_files_in_directory(rutina_dir)
        build_table(list_rutina_files)
        page.update()

    return {
        "view": rutina_view,
        "title": title,
        "load": on_page_load
    }
