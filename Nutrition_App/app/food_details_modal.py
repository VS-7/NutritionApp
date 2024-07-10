import flet as ft
from database import get_food_details

class FoodDetailsModal:
    def __init__(self, page):
        self.page = page

    async def show(self, food_id):
        food = await get_food_details(food_id)
        if food:
            food_details = ft.Container(
                padding=ft.padding.all(20),
                border_radius=ft.border_radius.all(10),
                content=ft.Column(
                    controls=[
                        ft.Text(value="Valores nutricionais com base em 100g do alimento", size=12),
                        ft.Text(value=food.name, size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(value="Macronutrientes", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(value=f"Calorias: {food.calories} kcal"),
                        ft.Text(value=f"Proteínas: {food.protein} g"),
                        ft.Text(value=f"Carboidratos: {food.carbs} g"),
                        ft.Text(value=f"Lipídios: {food.fat} g"),
                        ft.Text(value=f"Fibra: {food.fiber} g"),
                        ft.Text(value="Micronutrientes", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(value=f"Calcio: {food.calcium} mg"),
                        ft.Text(value=f"Magnésio: {food.magnesium} mg"),
                        ft.Text(value=f"Manganês: {food.manganese} mg"),
                        ft.Text(value=f"Fósforo: {food.phosphorus} mg"),
                        ft.Text(value=f"Ferro: {food.iron} mg"),
                        ft.Text(value=f"Sódio: {food.sodium} mg"),
                        ft.Text(value=f"Potássio: {food.potassium} mg"),
                        ft.Text(value=f"Cobre: {food.copper} mg"),
                        ft.Text(value=f"Zinco: {food.zinc} mg"),
                        ft.Text(value=f"Retinol: {food.retinol} mcg"),
                        ft.Text(value=f"Tiamina: {food.thiamine} mg"),
                        ft.Text(value=f"Riboflavina: {food.riboflavin} mg"),
                        ft.Text(value=f"Piridoxina: {food.pyridoxine} mg"),
                        ft.Text(value=f"Niacina: {food.niacin} mg"),
                        ft.Text(value=f"Vitamina C: {food.vitaminC} mg"),
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
