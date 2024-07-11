import flet as ft
from models.usuario import Usuario
from supabase.supabase_cliente import supabase

class RegistroInterface(ft.UserControl):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.page = app.page

        # Elementos de interface
        self.email_input = ft.TextField(label="Email", width=300)
        self.senha_input = ft.TextField(label="Senha", password=True, width=300)
        self.nome_input = ft.TextField(label="Nome", width=300)
        self.sexo_input = ft.Dropdown(
            label="Sexo",
            options=[
                ft.dropdown.Option("Masculino"),
                ft.dropdown.Option("Feminino")
            ],
            width=300
        )
        self.idade_input = ft.TextField(label="Idade", width=300)
        self.peso_input = ft.TextField(label="Peso (kg)", width=300)
        self.altura_input = ft.TextField(label="Altura (cm)", width=300)
        self.register_button = ft.ElevatedButton(text="Registrar", on_click=self.register)
        self.back_button = ft.ElevatedButton(text="Voltar", on_click=self.show_login)
        self.message = ft.Text("")

        # Layout
        self.controls.append(
            ft.Column(
                controls=[
                    self.email_input,
                    self.senha_input,
                    self.nome_input,
                    self.sexo_input,
                    self.idade_input,
                    self.peso_input,
                    self.altura_input,
                    self.register_button,
                    self.back_button,
                    self.message
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )

    def register(self, e):
        email = self.email_input.value
        senha = self.senha_input.value
        nome = self.nome_input.value
        sexo = self.sexo_input.value
        idade = int(self.idade_input.value)
        peso = float(self.peso_input.value)
        altura = float(self.altura_input.value)
        
        usuario = Usuario(email, senha, nome, sexo, idade, peso, altura)
        
        try:
            response = supabase.registrar_usuario(usuario)
            if response.get("error"):
                self.message.value = f"Erro: {response['error']['message']}"
            else:
                self.message.value = "Registro bem-sucedido! Faça login para continuar."
        except Exception as ex:
            self.message.value = f"Erro: {ex}"
        self.update()

    def show_login(self, e):
        self.app.show_login()
