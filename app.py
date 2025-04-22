import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import requests

load_dotenv()  # pull in .env

API_KEY = os.getenv("WEATHERSTACK_API_KEY")
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            resp = requests.get(
                "http://api.weatherstack.com/current",
                params={
                    "access_key": API_KEY,
                    "query": city,
                    "units": "m"   # metric
                }
            )
            if resp.ok:
                data = resp.json()
                if data.get("success", True) is False:
                    error = data.get("error", {}).get("info", "Unknown error")
                else:
                    loc = data["location"]
                    cur = data["current"]
                    weather = {
                        "city": loc["name"],
                        "country": loc["country"],
                        "temp": cur["temperature"],
                        "desc": cur["weather_descriptions"][0],
                        "hum": cur["humidity"],
                        "wind": cur["wind_speed"]
                    }
            else:
                error = f"Request failed: {resp.status_code}"
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
