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
            print(data)  # Imprime a resposta para análise
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


def food_container(food):
    return ft.Container(
        width=500,
        height=1000,
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE10,
        border_radius=ft.border_radius.all(10),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value=food["food_name"], size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value=f"Descrição: {food['food_description']}")
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
