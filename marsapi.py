from flask import Flask, render_template
import requests

app = Flask(__name__)

NASA_API_URL = "https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0"

@app.route("/")
def index():
    try:
        # Call the NASA API
        response = requests.get(NASA_API_URL)
        data = response.json()

        # Get the latest sol (Martian day)
        sols = data.get('sol_keys', [])
        latest_sol = sols[-1] if sols else None
        weather = data.get(latest_sol, {}) if latest_sol else {}

        # Prepare the weather data dictionary
        mars_weather = {
            "sol": latest_sol,
            "temperature": weather.get("AT", {}).get("av", "N/A"),
            "pressure": weather.get("PRE", {}).get("av", "N/A"),
            "wind": weather.get("HWS", {}).get("av", "N/A"),
            "season": weather.get("Season", "N/A"),
        }

    except Exception as e:
        mars_weather = {"error": f"Unable to fetch data: {e}"}

    # 🔥 This line sends data to index.html
    return render_template("index.html", weather=mars_weather)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
