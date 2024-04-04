import flet as ft

def LoginView(page, myPyrebase):
    title = "Login"

    def on_page_load():
        if myPyrebase.check_token():
            page.go('/home')

    def handle_sign_in(e):
        try:
            myPyrebase.sign_in(email.value, password.value)
            password.value = ""
            page.go('/home')
        except:
            handle_sign_in_error()
            page.update()

    def handle_sign_in_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Credenciales incorrectas. Intente de nuevo.", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()

    def handle_register(e):
        page.go("/home")

    # Componentes del view
    imagen = ft.Container(content=ft.Image(src=f"/images/Fondo_inicio.jpg", width=500, height=500))
    encabezado = ft.Text("Bienvenido de vuelta", style=ft.TextStyle(weight=ft.FontWeight.W_500))
    email = ft.TextField(label="Email", autofocus=True, width=300)
    login_button = ft.ElevatedButton(text="Entrar", scale=1.5, on_click=handle_sign_in)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    forgot_pass = ft.ElevatedButton(text="Registrarse", scale=1.5, on_click=handle_register)

    myPage = ft.SafeArea(
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

    return {
        "view": myPage,
        "title": title,
        "load": on_page_load
    }


# def info_user():
#     imagen = ft.Container(content=ft.Image(src=f"/images/Fondo_inicio.jpg", width=500, height=500))
#     encabezado = ft.Text("Bienvenido de vuelta", style=ft.TextStyle(weight=ft.FontWeight.W_500))
#     email = ft.TextField(label="Email", autofocus=True, width=300)
#     login_button = ft.ElevatedButton(text="Entrar", scale=1.5, on_click=login)
#     password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
#     forgot_pass = ft.Text("Olvido su contraseña?")

#     def login():
#         email_text = email.value
#         pass_text = password.value

#         try:
#             user = firebase_admin.auth()
            

#     area = ft.SafeArea(
#         ft.Row(
#             [
#                 ft.Container(imagen, expand=1),
#                 ft.Container(
#                     content=ft.Column(
#                         [
#                             ft.Container(encabezado, alignment=ft.alignment.center),
#                             ft.Container(email, alignment=ft.alignment.center),
#                             ft.Container(password, alignment=ft.alignment.center),
#                             ft.Container(login_button, alignment=ft.alignment.center),
#                             ft.Container(forgot_pass, alignment=ft.alignment.center)
#                         ],
#                         spacing=27,
#                         alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                     expand=1,
#                     padding=ft.Padding(bottom=20.0, left=20.0, right=20.0, top=30.0)
#                 ),
#             ]
#         ),
#         expand=True,
#     )

#     return area
