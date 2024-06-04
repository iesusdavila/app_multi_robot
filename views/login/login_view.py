import flet as ft

def LoginView(page, myPyrebase):
    title = "Login"

    def on_page_load():
        if myPyrebase.check_token():
            page.go('/home')

    def handle_sign_in(e):
        try:
            myPyrebase.sign_in(email.value, password.value)
            email.value = ""
            password.value = ""
            page.go('/home')
        except:
            handle_sign_in_error()
            page.update()

    def handle_sign_in_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Credenciales incorrectas. Intente de nuevo.", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()

    def handle_register(e):
        page.go("/register")

    def highlight_link(e):
        e.control.style.color = ft.colors.BLUE
        e.control.update()

    def unhighlight_link(e):
        e.control.style.color = None
        e.control.update()

    # Componentes del view
    imagen = ft.Image(src=f"/images/Fondo_inicio.jpg", width=500, height=500, expand=1)
    encabezado = ft.Text("Bienvenido", style=ft.TextStyle(weight=ft.FontWeight.W_500), text_align=ft.TextAlign.CENTER, expand=1)
    email = ft.TextField(label="Email", autofocus=True, width=300, expand=1)
    login_button = ft.ElevatedButton(text="Entrar", scale=1.5, on_click=handle_sign_in, expand=1)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, expand=1)
    text_register = ft.Text(
        disabled= False,
        expand=1,
        spans= [
            ft.TextSpan("¿No tienes una cuenta? "),
            ft.TextSpan(
                "¡Registrate!",
                style=ft.TextStyle(italic=True),
                on_enter=highlight_link,
                on_exit=unhighlight_link,
                on_click=handle_register
            )
        ]
    )

    myPage = ft.SafeArea(
        ft.Row(
            [
                ft.Container(imagen, expand=1, alignment=ft.alignment.center),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(encabezado, alignment=ft.alignment.center),
                            ft.Container(email, alignment=ft.alignment.center),
                            ft.Container(password, alignment=ft.alignment.center),
                            ft.Container(login_button, alignment=ft.alignment.center),
                            ft.Container(text_register, alignment=ft.alignment.center)
                        ],
                        spacing=30,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    expand=1,
                    padding=ft.Padding(bottom=20.0, left=20.0, right=20.0, top=30.0),
                    alignment=ft.alignment.center
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        expand=True,
        adaptive=True
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
