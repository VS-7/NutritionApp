import flet as ft
import sqlite3

# Função para buscar alimentos no banco de dados SQLite
def search_foods(query):
    connection = sqlite3.connect('tabela_alimentos.db')  # Conecta ao banco de dados SQLite
    cursor = connection.cursor()

    # Query para buscar alimentos pelo nome
    query = f"SELECT * FROM alimentos WHERE alimento LIKE '%{query}%'"
    cursor.execute(query)
    foods = cursor.fetchall()

    connection.close()
    return foods

# Função para obter detalhes do alimento no banco de dados SQLite
def get_food_details(food_id):
    connection = sqlite3.connect('tabela_alimentos.db')  # Conecta ao banco de dados SQLite
    cursor = connection.cursor()

    # Query para obter detalhes de um alimento pelo ID
    query = f"SELECT * FROM alimentos WHERE id = '{food_id}'"
    cursor.execute(query)
    food = cursor.fetchone()

    connection.close()
    return food

# Função para criar o container de exibição de alimentos
def food_container(food, on_click):
    return ft.Container(
        padding=ft.padding.all(10),
        bgcolor=ft.colors.WHITE10,
        border_radius=ft.border_radius.all(10),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(value=food[1], size=15, weight=ft.FontWeight.BOLD),  # Nome do alimento
            ],
            width=500,
        ),
        on_click=lambda e: on_click(e.page, food[0])  # Passa a página e o ID do alimento
    )

# Função para exibir o modal com detalhes do alimento
def show_food_details(page, food_id):
    food = get_food_details(food_id)
    if food:
        food_details = ft.Container(
            padding=ft.padding.all(20),
            
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                controls=[
                    ft.Text(value="Valores nutricionais com base em 100g do alimento", size=12),
                    ft.Text(value=food[1], size=24, weight=ft.FontWeight.BOLD),  # Nome do alimento
                    ft.Text(value="Macronutrientes", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(value=f"Calorias: {food[3]} kcal"),# Calorias
                    ft.Text(value=f"Proteínas: {food[5]} g"),  # Proteínas
                    ft.Text(value=f"Carboidratos: {food[8]} g"),  # Carboidratos
                    ft.Text(value=f"Lipídios: {food[6]} g"), # Lipídios
                    ft.Text(value=f"Fibra: {food[9]} g"),
                    ft.Text(value="Micronutrientes",  size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(value=f"Calcio: {food[11]} mg"),
                    ft.Text(value=f"Magnésio: {food[12]} mg"),
                    ft.Text(value=f"Manganês: {food[13]} mg"),
                    ft.Text(value=f"Fósforo: {food[14]} mg"),
                    ft.Text(value=f"Ferro: {food[15]} mg"),
                    ft.Text(value=f"Sódio: {food[16]} mg"),
                    ft.Text(value=f"Potássio: {food[17]} mg"),
                    ft.Text(value=f"Cobre: {food[18]} mg"),
                    ft.Text(value=f"Zinco: {food[19]} mg"),
                    ft.Text(value=f"Retinol: {food[20]} mcg"),
                    ft.Text(value=f"Tiamina: {food[23]} mg"),
                    ft.Text(value=f"Riboflavina: {food[24]} mg"),
                    ft.Text(value=f"Piridoxina: {food[25]} mg"),
                    ft.Text(value=f"Niacina: {food[26]} mg"),
                    ft.Text(value=f"Vitamina C: {food[27]} mg"),
                    # Adicione mais informações nutricionais aqui conforme necessário
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
            on_dismiss=lambda e: page.update()  # Atualiza a página ao fechar o modal
        )
        page.dialog = modal
        modal.open = True
        page.update()

# Função principal que cria a interface do aplicativo
def main(page: ft.Page):
    page.padding=ft.padding.all(30)
    
    
    
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
    
    # Função de busca de alimentos
    def search(e):
        query = e.control.value
        foods = search_foods(query)
        if not foods:
            foods_grid.controls = [ft.Text("Nenhum alimento encontrado.")]
        else:
            foods_grid.controls = [food_container(food, show_food_details) for food in foods]
        foods_grid.update()
    
    # Barra de pesquisa
    searchbar = ft.TextField(
        prefix_icon=ft.icons.SEARCH,
        hint_text='Digite o nome do alimento...',
        on_submit=search,
        border_radius=ft.border_radius.all(10),
    )
    
    # Grade de alimentos
    foods_grid = ft.GridView(
        expand=True,
        max_extent=300,
        controls=[],
        child_aspect_ratio=3.0,
    )
    
    # Layout principal
    layout = ft.Column(
        expand=True,
        controls=[
            title,
            searchbar,
            foods_grid,
        ]
    )
    
    # Adiciona o layout à página
    page.add(layout)
    
if __name__ == "__main__":
    ft.app(target=main)
