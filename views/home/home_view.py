import flet as ft
from funciones import *
from user_controls.robot import Robot
from db.flet_pyrebase import PyrebaseWrapper

def HomeView(page: ft.Page, myPyrebase: PyrebaseWrapper):
    title = "Home"

    modelos = obtain_model_list()
    all_robots = obtain_robot_list()
    control_types = ["Diferencial", "Omnidireccional", "Aerial"]

    def show_add_robot(e):
        page.dialog = ft.AlertDialog(
            modal=True,
            elevation=1,
            title=ft.Text("Agregar robot"),
            title_padding=15,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        name_input,
                        combobox_model,
                        combobox_control_type,
                        has_camera]),
                width=500,
                height=300),
            actions=[
                ft.TextButton("Guardar", on_click=save_robot),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    def add_model_robot(e):
        page.go("/add_model")
        page.update()

    robot_list_view = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False, height=200, width=700)

    def build_robot_list(robot_list: list[Robot]):
        robot_list_view.controls.clear()
        for robot in robot_list:
            fila = robot.build()
            robot_list_view.controls.append(fila)
        page.update()

    def go_worlds(e):
        page.go("/worlds")
        page.update()

    def go_environments(e):
        page.go("/environments")
        page.update()

    def go_configure_rutina(e):
        page.go('/rutina')
        page.update()
    
    def go_monitoreo(e):
        page.go('/monitor')
        page.update()

    def sign_out(e):
        myPyrebase.sign_out()
        page.go('/')

    add_robots_button = ft.ElevatedButton(
        text="Agregar robots", 
        icon=ft.icons.ADD_BOX, 
        on_click=show_add_robot,
        width=200)
    add_models_button = ft.ElevatedButton(
        text="Agregar modelos", 
        icon=ft.icons.ADD_ALERT, 
        on_click=add_model_robot,
        width=200)
    add_world_button = ft.ElevatedButton(
        text="Agregar mundo",
        icon=ft.icons.ADD_CARD,
        on_click=go_worlds,
        width=200)
    active_robot_text = ft.Text(
        value="Robots disponibles", 
        size=40, 
        style=ft.TextStyle(weight=ft.FontWeight.BOLD), 
        text_align=ft.TextAlign.CENTER)
    add_configure_button = ft.ElevatedButton(
        text="Entornos",
        icon=ft.icons.AC_UNIT,
        on_click=go_environments,
        width=200)
    configure_rutina = ft.ElevatedButton(
        text='Rutinas',
        icon=ft.icons.TASK,
        on_click=go_configure_rutina,
        width=200)
    monitoreo_rutina = ft.ElevatedButton(
        text='Monitorear rutinas',
        icon=ft.icons.DATA_EXPLORATION,
        on_click=go_monitoreo,
        width=200)
    cerrar_sesion = ft.ElevatedButton(
        text='Cerrar sesion',
        icon=ft.icons.LOGOUT,
        on_click=sign_out,
        width=200)

    build_robot_list(all_robots)

    name_input = ft.TextField(
        label="Nombre robot")
    combobox_model = ft.Dropdown(
            options=[ft.dropdown.Option(modelo.nombre) for modelo in modelos],
            label="Selecciona un modelo",
        )
    combobox_control_type= ft.Dropdown(
            options=[ft.dropdown.Option(control_type) for control_type in control_types],
            label="Selecciona un control_type"
        )
    has_camera = ft.Switch(
        label="Camara", value=False)

    def find_model_by_name(name: str, models: list[Modelo]) -> Modelo:
        for modelo in models:
            if modelo.nombre == name:
                return modelo

    def save_robot(e):
        modelo = find_model_by_name(combobox_model.value, modelos)
        new_robot = Robot(
            name_input.value,
            modelo,
            combobox_control_type.value,
            has_camera.value)
        add_robot(new_robot)
        all_robots = obtain_robot_list()
        build_robot_list(all_robots)
        page.dialog.open = False
        combobox_control_type.value = ""
        combobox_model.value = ""
        name_input.value = ""
        has_camera.value = False
        page.update()

    def close_dialog(e):
        combobox_control_type.value = ""
        combobox_model.value = ""
        name_input.value = ""
        has_camera.value = False
        page.dialog.open = False
        page.update()

    myPage = ft.SafeArea(
        expand=True,
        content=ft.Column(
            spacing=40,
            controls=[
                ft.Container(
                    active_robot_text, 
                    alignment=ft.alignment.center),
                ft.Container(
                    robot_list_view,
                    alignment=ft.alignment.center),
                ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                add_models_button,
                                add_robots_button,
                                add_world_button]),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                add_configure_button,
                                configure_rutina,
                                monitoreo_rutina])],
                    alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=cerrar_sesion,
                    alignment=ft.alignment.center)
                ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        
    )

    def on_page_load():
        pass

    return {
        "view":myPage,
        "title": title,
        "load": on_page_load
    }
