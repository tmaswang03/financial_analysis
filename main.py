import yfinance as yf, pandas as pd, shutil, os, time, glob, smtplib, ssl
from get_all_tickers import get_tickers as gt

ticks = []

x = int(input("Enter Number of Ticks: "))
for i in range (x):
    tmpTick = str(input("Enter tick number " + str(i) + ": ")) 
    ticks.append(tmpTick)

shutil.rmtree("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Daily_Stock_Report\\Stocks\\")
os.mkdir("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Daily_Stock_Report\\Stocks\\")

calls, fails, notImported, iterator, i = 0, 0, 0, 0, 0

while(i < len(ticks) and (calls < 1800)):
    try: 
        stock = ticks[i]
        temp = yf.Ticker(str(stock))
        Hist_data = temp.history(period="max")
        Hist_data.to_csv("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Daily_Stock_Report\\Stocks\\"+stock+".csv")
        calls += 1
        fails = 0
        i+=1
        time.sleep(2)
    except ValueError: 
        fails += 1
        calls += 1
        if fails > 5: 
            i += 1
            notImported += 1


print(i - notImported)

files = glob.glob("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Daily_Stock_Report\\Stocks\\*.csv")

res = []

while iterator < len(files): 
    OBV_val = 0
    tmpData = pd.read_csv(files[iterator]).tail(10)
    pos_vals, neg_vals = [], []
    for cnt in range(10):
        if tmpData.iloc[cnt, 1] < tmpData.iloc[cnt, 4]: #this means closing > opening, pos obv
            pos_vals.append(cnt)
        else:
             neg_vals.append(cnt)
    for cnt in pos_vals: #calculate on balance volume: 
        OBV_val = round(OBV_val + 100*(tmpData.iloc[cnt, 5] / tmpData.iloc[cnt, 1]))
    for cnt in neg_vals: 
        OBV_val = round(OBV_val - 100*(tmpData.iloc[cnt, 5] / tmpData.iloc[cnt, 1]))
    name = ((os.path.basename(files[iterator])).split(".csv")[0])
    res.append([name, OBV_val])
    iterator += 1

dataFrame = pd.DataFrame(res, columns = ["Company", "OBV_Value"])
dataFrame["Stocks_Ranked"] = dataFrame["OBV_Value"].rank(ascending = False)
dataFrame.sort_values("OBV_Value", inplace = True, ascending = False)
dataFrame.to_csv("C:\\Users\\thoma\\OneDrive\\Documents\\GitHub\\financial_analysis\\Daily_Stock_Report\\OBV_Ranked.csv", index = False)


