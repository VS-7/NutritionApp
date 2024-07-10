import flet as ft
from food_finder import FoodFinder

def main(page: ft.Page):
    page.padding = ft.padding.all(30)
    
    food_finder = FoodFinder(page)
    food_finder.build()

if __name__ == "__main__":
    ft.app(target=main)
