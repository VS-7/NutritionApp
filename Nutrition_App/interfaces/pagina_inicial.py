import flet as ft
from supabase.supabase_cliente import supabase

class PaginaInicial(ft.UserControl):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.page = app.page


        # Título
        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    value='FOOD FINDER',
                    weight=ft.FontWeight.BOLD,
                    size=20,
                ),
                ft.Icon(
                    ft.icons.FOOD_BANK,
                    color=ft.colors.WHITE,
                    size=30
                ),
            ]
        )

        # Barra de pesquisa
        self.searchbar = ft.TextField(
            prefix_icon=ft.icons.SEARCH,
            hint_text='Digite o nome do alimento...',
            on_submit=self.search,
            border_radius=ft.border_radius.all(10),
        )

        # Grade de alimentos
        self.foods_grid = ft.GridView(
            expand=True,
            max_extent=300,
            controls=[],
            child_aspect_ratio=3.0,
        )

        # Layout principal
        self.layout = ft.Column(
            expand=True,
            controls=[
                self.title,
                self.searchbar,
                self.foods_grid,
            ]
        )

        self.controls.append(self.layout)

    def search(self, e):
        query = e.control.value
        foods = self.search_foods(query)
        if not foods:
            self.foods_grid.controls = [ft.Text("Nenhum alimento encontrado.")]
        else:
            self.foods_grid.controls = [self.food_container(food) for food in foods]
        self.foods_grid.update()

    def search_foods(self, query):
        response = supabase.table('alimentos').select('*').ilike('alimento', f'%{query}%').execute()
        foods = response.get('data', [])
        return foods

    def food_container(self, food):
        return ft.Container(
            padding=ft.padding.all(10),
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(value=food['alimento'], size=15, weight=ft.FontWeight.BOLD),
                ],
                width=500,
            ),
            on_click=lambda e: self.show_food_details(food['id'])
        )

    def show_food_details(self, food_id):
        food = self.get_food_details(food_id)
        if food:
            food_details = ft.Container(
                padding=ft.padding.all(20),
                border_radius=ft.border_radius.all(10),
                content=ft.Column(
                    controls=[
                        ft.Text(value="Valores nutricionais com base em 100g do alimento", size=12),
                        ft.Text(value=food['alimento'], size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(value="Macronutrientes", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(value=f"Calorias: {food['caloria_kcal']} kcal"),
                        ft.Text(value=f"Proteínas: {food['proteina']} g"),
                        ft.Text(value=f"Carboidratos: {food['carboidrato']} g"),
                        ft.Text(value=f"Lipídios: {food['lipideos']} g"),
                        ft.Text(value=f"Fibra: {food['fibra']} g"),
                        ft.Text(value="Micronutrientes", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(value=f"Cálcio: {food['calcio']} mg"),
                        ft.Text(value=f"Magnésio: {food['magnesio']} mg"),
                        ft.Text(value=f"Manganês: {food['manganes']} mg"),
                        ft.Text(value=f"Fósforo: {food['fosforo']} mg"),
                        ft.Text(value=f"Ferro: {food['ferro']} mg"),
                        ft.Text(value=f"Sódio: {food['sodio']} mg"),
                        ft.Text(value=f"Potássio: {food['potassio']} mg"),
                        ft.Text(value=f"Cobre: {food['cobre']} mg"),
                        ft.Text(value=f"Zinco: {food['zinco']} mg"),
                        ft.Text(value=f"Retinol: {food['retinol']} mcg"),
                        ft.Text(value=f"Tiamina: {food['tiamina']} mg"),
                        ft.Text(value=f"Riboflavina: {food['riboflavina']} mg"),
                        ft.Text(value=f"Piridoxina: {food['piridoxina']} mg"),
                        ft.Text(value=f"Niacina: {food['niacina']} mg"),
                        ft.Text(value=f"Vitamina C: {food['vitamina_c']} mg"),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=500,
                height=700,
            )
            modal = ft.AlertDialog(
                bgcolor=ft.colors.BLACK87,
                title=ft.Text("Detalhes do Alimento"),
                content=food_details,
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: self.page.update()
            )
            self.page.dialog = modal
            modal.open = True
            self.page.update()

    def get_food_details(self, food_id):
        response = supabase.table('alimentos').select('*').eq('id', str(food_id)).execute()
        food = response.get('data', [None])[0]
        return food
