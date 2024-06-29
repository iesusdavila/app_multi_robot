import flet as ft
from funciones import obtain_world_list, obtain_robot_list, configure_package
from user_controls.world import World
from user_controls.robot import Robot
import yaml

def ConfigureWorld(page: ft.Page):
    title = "Configurar mundos"

    world_list: list[World] = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")
    robot_list: list[Robot] = obtain_robot_list("/home/robot/app_multirobot/app_multi_robot/robots_register.yaml")
    robot_configure_list: list = list()
    num_robots = 0
    widget_robots = ft.Column(
        controls=[ft.Text(value="No hay robots agregados")]
    )

    def update_num_robots_input(value):
        nonlocal num_robots
        num_robots_input.value = str(value)
        num_robots = value
        num_robots_input.update()
        on_num_robots_input_change()

    def add_value_number(e):
        value = int(num_robots_input.value) + 1
        update_num_robots_input(value)

    def reduce_value_number(e):
        value = int(num_robots_input.value) - 1
        if value >= 0:
            update_num_robots_input(value)

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def build_table_robot(collection_robot):
        widget_robots.controls.clear()
        if collection_robot:
            for robot in collection_robot:
                widget_robots.controls.append(ft.Text(value=robot['name']))
        else:
            widget_robots.controls.append(ft.Text(value="No hay robots agregados"))
        widget_robots.update()

    def save_robot(e):
        robot = find_robot_by_name(robot_combobox.value, robot_list)
        info = robot.yaml_configure()
        info['x_pose'] = float(x_pose.value)
        info['y_pose'] = float(y_pose.value)
        info['z_pose'] = float(z_pose.value)
        info['yaw'] = float(yaw.value)
        info['rviz_view'] = str(rviz_view.value).lower()
        robot_configure_list.append(info)
        build_table_robot(robot_configure_list)
        page.dialog.open = False
        x_pose.value = ''
        robot_combobox.value = None
        y_pose.value = ''
        z_pose.value = ''
        yaw.value = ''
        rviz_view.value = False
        page.update()

    def write_gazebo_world(world: World, robots: list):
        path = configure_package() + '/' + save_path.value + '.yaml'
        print(path)
        with open(path, 'w') as file:
            datos = {'world': world.to_yaml(),
                     'robots': robots}
            yaml.dump(datos, file)

    def save_file(e):
        nonlocal robot_configure_list
        world = find_world_by_name(world_combobox.value, world_list)
        write_gazebo_world(world, robot_configure_list)
        robot_configure_list = []
        build_table_robot(robot_configure_list)
        update_num_robots_input(0)
        world_combobox.value = None
        page.dialog.open = False
        page.update()

    def find_robot_by_name(name: str, robots: list[Robot]) -> Robot:
        for robot in robots:
            if robot.name == name:
                return robot
    
    def find_world_by_name(name: str, worlds: list[World]) -> World:
        for world in worlds:
            if world.name == name:
                return world

    def save_configuration(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("Guardar configuracion"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        save_path
                    ]),
                width=300,
                height=200),
            actions=[
                ft.TextButton("Guardar", on_click=save_file),
                ft.TextButton("Cancelar", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog.open = True
        page.update()

    def on_num_robots_input_change():
        print("El valor de num_robots_input ha cambiado:", num_robots_input.value)
        check_add_robot_button()
    
    def check_add_robot_button():
        if len(robot_configure_list) >= int(num_robots_input.value):
            add_robot_button.disabled = True
        else:
            add_robot_button.disabled = False
        add_robot_button.update()

    label_title = ft.Text(
        value="Configurar mundo en gazebo",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        size=40)
    world_combobox = ft.Dropdown(
        label="Mundo",
        hint_text="Elige el mundo",
        width=300,
        options=[ft.dropdown.Option(world.name) for world in world_list])
    label_num_robots = ft.Text(
        value="Numero de robots",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    num_robots_input = ft.TextField(
        value="0",
        text_align="right",
        on_change=lambda e: on_num_robots_input_change(),
        width=100)
    add_value = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE,
        on_click=add_value_number)
    reduce_value = ft.IconButton(
        icon=ft.icons.REMOVE_CIRCLE,
        on_click=reduce_value_number)
    save_button = ft.ElevatedButton(
        text="Guardar",
        icon=ft.icons.SAVE,
        on_click=save_configuration)
    robot_combobox = ft.Dropdown(
        label="Robot",
        hint_text="Seleccione un robot",
        options=[ft.dropdown.Option(robot.name) for robot in robot_list])
    x_pose = ft.TextField(
        label="Pose X",
        width=90)
    y_pose = ft.TextField(
        label="Pose Y",
        width=90)
    z_pose = ft.TextField(
        label="Pose Z",
        width=90)
    yaw = ft.TextField(
        label="Yaw",
        width=90)
    rviz_view = ft.Checkbox(
        label="Vista en RViz",
        value=False)
    save_path = ft.TextField(
        label="Nombre archivo configuracion")

    def add_robot(e):
        if len(robot_configure_list) < int(num_robots_input.value):
            page.dialog = ft.AlertDialog(
                title=ft.Text("Agregar robot"),
                content=ft.Container(
                    ft.Column(
                        controls=[
                            robot_combobox,
                            ft.Row(
                                controls=[
                                    x_pose,
                                    y_pose,
                                    z_pose,
                                ]
                            ),
                            yaw,
                            rviz_view
                        ]),
                    width=350,
                    height=300),
                actions=[
                    ft.TextButton("Guardar", on_click=save_robot),
                    ft.TextButton("Cancelar", on_click=close_dialog)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog.open = True
            page.update()
        check_add_robot_button()
    
    add_robot_button = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE,
        on_click=add_robot)
    
    def return_home(e):
        page.go("/")
        page.update()

    return_home_button = ft.ElevatedButton(
        text="Regresar a home",
        icon=ft.icons.HOME,
        on_click=return_home
    )

    configure_view = ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=label_title,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=world_combobox,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=label_num_robots,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            num_robots_input,
                            add_value,
                            reduce_value
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center),
                ft.Container(
                    content=widget_robots,
                    alignment=ft.alignment.center),  
                ft.Container(
                    content=add_robot_button,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=save_button,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=return_home_button,
                    alignment=ft.alignment.center)
            ],
            spacing=20
        )
    )

    def on_page_load():
        nonlocal robot_configure_list, num_robots
        robot_configure_list = []
        num_robots = 0
        widget_robots.controls.clear()
        world_combobox.value = None
        robot_combobox.value = None
        page.update()


    return {
        "view": configure_view,
        "title": title,
        "load": on_page_load
    }
