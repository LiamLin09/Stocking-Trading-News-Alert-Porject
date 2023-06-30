import requests
from twilio.rest import Client

STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = '3X5M06T0XJIN0HQX'
NEWS_API_KEY = '837d5e2250fb41f8921149c13656df70'

Twilio_SID = 'AC29c3423a7770608e14019866c0258507'
Twilio_auth_token = 'f982f3cbc363f07630079f4a742af5a9'
Twilio_phone_number = '+18889819531'
MY_PHONE_NUMBER = '+1XXXXXXXXXX'

stock_params = {
    'function': 'TIME_SERIES_WEEKLY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Weekly Time Series']
data_list = [value for (key, value) in data.items()]
lastweek_data = data_list[0]
lastweek_closing_price = lastweek_data['4. close']
print(lastweek_closing_price)

week_before_lastweek_data = data_list[1]
week_before_lastweek_closing_price = week_before_lastweek_data['4. close']
print(week_before_lastweek_closing_price)

difference = float(lastweek_closing_price) - float(week_before_lastweek_closing_price)
up_down = None
if difference > 0:
    up_down = '⬆️'
else:
    up_down = '👇'

diff_percent = (difference / float(lastweek_closing_price)) * 100
print(diff_percent)

if abs(diff_percent) > 1:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'q': COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    client = Client(Twilio_SID, Twilio_auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=Twilio_phone_number,
            to=MY_PHONE_NUMBER
        )
