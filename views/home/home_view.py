import flet as ft
import yaml

def HomeView(page, myPyrebase):
    title = "Home"

    add_robots_button = ft. ElevatedButton()
    robot_tasks_button = ft.ElevatedButton()
    logo_app_image = ft.Container()

    def build_robots():
        all_robots.clear()
        data = myPyrebase.get_robots()
        pass

    active_robot_text = ft.Text("Robots disponibles", size=30, style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    robot_list_view = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    all_robots = []

    myPage = ft.SafeArea(
        expand=True,
        content=ft.Row(
            controls=[
                active_robot_text,
                robot_list_view,
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
