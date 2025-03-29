import requests
import pandas as pd

API_KEY = "********"  # Reemplázalo con tu API key (token)

# Base URL for the random recipe endpoint
BASE_URL = "https://api.spoonacular.com/recipes/random"

# Parámetros para la API
params = {
    "apiKey": API_KEY,
    "includeNutrition": True,  # Incluir información nutricional
    "number": 100  # Número de recetas
}

# Hacer la solicitud a la API
response = requests.get(BASE_URL, params=params)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()

    # Verificar si hay recetas en la respuesta
    if "recipes" in data and len(data["recipes"]) > 0:
        recipes_data = []

        for recipe in data["recipes"]:
            # Extraer lista de ingredientes
            ingredients = [
                ingredient["original"] for ingredient in recipe.get("extendedIngredients", [])
            ]

            # Extraer instrucciones (algunas recetas no tienen instrucciones)
            instructions = recipe.get("instructions", "No instructions available")

            recipe_details = {
                "Title": recipe.get("title", "N/A"),
                "Servings": recipe.get("servings", "N/A"),
                "Ready in (minutes)": recipe.get("readyInMinutes", "N/A"),
                "Source URL": recipe.get("sourceUrl", "N/A"),
                "Image": recipe.get("image", "N/A"),
                "Calories": recipe.get("nutrition", {}).get("nutrients", [{}])[0].get("amount", "N/A"),
                "Carbs (g)": recipe.get("nutrition", {}).get("nutrients", [{}])[1].get("amount", "N/A"),
                "Fat (g)": recipe.get("nutrition", {}).get("nutrients", [{}])[2].get("amount", "N/A"),
                "Protein (g)": recipe.get("nutrition", {}).get("nutrients", [{}])[3].get("amount", "N/A"),
                "Ingredients": ", ".join(ingredients),  # Unir ingredientes en una sola celda
                "Instructions": instructions.replace("\n", " ")  # Evitar saltos de línea en CSV
            }
            recipes_data.append(recipe_details)

        # Convertir a DataFrame y guardar en CSV
        df = pd.DataFrame(recipes_data)
        output_csv = "random_recipes_with_ingredients_and_instructions.csv"
        df.to_csv(output_csv, index=False)

        print(f"✅ Guardadas {len(recipes_data)} recetas en {output_csv}")
    else:
        print("⚠️ No se encontraron recetas en la respuesta.")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
