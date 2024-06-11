import flet as ft

# views
from views.dashboard.dashboard_view import DashboardView
from views.login.login_view import LoginView
from views.register.register_view import RegisterView
from views.home.home_view import HomeView
from views.modelo.modelo_view import ModeloView
from views.worlds.worlds_view import WorldsView
from views.gazebo.configure_world_view import ConfigureWorld
from views.gazebo.execute_gazebo import ExecuteGazebo

import flet as ft

class Router:

    def __init__(self, page, myPyrebase):
        self.page = page
        self.routes = {
            "/": LoginView(page, myPyrebase),
            "/home": HomeView(page),
            "/add_model": ModeloView(page),
            "/register": RegisterView(page, myPyrebase),
            "/worlds": WorldsView(page),
            "/configure": ConfigureWorld(page),
            "/execute": ExecuteGazebo(page)
        }
        self.body = ft.Container(content=self.routes['/']["view"])

    def route_change(self, route):
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        if self.routes[route.route].get("load"):
            self.routes[route.route].get("load")()
        self.page.update()
        