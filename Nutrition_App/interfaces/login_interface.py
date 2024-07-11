import flet as ft
from supabase.supabase_cliente import supabase

class LoginInterface(ft.UserControl):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.page = app.page


        # Elementos de interface
        self.email_input = ft.TextField(label="Email", width=300)
        self.senha_input = ft.TextField(label="Senha", password=True, width=300)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)
        self.register_button = ft.ElevatedButton(text="Registrar", on_click=self.show_register)
        self.message = ft.Text("")

        # Layout
        self.controls.append(
            ft.Column(
                controls=[
                    self.email_input,
                    self.senha_input,
                    self.login_button,
                    self.register_button,
                    self.message
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )

    def login(self, e):
        email = self.email_input.value
        senha = self.senha_input.value
        try:
            response = supabase.autenticar_usuario(email, senha)
            if 'error' in response:  # Aqui pode ocorrer o erro
                self.message.value = f"Erro: {response['error']['message']}"
            else:
                self.message.value = "Login bem-sucedido!"
                self.app.show_home()  # Navegar para a página inicial após login bem-sucedido
        except Exception as ex:
            self.message.value = f"Erro: {ex}"
        self.update()

    def show_register(self, e):
        self.app.show_register()
