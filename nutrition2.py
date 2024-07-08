import flet as ft
import requests

# Função para obter um token de acesso da API FatSecret
def get_access_token(consumer_key, consumer_secret):
    url = "https://oauth.fatsecret.com/connect/token"
    data = {
        "grant_type": "client_credentials",
        "scope": "basic",
        "client_id": consumer_key,
        "client_secret": consumer_secret
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token", None)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Função para buscar alimentos
def search_foods(query, access_token):
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "foods" in data and "food" in data["foods"]:
            return data["foods"]["food"]
        else:
            print("No foods found.")
            return []
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# Função para obter detalhes do alimento
def get_food_details(food_id, access_token):
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "method": "food.get",
        "food_id": food_id,
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("food", {})
    else:
        print(f"Error {response.status_code}: {response.text}")
        return {}

def food_container(food, on_click):
    return ft.Container(
        width=500,
        height=1500,
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE10,
        border_radius=ft.border_radius.all(10),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value=food["food_name"], size=15, weight=ft.FontWeight.BOLD),
                ft.Text(value=f"Descrição: {food['food_description']}"),
                ft.ElevatedButton(
                    text="Ver detalhes",
                    on_click=lambda e: on_click(e, food["food_id"])
                )
            ]    
        ),
    )

def food_details_container(food_details, on_back):
    nutrients = food_details.get("servings", {}).get("serving", [])
    if not nutrients:
        return ft.Container(
            width=500,
            height=1000,
            padding=ft.padding.all(10),
            bgcolor=ft.colors.WHITE10,
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("No nutrition information available."),
                    ft.ElevatedButton(
                        text="Voltar",
                        on_click=on_back
                    )
                ]
            )
        )

    
    image_url = food_details.get("food_images", {}).get("food_image", [{}])[0].get("image_url", "")
    
    return ft.Container(
        width=500,
        height=1500,
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE10,
        border_radius=ft.border_radius.all(10),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value=food_details["food_name"], size=30, weight=ft.FontWeight.BOLD),
                ft.Image(src=image_url) if image_url else ft.Text("No image available"),
                ft.Text(value=f"Calorias: {nutrients.get('calories', 'N/A')} kcal"),
                ft.Text(value=f"Carboidratos: {nutrients.get('carbohydrate', 'N/A')} g"),
                ft.Text(value=f"Proteínas: {nutrients.get('protein', 'N/A')} g"),
                ft.Text(value=f"Gorduras: {nutrients.get('fat', 'N/A')} g"),
                ft.Text(value=f"Fibras: {nutrients.get('fiber', 'N/A')} g"),
                ft.Text(value=f"Açúcares: {nutrients.get('sugar', 'N/A')} g"),
                ft.Text(value=f"Colesterol: {nutrients.get('cholesterol', 'N/A')} mg"),
                ft.Text(value=f"Sódio: {nutrients.get('sodium', 'N/A')} mg"),
                ft.Text(value=f"Potássio: {nutrients.get('potassium', 'N/A')} mg"),
                ft.Text(value=f"Vitaminas: A-{nutrients.get('vitamin_a', 'N/A')} IU, C-{nutrients.get('vitamin_c', 'N/A')} mg, D-{nutrients.get('vitamin_d', 'N/A')} IU"),
                ft.Text(value=f"Minerais: Cálcio-{nutrients.get('calcium', 'N/A')} mg, Ferro-{nutrients.get('iron', 'N/A')} mg"),
                ft.ElevatedButton(
                    text="Voltar",
                    on_click=on_back
                )
            ]
        ),
    )

def main(page: ft.Page):
    consumer_key = "326b760948b34675a9dfb2c070f8b11b"
    consumer_secret = "7546d7068c274d5ab415a8ff88123658"
    access_token = get_access_token(consumer_key, consumer_secret)

    if not access_token:
        page.add(ft.Text("Erro ao obter token de acesso. Verifique as credenciais da API."))
        return

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
        foods = search_foods(query, access_token)
        if not foods:
            foods_grid.controls = [ft.Text("Nenhum alimento encontrado.")]
        else:
            foods_grid.controls = [food_container(food, show_food_details) for food in foods]
        foods_grid.update()
    
    def show_food_details(e, food_id):
        food_details = get_food_details(food_id, access_token)
        details_container.content = food_details_container(food_details, back_to_search)
        details_container.update()
        details_container.visible = True
        search_container.visible = False
        page.update()
    
    def back_to_search(e):
        details_container.visible = False
        search_container.visible = True
        page.update()
    
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
    
    details_container = ft.Container(visible=False)

    search_container = ft.Column(
        expand=True,
        controls=[
            title,
            searchbar,
            foods_grid,
        ]
    )

    layout = ft.Stack(
        expand=True,
        controls=[
            search_container,
            details_container
        ]
    )
    
    page.add(layout)
    
if __name__ == "__main__":
    ft.app(target=main)
