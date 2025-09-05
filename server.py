from flask import Flask, request, jsonify
from recipe_scrapers import scrape_me

# Här skapas Flask-appen
app = Flask(__name__)

@app.route("/get-recipe", methods=["POST"])
def get_recipe():
    data = request.json
    url = data.get("url")
    try:
        scraper = scrape_me(url)
        recipe = {
            "title": scraper.title(),
            "ingredients": scraper.ingredients(),
            "instructions": scraper.instructions(),
            "yields": scraper.yields(),
        }
        return jsonify({"success": True, "recipe": recipe})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Den här delen ska vara kvar, men Render använder inte den
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
