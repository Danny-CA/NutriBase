import requests
import pandas as pd

# Spoonacular API key
API_KEY = "1c960c28f635462f88735f977c1a19c1"  # Replace with your Spoonacular API key

# Base URL for the random recipe endpoint
BASE_URL = "https://api.spoonacular.com/recipes/random"

# Parameters for the API request
params = {
    "apiKey": API_KEY,
    "includeNutrition": True,  # Include nutritional information
    "number": 140  # Number of random recipes to fetch
}

# Make the API request
response = requests.get(BASE_URL, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Check if recipes are returned
    if "recipes" in data and len(data["recipes"]) > 0:
        # List to store recipe data
        recipes_data = []

        # Loop through each recipe
        for recipe in data["recipes"]:
            # Extract recipe details (with missing value handling)
            recipe_details = {
                "Title": recipe.get("title", "N/A"),
                "Servings": recipe.get("servings", "N/A"),
                "Ready in (minutes)": recipe.get("readyInMinutes", "N/A"),
                "Source URL": recipe.get("sourceUrl", "N/A"),
                "Image": recipe.get("image", "N/A"),
                "Calories": recipe.get("nutrition", {}).get("nutrients", [{}])[0].get("amount", "N/A"),
                "Carbs (g)": recipe.get("nutrition", {}).get("nutrients", [{}])[1].get("amount", "N/A"),
                "Fat (g)": recipe.get("nutrition", {}).get("nutrients", [{}])[2].get("amount", "N/A"),
                "Protein (g)": recipe.get("nutrition", {}).get("nutrients", [{}])[3].get("amount", "N/A")
            }
            recipes_data.append(recipe_details)

        # Convert the list of recipes to a DataFrame
        df = pd.DataFrame(recipes_data)

        # Save the DataFrame to a CSV file
        output_csv = "random_recipes.csv"
        df.to_csv(output_csv, index=False)

        print(f"Successfully saved {len(recipes_data)} recipes to {output_csv}")
    else:
        print("No recipes found in the response.")
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print the error message from the API