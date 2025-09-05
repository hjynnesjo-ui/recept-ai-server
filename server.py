from flask import Flask, request, jsonify
from flask_cors import CORS
from recipe_scrapers import scrape_me
import re

app = Flask(__name__)
CORS(app)

# Enkel tabell för konvertering (kan byggas ut)
unit_map = {
    "cup": "2,4 dl",
    "cups": "2,4 dl",
    "ounce": "28 g",
    "ounces": "28 g",
    "oz": "28 g",
    "pound": "450 g",
    "pounds": "450 g",
    "tbsp": "msk",
    "tablespoon": "msk",
    "tablespoons": "msk",
    "tsp": "tsk",
    "teaspoon": "tsk",
    "teaspoons": "tsk"
}

# Enkel eng→sv ordlista för ingredienser (kan byggas ut)
word_map = {
    "egg": "ägg",
    "milk": "mjölk",
    "flour": "mjöl",
    "sugar": "socker",
    "salt": "salt",
    "butter": "smör",
    "water": "vatten",
    "cream": "grädde"
}

def translate_and_convert(text):
    # konvertera mått
    for en, sv in unit_map.items():
        text = re.sub(rf"\b{en}\b", sv, text, flags=re.IGNORECASE)

    # översätt vanliga ord
    for en, sv in word_map.items():
        text = re.sub(rf"\b{en}\b", sv, text, flags=re.IGNORECASE)

    return text

@app.route("/get-recipe", methods=["POST"])
def get_recipe():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"success": False, "error": "Ingen URL skickades."}), 400

    try:
        scraper = scrape_me(url)
        recipe = {
            "title": translate_and_convert(scraper.title()),
            "ingredients": [translate_and_convert(i) for i in scraper.ingredients()],
            "instructions": translate_and_convert(scraper.instructions()),
            "yields": translate_and_convert(scraper.yields() or "")
        }
        return jsonify({"success": True, "recipe": recipe})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
