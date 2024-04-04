import flet as ft

def HomeView(page, myPyreBase):
    title = "Home"

    add_robots_button = ft. ElevatedButton()
    robot_tasks_button = ft.ElevatedButton()
    logo_app_image = ft.Container()

    active_robot_text = ft.Text("Robots activos")

    myPage = ft.Container()

    def on_page_load():
        pass

    return {
        "view":myPage,
        "title": title,
        "load": on_page_load
    }
