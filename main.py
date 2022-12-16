from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import sys
import time
from datetime import datetime

try:
    print('MENU: \n\t1.BTC\n\t2.ETH\n\t3.BNB\n\t4.USDT\n\t5.ADA\n')
    y = int(input('Enter your choice: '))
    if y > 5 or y < 1:
        print('Invalid choice!\nEnter valid choice')
        exit()
except ValueError as e:
    print('Invalid choice!\nEnter valid choice')
    exit()


def bitcoin_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start': '1',
        'limit': y,
        'convert': 'INR',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'eaf347ad-5adb-400f-8a23-89f5998c984c',
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)  # storing json response in variable

        for item in data['data']:
            price = item['quote']['INR']['price']
            name = item['name']
            price2 = int(price)

        name2 = name
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return (price2, name2)


def final():
    max_limit = int(input('Enter the price for notification: '))
    print(
        'You will recieve a notification when the crypto crosses the entered price!'
    )
    bitcoin_history = []
    i = 1
    rows = []
    while True:

        price, name = bitcoin_price()

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y,%H:%M:%S")
        date = str(date_time)
        price2 = int(price)
        bitcoin_history.append({
            'value1': date,
            'value2': price2,
            'value3': name
        })

        if price2 > max_limit:
            price_data = {'value1': price2, 'value2': name}
            ifttt_webhook_url = 'https://maker.ifttt.com/trigger/Bitcoin price emergency!/with/key/iAnyBdh8M7bPk4K4wIsSNAy4ea_e6VWms0pmLIcu4h0'  #ifttt url for emergency price notification
            requests.post(ifttt_webhook_url, price_data)
        # i+=1
        time.sleep(60)
        # rows=[]
        if len(bitcoin_history) == 1:
            for i in bitcoin_history:
                date = i['value1']
                price = i['value2']
                row = '{}: ₹<b>{}</b><br>'.format(
                    date,
                    price,
                )
                rows.append(row)
                data = {
                    'value1': ''.join(rows),
                }
            ifttt_webhook_url = 'https://maker.ifttt.com/trigger/Latest Price/with/key/iAnyBdh8M7bPk4K4wIsSNAy4ea_e6VWms0pmLIcu4h0'
            requests.post(
                ifttt_webhook_url,
                json=data)  #passing the formatted value in json format
            bitcoin_history = []


final()

