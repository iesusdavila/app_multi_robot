import flet as ft
from screens.login_screen import login_view

def main(page: ft.Page):
    page.add(login_view.info_user())

ft.app(main, assets_dir="assets")