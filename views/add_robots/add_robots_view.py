from flet import Page, UserControl, Column
from funciones import *

def AddRobotsView(page: Page):
    ruta_ws = "/home/robot/multirobot_ws"
    page.title = "Add Robots"

    def on_page_load():
        pass

    def load_robots(ruta_ws: str):
        robot_list = obtain_robots_list(ruta_ws)

    def build_list_robots(robot_list: list):
        table = Column(
            controls=robot_list,
            
        )