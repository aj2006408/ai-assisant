from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""

    if request.method == "POST":
        user_input = request.form["user_input"].lower()

        if "weather" in user_input:
            response = get_weather("Kochi")
        elif "time" in user_input:
            response = f"🕒 Time now: {datetime.now().strftime('%I:%M %p')}"
        elif "date" in user_input:
            response = f"📅 Today is: {datetime.now().strftime('%A, %d %B %Y')}"
        elif "quote" in user_input or "motivate" in user_input:
            response = get_quote()
        elif "news" in user_input or "headline" in user_input:
            response = get_news()
        else:
            response = "🤖 Sorry, I didn't understand. Try asking about weather, time, date, quote, or news."

    return render_template("index.html", response=response)

def get_weather(city):
    api_key = "66661fe166cfa7f18352ac690d087154"  # Your OpenWeatherMap API Key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=66661fe166cfa7f18352ac690d087154&units=metric"
    try:
        data = requests.get(url).json()
        if data.get("main"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"🌤 Weather in {city.title()}: {temp}°C, {desc.capitalize()}"
        else:
            return "⚠ Couldn't fetch weather info. Check your API key or city name."
    except Exception as e:
        return f"❌ Error: {e}"
def get_quote():
    try:
        url = "http://quotes.toscrape.com/page/1/"
        response = requests.get(url)
        if response.status_code != 200:
            return "⚠ Site returned an error."

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        
        if not quotes:
            return "⚠ No quotes found on the page."

        quote_data = random.choice(quotes)
        text = quote_data.find("span", class_="text").get_text(strip=True)
        author = quote_data.find("small", class_="author").get_text(strip=True)
        
        return f'📝 {text} — {author}'

    except Exception as e:
        return f"⚠ Error: {e}"

def get_news():
    api_key = "e033b65accaa4e2d898cbb82713bab2e"  # 🔑 Replace with your News API key from newsapi.org
    url = f"https://newsapi.org/v2/everything?q=apple&from=2025-06-20&to=2025-06-20&sortBy=popularity&apiKey=e033b65accaa4e2d898cbb82713bab2e"

    try:
        data = requests.get(url).json()
        print(data)
        articles = data.get("articles",[])[:3]  # Top 3 news

        if not articles:
            return "⚠ No news found."

        headlines = "🗞 Top Headlines:\n"
        for i, article in enumerate(articles, 1):
            headlines += f"{i}. {article['title']}\n"

        return headlines
    except Exception as e:
        return f"❌ Error fetching news: {e}"

if __name__ == "__main__":
    app.run(debug=True)