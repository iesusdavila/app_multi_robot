import flet as ft
from funciones import *
from user_controls.robot import Robot

def HomeView(page: ft.Page):
    title = "Home"

    modelos = obtain_model_list("/home/robot/app_multirobot/app_multi_robot/models_register.yaml")
    all_robots = obtain_model_list("")
    control_types = ["Diferenttial", "Omnidirectional", "Ackermann", "Aerial"]

    add_robots_button = ft.ElevatedButton(text="Agregar robots", icon=ft.icons.ADD_BOX, on_click=show_add_robot)
    add_models_button = ft.ElevatedButton(text="Agregar modelos", icon=ft.icons.ADD_ALERT, on_click=add_model_robot)
    active_robot_text = ft.Text("Robots disponibles", size=30, style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    robot_list_view = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    all_robots = []

    name_input = ft.TextField(label="Nombre robot")
    combobox_model = ft.Dropdown(
            options=[ft.dropdown.Option(modelo.nombre) for modelo in modelos],
            label="Selecciona un modelo",
        )
    combobox_control_type= ft.Dropdown(
            options=[ft.dropdown.Option(control_type) for control_type in control_types],
            label="Selecciona un control_type"
        )
    has_camera = ft.Switch(label="Camara", value=False)

    def build_robot_list():
        robot_list_view.controls.clear()
        for robot in all_robots:
            fila = ft.Row(controls=[
                ft.Text(robot.name),
                ft.Text(robot.rutaURDF),
                ft.Text(robot.rutaSDF)])
            robot_list_view.controls.append(fila)
        page.update()

    def add_model_robot(e):
        page.go("/add_model")
        page.update()

    def save_robot(e):
        new_robot = Robot(
            name_input.value,
            combobox_model.value,
            combobox_control_type.value,
            has_camera.value
        )
        #add_robot(new_robot)
        #all_robots = obtain_robot_list("")


    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def show_add_robot(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Agregar robot"),
            content=ft.Column(controls=[
                name_input,
                combobox_model,
                combobox_control_type,
                has_camera
            ]),
            actions=[
                ft.TextButton("Guardar", on_click=save_robot),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    myPage = ft.SafeArea(
        expand=True,
        content=ft.Row(
            controls=[
                active_robot_text,
                robot_list_view,
                add_robots_button
            ]
        )
    )

    def on_page_load():
        pass

    return {
        "view":myPage,
        "title": title,
        "load": on_page_load
    }
