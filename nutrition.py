import flet as ft
import requests

# Função para buscar alimentos na nossa API
def search_foods(query):
    url = "https://servernutritionapp.vercel.app/foods"  # Substitua pela URL da sua API
    response = requests.get(url)
    if response.status_code == 200:
        foods = response.json()
        filtered_foods = [food for food in foods if query.lower() in food["name"].lower()]
        return filtered_foods
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# Função para obter detalhes do alimento na nossa API
def get_food_details(food_id):
    url = f"http://localhost:3000/foods/{food_id}"  # Substitua pela URL da sua API
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return {}

def food_container(food):
    return ft.Container(
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE10,
        border_radius=ft.border_radius.all(10),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value=food["name"], size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value=f"Calorias: {food['energy_kcal']} kcal"),
                ft.Text(value=f"Proteínas: {food['protein_g']} g"),
                ft.Text(value=f"Carboidratos: {food['carbohydrate_total']} g"),
                ft.Text(value=f"Lipídios: {food['lipids_g']} g")
            ],
            width=500,
            height=1500,    
        ),
    )

def main(page: ft.Page):
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
    
    def search(e):
        query = e.control.value
        foods = search_foods(query)
        if not foods:
            foods_grid.controls = [ft.Text("Nenhum alimento encontrado.")]
        else:
            foods_grid.controls = [food_container(food) for food in foods]
        foods_grid.update()
    
    searchbar = ft.TextField(
        prefix_icon=ft.icons.SEARCH,
        hint_text='Digite o nome do alimento...',
        on_submit=search,
        border_radius=ft.border_radius.all(10)
    )
    
    foods_grid = ft.GridView(
        expand=True,
        max_extent=600,
        controls=[],
        child_aspect_ratio=3.0,
    )
    
    layout = ft.Column(
        expand=True,
        controls=[
            title,
            searchbar,
            foods_grid,
        ]
    )
    
    page.add(layout)
    
if __name__ == "__main__":
    ft.app(target=main)
