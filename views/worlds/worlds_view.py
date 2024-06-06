import flet as ft
from funciones import obtain_world_list, add_world
from user_controls.world import World

def WorldsView(page: ft.Page):
    title = "Worlds"
    world_list = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")

    world_label = ft.Text(value='Mundos disponibles')
    world_listview = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    name_input = ft.TextField(label="Nombre mundo")
    world_input = ft.TextField(label="Ruta world")
    map_input = ft.TextField(label="Ruta map")

    construir_tabla(world_list)

    def show_add_world(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text('Agregar mundo'),
            content=ft.Column(
                controls=[

                ]),
            actions=[
                ft.TextButton("Guardar", on_click=save_world),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    add_world_button = ft.ElevatedButton(text="Agregar robots", icon=ft.icons.ADD_BOX, on_click=show_add_world)
    
    def construir_tabla(world_list: list[World]):
        world_listview.controls.clear()
        for world in world_list:
            fila = ft.Row(controls=[
                ft.Text(world.name),
                ft.Text(world.world_path),
                ft.Text(world.map_path)])
            world_listview.controls.append(fila)
        page.update()
    
    def go_home(e):
        page.go('/home')
        page.update() 

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def on_page_load():
        pass

    def save_world(e):
        new_world = World(
            name_input.value,
            world_input.value,
            map_input.value
        )
        add_world(new_world)
        world_list = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")
        construir_tabla(world_list)
        name_input.value = ''
        world_input.value = ''
        map_input.value = ''
        page.dialog.open = False
        page.update()

    world_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            controls=[
                world_label,
                world_listview,
                add_world_button
            ]
        )
    )

    return {
        "view":world_view,
        "title": title,
        "load": on_page_load
    }
