import flet as ft
from funciones import obtain_world_list, obtain_robot_list
from user_controls.world import World
from user_controls.robot import Robot

def ConfigureWorld(page: ft.Page):
    title = "Configurar mundos"

    world_list: list[World] = obtain_world_list("/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml")
    robot_list: list[Robot] = obtain_robot_list("/home/robot/app_multirobot/app_multi_robot/robots_register.yaml")

    world_combobox = ft.Dropdown(
        label="World",
        hint_text="Choose the world",
        options=[ft.dropdown.Option(world.name) for world in world_list])

    num_robots_input = ft.TextField(
        value="0",
        disabled=True,
        text_align="right",
        width=100)
    
    add_value = ft.IconButton(
        icon=ft.icons.REMOVE_CIRCLE,
    )
    
    reduce_value = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE
    )

    configure_view = ft.SafeArea(
        content=ft.Column(
            controls=[
                world_combobox,
                ft.Row(
                    controls=[
                        reduce_value,
                        num_robots_input,
                        add_value
                    ]
                )
            ]
        )
    )

    return configure_view
