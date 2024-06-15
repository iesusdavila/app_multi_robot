import flet as ft
from funciones import obtain_world_list, add_world
from user_controls.world import World
from user_controls.file_selector import FileSelector

def WorldsView(page: ft.Page):
    title = "Worlds"
    world_list = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")

    world_label = ft.Text(
        value='Mundos disponibles', 
        size=30, 
        style=ft.TextStyle(weight=ft.FontWeight.BOLD), 
        text_align=ft.TextAlign.CENTER)
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
        for world in world_list:
            fila = ft.Row(controls=[
                ft.Text(world.name)])
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
        world_list = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")
        construir_tabla(world_list)
        name_input.value = ''
        world_path_picker.reset()
        map_path.reset()
        page.dialog.open = False
        page.update()

    def close_dialog(e):
        name_input.value = ""
        world_path_picker.file_path_label = "Seleccionar archivo"
        world_path_picker.file_path_text = ""
        map_path.file_path_label = "Seleccionar archivo"
        map_path.file_path_text = ""
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

    add_return = ft.ElevatedButton(
        text="Regresar a home", 
        icon=ft.icons.ADD_CARD, 
        on_click=go_home)

    def on_page_load():
        pass

    world_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            controls=[
                ft.Container(
                    content=world_label,
                    alignment=ft.alignment.center),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                add_world_button,
                                add_return
                            ]
                        ),
                        ft.Container(world_listview)
                    ]),
            ]
        )
    )

    return {
        "view":world_view,
        "title": title,
        "load": on_page_load
    }
