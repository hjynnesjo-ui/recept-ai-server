from flask import Flask, request, jsonify
from flask_cors import CORS
from recipe_scrapers import scrape_me

# Skapa Flask-app
app = Flask(__name__)

# Aktivera CORS så att WordPress (din domän) får prata med servern
CORS(app)

@app.route("/get-recipe", methods=["POST"])
def get_recipe():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"success": False, "error": "Ingen URL skickades."}), 400

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

if __name__ == "__main__":
    # Render använder gunicorn i produktion, men lokalt kan du köra denna
    app.run(host="0.0.0.0", port=5000)
