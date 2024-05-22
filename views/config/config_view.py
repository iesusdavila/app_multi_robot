import flet as ft 
from user_controls.modelo import Modelo

def ConfigView(page, myPyrebase):
    # Datos iniciales
    title = "Configuraciones iniciales"

    predef_models = [
        Modelo("Turtlebot3 Burger", "", "", "/images/burger.jpg"),
        Modelo("Turtlebot3 Waffle", "", "", "/images/waffle.jpg"),
        Modelo("Turtlebot3 Waffle Pi", "", "", "/images/waffle_pi.jpg"),
        Modelo("Roombabot", "", "", "/images/roomba.jpg")
    ]

    modelos = list()

    def modelo_widget(modelo):
        nombre = ft.Text(modelo.nombre)
        image = ft.Image(src=modelo.image)
        rutaURDF = ft.TextField(label="Ruta del URDF")
        rutaSDF = ft.TextField(label="Ruta del SDF")

        widget = ft.Column(
            controls=[
                nombre,
                image,
                rutaURDF,
                rutaSDF
            ]
        )
        return widget

    def charge_models(models):
        for nombre in models.keys():
            modelos.append(Modelo(nombre, models[nombre]["rutaURDF"],models[nombre]["rutaSDF"],models[nombre]["imagen"]))
    
    def first_charge():
        for model in predef_models:
            myPyrebase.add_model(model.to_string())

    def clean_config():
        modelos.clear()
        page.update()

    def on_load():
        clean_config()
        modelos_db = myPyrebase.get_models()
        if modelos == None:
            first_charge()
        charge_models(modelos_db)
        continue_home = True
        for modelo in modelos:
            continue_home = continue_home and modelo.is_completed()
        if continue_home:
            page.go("/home")
            page.update()
            
    def handle_logout(*e):
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.go("/")
    
    view = ft.Column(
        controls=[
            ft.Container(ft.Text("Configuracion inicial", size=35, style=ft.TextStyle(weight=ft.FontWeight.BOLD)), alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=ft.Row(
                    controls=[
                        modelo_widget(modelos[0]),
                        modelo_widget(modelos[1]),
                        modelo_widget(modelos[2]),
                        modelo_widget(modelos[3])
                    ]
                )
            ),
            ft.Container(ft.ElevatedButton(text="Guardar configuracion", on_click=handle_logout), alignment=ft.MainAxisAlignment.CENTER)
        ]
    )
    return {
        "view": view,
        "title": title,
        "load": on_load
    }
