import flet as ft
from funciones import obtain_world_list, obtain_robot_list
from user_controls.world import World
from user_controls.robot import Robot

def ConfigureWorld(page: ft.Page):
    title = "Configurar mundos"

    world_list: list[World] = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")
    robot_list: list[Robot] = obtain_robot_list("/home/robot/app_multirobot/app_multi_robot/robots_register.yaml")
    robot_configure_list: list = list()
    widget_robots = ft.Container(
        bgcolor="gray",
        border=ft.border.all(width=1.5),
        content=ft.Text(value="No hay robots agregados"))

    def add_value_number(e):
        value = int(num_robots_input.value) + 1
        num_robots_input.value = str(value)
        num_robots_input.update()

    def reduce_value_number(e):
        value = int(num_robots_input.value) - 1
        if value >= 0:
            num_robots_input.value = str(value)
            num_robots_input.update()

    def close_dialog(e):
        page.dialog.open = False
        page.update()
    
    
    def build_table_robot(collection_robot: list[Robot]):
        if collection_robot:
            widget_robots = ft.Column()
            widget_robots.controls.clear()
            for robot in collection_robot:
                widget_robots.controls.append(robot.build())
            widget_robots.update()

    def save_robot(e):
        robot = find_robot_by_name(robot_combobox.value, robot_list)
        info = robot.yaml_configure()
        info['x_pose'] = x_pose.value
        info['y_pose'] = y_pose.value
        info['z_pose'] = z_pose.value
        info['yaw'] = yaw.value
        info['rviz_view'] = str(rviz_view.value).lower()
        robot_configure_list.append(info)
        page.dialog.open = False
        page.update()

    def find_robot_by_name(name: str, robots: list[Robot]) -> Robot:
        for robot in robots:
            if robot.name == name:
                return robot
    
    def save_configuration(e):
        page.dialog = ft.AlertDialog(
            title="Guardar configuracion",
            content=ft.Column(
                controls=[
                    save_path,
                    save_configuration_button
                ]))
        page.dialog.open = True
        page.update()

    label_title = ft.Text(
        value="Configurar mundo")
    world_combobox = ft.Dropdown(
        label="Mundo",
        hint_text="Elige el mundo",
        options=[ft.dropdown.Option(world.name) for world in world_list])
    label_num_robots = ft.Text(
        value="Numero de robots")
    num_robots_input = ft.TextField(
        value="0",
        disabled=True,
        text_align="right",
        width=100)
    add_value = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE,
        on_click=add_value_number)
    reduce_value = ft.IconButton(
        icon=ft.icons.REMOVE_CIRCLE,
        on_click=reduce_value_number)
    save_button = ft.ElevatedButton(
        text="Guardar",
        icon=ft.icons.SAVE)
    robot_combobox = ft.Dropdown(
        label="Robot",
        hint_text="Seleccione un robot",
        options=[ft.dropdown.Option(robot.name) for robot in robot_list])
    x_pose = ft.TextField(
        label="Pose X")
    y_pose = ft.TextField(
        label="Pose Y")
    z_pose = ft.TextField(
        label="Pose Z")
    yaw = ft.TextField(
        label="Yaw")
    rviz_view = ft.Checkbox(
        label="Vista en RViz",
        value=False)
    save_path = ft.TextField(
        label="Nombre archivo configuracion")
    save_configuration_button = ft.ElevatedButton(
        text="Finish",
        on_click=save_configuration)

    build_table_robot(robot_configure_list)

    def add_robot(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Agregar robot"),
            content=ft.Column(
                controls=[
                    robot_combobox,
                    x_pose,
                    y_pose,
                    z_pose,
                    yaw,
                    rviz_view
                ]),
            actions=[
                ft.TextButton("Guardar", on_click=save_robot),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()
    
    add_robot_button = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE,
        on_click=add_robot)

    configure_view = ft.SafeArea(
        content=ft.Column(
            controls=[
                label_title,
                world_combobox,
                ft.Row(
                    controls=[
                        label_num_robots,
                        num_robots_input,
                        add_value,
                        reduce_value
                    ]
                ),
                ft.Row(
                    controls=[
                        widget_robots,
                        add_robot_button
                    ]
                ),
                save_button
            ]
        )
    )

    def on_page_load():
        pass

    return {
        "view": configure_view,
        "title": title,
        "load": on_page_load
    }
