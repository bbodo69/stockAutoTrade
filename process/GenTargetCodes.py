import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import module.Common as Common
import module.dataProcessing
import module.excel_collection as excel_collection
import module.dataProcessing as dataProcessing
import module.sender_collection as sender_collection

import module.resultBuySell as resultBuySell
import module.Sort_DF as Sort_Df
import module.Image as Image
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import warnings
from datetime import datetime, timedelta
import exchange_calendars as ecals
import requests
import operator
from bs4 import BeautifulSoup
import re
from pykrx import stock

def BBandCheck(code, MV, cons):
    df = dataProcessing.GetStockPrice(code, 60)
    df = dataProcessing.addBBTrend(df, MV, cons)
    if df.iloc[-1]["하한선추세"+str(MV)]:
        # print("{0} / {1} / {2}".format(df.iloc[-2]["하한선"+str(MV)], df.iloc[-1]["하한선"+str(MV)], code))
        return {"code":code, "매수가":df.iloc[-1]["하한선"+str(MV)], "하한선추세":df.iloc[-1]["하한선추세"+str(MV)]}
    else:
        pass

def RSICheck(code, period):
    df = dataProcessing.GetStockPrice(code, 60)
    df = dataProcessing.addRSI(df, 14)
    if df.iloc[-1]["RSI"] < 30 and df.iloc[-2]["RSI"] < 30 and df.iloc[-3]["RSI"] < 30 and df.iloc[-4]["RSI"] < 30 and df.iloc[-5]["RSI"] < 30:
        # print("{0} / {1} / {2}".format(df.iloc[-2]["하한선"+str(MV)], df.iloc[-1]["하한선"+str(MV)], code))
        return {"code":code}
    else:
        pass


dfCodes = pd.DataFrame(columns=['code'])

df = dataProcessing.getStockCodes('KOSPI')
for idx, row in df.iterrows():
    try :
        print("{0} / {1}".format(idx, len(df)))
        result = RSICheck(row['code'], 14)
        if result:
            dfCodes.loc[len(dfCodes)] = [result['code']]
    except Exception as e :
        dfCodes.loc[len(dfCodes)] = [result['code'], e]


# totalFilePath = "buyCode_"+datetime.now().strftime('%Y%m%d')+".xlsx"
# excel_collection.saveDFToAppendExcel(totalFilePath, "codes", dfCodes)

# totalJsonFilePath = "buyCode_"+datetime.now().strftime('%Y%m%d')+".json"
# excel_collection.saveDFToJson(totalJsonFilePath, dfCodes)

# 라인 메세지 전송
nowDate = datetime.now().strftime('%Y.%m.%d')
lineMessege = nowDate + "\n종목갯수\n" + " : " + str(len(dfCodes))
sender_collection.SendLine(lineMessege)

todayJsonFilePath = "buyCode.json"
excel_collection.saveDFToJson(todayJsonFilePath, dfCodes)

# os.system('shutdown -s -t 600')