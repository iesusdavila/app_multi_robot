import flet as ft
from funciones import obtain_world_list, add_world
from user_controls.world import World
from user_controls.file_selector import FileSelector
from db.flet_pyrebase import PyrebaseWrapper

def WorldsView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Worlds"
    world_list = obtain_world_list()

    world_listview = ft.ListView(
        spacing=10, 
        padding=20, 
        auto_scroll=True,
        height=100, 
        width=300)
    name_input = ft.TextField(
        label="Nombre mundo")
    world_path_label = ft.Text(
        value="Ruta del mundo")
    map_label = ft.Text(
        value="Ruta del mapa")
    world_path_picker = FileSelector()
    map_path = FileSelector()

    def construir_tabla(world_list: list[World]):
        world_listview.controls.clear()
        encabezado = ft.Container(
            content=ft.Text(
                value="Nombre mundos",
                style=ft.TextStyle(
                    size=20,
                    weight=ft.FontWeight.W_400)
            ),
            bgcolor=ft.colors.GREY_400,
            alignment=ft.alignment.center)
        world_listview.controls.append(encabezado)
        for world in world_list:
            fila = ft.Container(
                content=ft.Text(
                    value=world.name),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREY_300)
            world_listview.controls.append(fila)
        page.update()

    construir_tabla(world_list)

    def save_world(e):
        new_world = World(
            name_input.value,
            world_path_picker.file_path_text,
            map_path.file_path_text
        )
        add_world(new_world)
        world_list = obtain_world_list()
        construir_tabla(world_list)
        name_input.value = ''
        world_path_picker.reset()
        map_path.reset()
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        name_input.value = ""
        world_path_picker.reset()
        map_path.reset()
        page.dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text('Agregar mundo'),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    name_input,
                    world_path_label,
                    world_path_picker,
                    map_label,
                    map_path
                ]),
            width=350,
            height=300),
        actions=[
            ft.TextButton("Guardar", on_click=save_world),
            ft.TextButton("Cancelar", on_click=close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def show_add_world(e):
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    add_world_button = ft.ElevatedButton(
        text="Agregar mundo", 
        icon=ft.icons.ADD_BOX, 
        on_click=show_add_world)
    
    def go_home(e):
        page.go('/home')
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')
        page.update() 

    def on_page_load():
        nonlocal world_list
        world_list = obtain_world_list()
        construir_tabla(world_list)
        page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.HOME,
                on_click=go_home),
            leading_width=60,
            title=ft.Text(
                value="Mundos disponibles",
                style=ft.TextStyle(
                    size=30,
                    weight=ft.FontWeight.BOLD)),
            center_title=True,
            bgcolor=ft.colors.GREY_200,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text=str(myPyrebase.email)),
                        ft.PopupMenuItem(
                            text="Cerrar Sesion",
                            icon=ft.icons.LOGOUT_ROUNDED,
                            on_click=sign_out)])])
        page.update()

    world_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Container(
                    height=10),
                ft.Container(
                    content=add_world_button,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=world_listview,
                    alignment=ft.alignment.center),
            ]
        )
    )

    return {
        "view":world_view,
        "title": title,
        "load": on_page_load
    }
