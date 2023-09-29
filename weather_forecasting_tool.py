from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather_forecast(city):
    api_key = "API_KEY" 
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(base_url, params={"q": city, "appid": api_key})
        response.raise_for_status()
        weather_data = response.json()

        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        return {
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
        }

    except requests.exceptions.RequestException as err:
        return {"error": str(err)}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_name = request.form["city_name"]
        weather_data = get_weather_forecast(city_name)
        return render_template("index.html", weather_data=weather_data)

    return render_template("index.html", weather_data=None)

if __name__ == "__main__":
    app.run(debug=True)
