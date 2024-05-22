import flet as ft

# views
from views.dashboard.dashboard_view import DashboardView
from views.login.login_view import LoginView
from views.register.register_view import RegisterView
from views.config.config_view import ConfigView
from views.home.home_view import HomeView

import flet as ft

class Router:

    def __init__(self, page, myPyrebase):
        self.page = page
        self.routes = {
            "/": LoginView(page, myPyrebase),
            "/home": HomeView(page, myPyrebase),
            "/register": RegisterView(page, myPyrebase),
            # "/config": ConfigView(page, myPyrebase)
        }
        self.body = ft.Container(content=self.routes['/']["view"])

    def route_change(self, route):
        self.body.content = self.routes[route.route].get("view")
        self.page.title = self.routes[route.route].get("title")
        if self.routes[route.route].get("load"):
            self.routes[route.route].get("load")()
        self.page.update()
        