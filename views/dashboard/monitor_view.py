import flet as ft

def MonitorView(page: ft.Page):
    title = "Monitoreo de tareas"

    label_title = ft.Text(
        value="Monitoreo de datos",
        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        size=40)
    
    image_process = ft.Image(
        src=f"/images/construccion.jpg",
        fit=ft.ImageFit.FILL, 
        width=500,
        height=500,
        expand=1)

    def return_home(e):
        page.go("/home")
        page.update()

    return_home_button = ft.ElevatedButton(
        text="Regresar a home",
        icon=ft.icons.HOME,
        on_click=return_home
    )

    def on_page_load():
        pass

    monitor_view = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=40,
            controls=[
                ft.Container(
                    content=label_title,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=image_process,
                    alignment=ft.alignment.center),
                ft.Container(
                    content=return_home_button,
                    alignment=ft.alignment.center)
            ]
        )
    )

    return {
        "view":monitor_view,
        "title": title,
        "load": on_page_load
    }