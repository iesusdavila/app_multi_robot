import flet as ft

def info_user():
    imagen = ft.Container(content=ft.Image(src=f"/images/Fondo_inicio.jpg", width=500, height=500))
    encabezado = ft.Text("Bienvenido de vuelta", style=ft.TextStyle(weight=ft.FontWeight.W_500))
    email = ft.TextField(label="Email", autofocus=True, width=300)
    login_button = ft.ElevatedButton(text="Entrar", scale=1.5)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    forgot_pass = ft.Text("Olvido su contraseña?")

    area = ft.SafeArea(
        ft.Row(
            [
                ft.Container(imagen, expand=1),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(encabezado, alignment=ft.alignment.center),
                            ft.Container(email, alignment=ft.alignment.center),
                            ft.Container(password, alignment=ft.alignment.center),
                            ft.Container(login_button, alignment=ft.alignment.center),
                            ft.Container(forgot_pass, alignment=ft.alignment.center)
                        ],
                        spacing=27,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=1,
                    padding=ft.Padding(bottom=20.0, left=20.0, right=20.0, top=30.0)
                ),
            ]
        ),
        expand=True,
    )

    return area
