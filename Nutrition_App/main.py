import flet as ft
from interfaces.login_interface import LoginInterface
from interfaces.registro_interface import RegistroInterface
from interfaces.pagina_inicial import PaginaInicial

class App:
    def __init__(self, page):
        self.page = page
        self.page.title = 'FoodFinder'
        self.login_interface = LoginInterface(self)
        self.registro_interface = RegistroInterface(self)
        self.pagina_inicial = PaginaInicial(self)
        self.show_login()

    def show_login(self):
        self.page.clean()
        self.page.add(self.login_interface)

    def show_register(self):
        self.page.clean()
        self.page.add(self.registro_interface)

    def show_home(self):
        self.page.clean()
        self.page.add(self.pagina_inicial)

def main(page: ft.Page):
    app = App(page)

ft.app(target=main)
