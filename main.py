import requests
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client
STOCK_NAME = "FB"
COMPANY_NAME = "Meta Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY ="Your API KEY"

account_sid = "Your Account SID"
auth_token = "Your Auth Token"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stocks_parameters ={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey": API_KEY
}
response = requests.get(STOCK_ENDPOINT,params=stocks_parameters)
response.raise_for_status()
stocks_data = response.json()["Time Series (Daily)"]
stocks_daily = [value for (key,value) in stocks_data.items()]
yesterday_data = stocks_daily[0]
yesterday_closing_price = yesterday_data["4. close"]


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stocks_daily = [value for (key,value) in stocks_data.items()]
yesterday_data = stocks_daily[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
day_before_yesterday_data = stocks_daily[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price)- float(day_before_yesterday_closing_price))
up_down =None
if difference > 0:
    up_down ="🔺"
up_down ="🔻"

percentage = round((difference/float(yesterday_closing_price))*100)
print(percentage)

if percentage > 1:
    news_url = "https://newsapi.org/v2/everything"
    news_api_key = "798021dd939d45a38cb28ab7ec68ca84"
    news_params = {
        "qinTitle": COMPANY_NAME,
        "apiKey": news_api_key
    }
    response_news = requests.get(news_url, params=news_params)
    news_data = response_news.json()["articles"]
    three_articles = news_data[:3]
    formatted_articles = [
        f"{STOCK_NAME}:{up_down}{percentage}%\nHeadline:{article['title']}. \nBrief: {article['description']}" for
        article in three_articles]

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    proxy_client = TwilioHttpClient()
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_="Your Twiilio Number",
            to="Your Verified Phone Number"
        )





