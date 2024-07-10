import flet as ft
from food_details_modal import FoodDetailsModal
from database import search_foods

class FoodFinder:
    def __init__(self, page):
        self.page = page
        self.food_details_modal = FoodDetailsModal(self.page)
        self.foods_grid = ft.GridView(
            expand=True,
            max_extent=300,
            controls=[],
            child_aspect_ratio=3.0,
        )

    def build(self):
        title = ft.Row(
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
        
        searchbar = ft.TextField(
            prefix_icon=ft.icons.SEARCH,
            hint_text='Digite o nome do alimento...',
            on_submit=self.search,
            border_radius=ft.border_radius.all(10),
        )
        
        layout = ft.Column(
            expand=True,
            controls=[
                title,
                searchbar,
                self.foods_grid,
            ]
        )
        
        self.page.add(layout)
    
    def search(self, e):
        query = e.control.value
        self.update_foods_grid(query)
    
    async def update_foods_grid(self, query):
        foods = await search_foods(query)
        if not foods:
            self.foods_grid.controls = [ft.Text("Nenhum alimento encontrado.")]
        else:
            self.foods_grid.controls = [
                self.food_container(food) for food in foods
            ]
        self.foods_grid.update()

    def food_container(self, food):
        return ft.Container(
            padding=ft.padding.all(10),
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(value=food.name, size=15, weight=ft.FontWeight.BOLD),
                ],
                width=500,
            ),
            on_click=lambda e: self.food_details_modal.show(food.id)
        )
