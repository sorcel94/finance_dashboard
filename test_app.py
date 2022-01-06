import time
import json
from flask import Flask, jsonify, render_template, render_template_string, flash
import csv
from flask.templating import Environment
import pandas as pd
from flask_assets import Environment, Bundle
from turbo_flask import Turbo
import datetime
import threading

app = Flask(__name__)
turbo = Turbo(app)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('styles.scss', filters = 'pyscss', output = 'all.css')
assets.register('scss_all', scss)

@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def getOrders():

    file_path='./static/message.csv'
    with open (file_path) as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)

        price = [x[0] for x in reader]
        avg_price = [round(float(x[1]),2) for x in reader]
        cum_qty = [x[2] for x in reader]
        symbol = [x[3] for x in reader]
        ord_qty = [x[4] for x in reader]
        currency = [x[5] for x in reader]
        last_qty = [x[6] for x in reader]
        last_px = [x[6] for x in reader]
        date = [x[-1] for x in reader]
        side = [x[-2] for x in reader]

        table = {'price': price,
                'avg_price': avg_price,
                'cum_qty': cum_qty,
                'symbol': symbol,
                'ord_qty':ord_qty,
                'currency':currency,
                'last_qty':last_qty,
                'last_px':last_px,
                'date':date,
                'side':side}

    return table

@app.context_processor
def Donught_charts():

    file_path='./static/message.csv'
    with open (file_path) as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)

        symbol = [x[3] for x in reader]
        ord_qty = [float(x[4]) for x in reader]
        date = [x[-1] for x in reader]
        side = [x[-2] for x in reader]

        date = [pd.to_datetime(x) for x in date]
        df = pd.DataFrame(list(zip(date,side,symbol,ord_qty)), columns=['date', 'side', 'pair', 'quantity'])

        today = datetime.date.today()
        today = str(today)

        df_sub = df[df['date'] == today]
        tot_qty = sum(df_sub['quantity'])

        buy = df_sub[df_sub['side']== 'Buy']
        buy_qty = sum(list(buy['quantity']))

        sell = df_sub[df_sub['side']== 'Sell']
        sell_qty = sum(list(sell['quantity']))

        sell_ratio = (sell_qty/tot_qty)*100
        buy_ratio = (buy_qty/tot_qty)*100

        pair = list(df_sub['pair'])

        return {'buy_ratio': buy_ratio, 'sell_ratio':sell_ratio, 'pair':pair}

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            turbo.stream([
                turbo.push(turbo.update(render_template('table.html'), 'table'))
                #turbo.push(turbo.update('base.html', 'code'))
            ])

app.run(debug = True)