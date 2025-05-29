
import pandas as pd

class Ingredient:
    def __init__(self, row):
        self.id = row['Raw Material ID']
        self.similarity_index = row['Similarity Index']
        self.melting_point = row['Melting Point']
        self.availability = row['Availability in Country']
        self.price = float(str(row['Price']).replace('$', '').strip())

    def is_available_in_china(self):
        return 'except China' not in self.availability

class RecipeOptimizer:
    def __init__(self, ingredients_df):
        self.ingredients_df = ingredients_df
        print(self.ingredients_df)
        self.ingredients_df.columns = self.ingredients_df.columns.str.strip()
        self.ingredients = [Ingredient(row) for _, row in self.ingredients_df.iterrows()]
        self.original_recipe = {
            '6Z9K9FXGBN9Y1GXA': 0.10,
            'P5XJ8TYFZZPV79EX': 0.20,
            'X5VC25AYKD8CE3Z0': 0.70
        }
        self.final_recipe = {}

    def find_substitute(self, target_id, similarity_tol=100, melting_point_tol=20):
        target_ingredient = next((ing for ing in self.ingredients if ing.id == target_id), None)
        if not target_ingredient:
            raise ValueError(f"Target ingredient {target_id} not found.")

        for item in self.ingredients:
            if (item.is_available_in_china() and
                abs(item.similarity_index - target_ingredient.similarity_index) <= similarity_tol and
                abs(item.melting_point - target_ingredient.melting_point) <= melting_point_tol):
                return item
        return None

    def optimize(self):
        for item_id, pct in self.original_recipe.items():
            item = next((i for i in self.ingredients if i.id == item_id), None)
            if item and item.is_available_in_china():
                self.final_recipe[item_id] = pct
            else:
                substitute = self.find_substitute(item_id)
                if substitute:
                    self.final_recipe[substitute.id] = pct
                else:
                    raise ValueError(f"No substitute found for {item_id}")

    def calculate_cost_and_melting_point(self):
        total_cost = 0
        total_melting_point = 0
        for item_id, pct in self.final_recipe.items():
            item = next((i for i in self.ingredients if i.id == item_id), None)
            total_cost += item.price * pct
            total_melting_point += item.melting_point * pct
        return total_cost, total_melting_point

    def display_recipe(self):
        print("Final Recipe Composition:")
        for k, v in self.final_recipe.items():
            print(f"{k}: {v*100:.0f}%")
        cost, mp = self.calculate_cost_and_melting_point()
        print(f"Total Cost: ${cost:.2f}")
        print(f"Average Melting Point: {mp:.2f}°C")

if __name__ == "__main__":
    df = pd.read_csv("ingredients_info.csv")
    optimizer = RecipeOptimizer(df)
    optimizer.optimize()
    optimizer.display_recipe()
