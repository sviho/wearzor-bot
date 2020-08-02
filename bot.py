import requests
import random
import telebot


bot = telebot.TeleBot('111111:your_telegram_bot_token')
API_KEY = 'your_api_key_to_openweatherdata'


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "🤖 Hi, I am Wearzor Bot! Here, you can get advice on what to wear before you go "
                                      "outside. Never get too cold or too hot! Type in your city name to start.")


@bot.message_handler(func=lambda message: True)
def handle_city(message):
    weather_answer, advice_answer = fetch_by_name(message.text)
    bot.send_message(message.chat.id, weather_answer)
    bot.send_message(message.chat.id, advice_answer)


def fetch_by_name(city_name):
    url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + API_KEY
    data = requests.request('GET', url)

    if not data:
        return "🤷 Sorry, I couldn't find the weather data for " + city_name + ".", \
               "👉 Please, make sure you don't have any typos and try again."

    return prepare_data_for_answers(data.json())


def prepare_data_for_answers(weather):
    celsius = int(weather['main']['temp'] - 273.15)
    fahrenheit = (celsius * 9 / 5) + 32

    temp_answer = "⭐️ " + str(celsius) + " ºC  | " + str(fahrenheit) + " ºF in " + weather['name']
    generator = AdviceGenerator()
    advice_answer = generator.generate_advice(fahrenheit)

    return temp_answer, advice_answer


class AdviceGenerator:

    temp1 = ["🥶 Hey it's freezing. You definitely need a winter jacket!",
             "🥶 Sooo cold!! Don't forget your winter jacket!",
             "🥶 Do wear a winter jacket and stay warm!"]

    temp2 = ["🧥 It's pretty cold, you'd rather wear a coat.",
             "🧥 Hey, get a coat!",
             "🧥 You need a coat outside!"]

    temp3 = ["😏 Wear a fleece, and you'll be fine!",
             "😏 It's cool, so you should get a fleece.",
             "😏 Don't forget a fleece, you will need it."]

    temp4 = ["🥰 It's nice outside, but you still need a jeans jacket.",
             "🥰 It's good, but you want your light jeans jacket!",
             "🥰 Get a jeans jacket, and it will be perfect."]

    temp5 = ["😎 It is warm! You'll be fine in your favorite t-shirt.",
             "😎 Warm! Get one of your tees.",
             "😎 It's mild outside, just wear a t-shirt."]

    temp6 = ["🥵 It's hot outside! Time for your favorite shorts and a lightweight t-shirt.",
             "🥵 Wear those summer shorts today, and stay cool!",
             "🥵 Hot!! You need your shorts today."]

    def generate_advice(self, temp):
        random_index = random.randint(0, 2)
        if temp <= 35:
            return self.temp1[random_index]
        elif temp <= 47:
            return self.temp2[random_index]
        elif temp <= 59:
            return self.temp3[random_index]
        elif temp <= 67:
            return self.temp4[random_index]
        elif temp <= 80:
            return self.temp5[random_index]
        else:
            return self.temp6[random_index]


if __name__ == '__main__':
    bot.polling(none_stop=True)
