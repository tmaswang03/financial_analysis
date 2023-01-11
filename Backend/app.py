from flask import *
from flask_cors import CORS
import json, time
import yfinance as yf, pandas as pd, shutil, os, time, glob, smtplib, ssl
import kaleido
import plotly
import plotly.graph_objs as go

shutil.rmtree("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Backend\\Daily_Stock_Report\\Stocks\\")
os.mkdir("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Backend\\Daily_Stock_Report\\Stocks\\")

app = Flask(__name__)
CORS(app)

@app.route('/stock/', methods = ['GET'])
def request_page(): 
    stock = str(request.args.get('tick')) 
    completed, count, days = 0, 0, 10
    while(completed == 0 and count <= 5):  
        try: 
            tmp = yf.Ticker(stock)
            hist_data = tmp.history(period="max")
            hist_data.to_csv("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Backend\\Daily_Stock_Report\\Stocks\\"+stock+".csv")
            completed = 1
        except: 
            count += 1
    if(completed == 0): 
        return "Invalid input", 400
    file = "C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Backend\\Daily_Stock_Report\\Stocks\\"+stock+".csv"
    OBV_val = 0
    tmpData = pd.read_csv(file)
    pos_vals, neg_vals = [], [] 
    for cnt in range(days): 
        if tmpData.iloc[cnt, 1] < tmpData.iloc[cnt, 4]: #this means closing > opening, pos obv
            pos_vals.append(cnt)
        else:
             neg_vals.append(cnt)
    for cnt in pos_vals: 
        OBV_val = round(OBV_val + 100*(tmpData.iloc[cnt, 5] / tmpData.iloc[cnt, 1]))
    for cnt in neg_vals: 
        OBV_val = round(OBV_val - 100*(tmpData.iloc[cnt, 5] / tmpData.iloc[cnt, 1]))
    data = yf.download(tickers = stock, period = '10d', interval = '1h', rounding = True)
    fig = go.Figure()
    fig.add_trace(go.Candlestick())
    fig.add_trace(go.Candlestick(x = data.index, open = data['Open'], high=data['High'], low = data['Low'], close = data['Close'], name = 'market data'))
    fig.update_layout(title = str(stock) + ' Share Price', yaxis_title = 'Stock Price USD')
    graphJSON = plotly.io.to_json(fig, pretty = True)
    # return graphJSON
    return jsonify(OBV = OBV_val, graph = graphJSON)

if __name__ == "__main__": 
    app.run(debug = True)

