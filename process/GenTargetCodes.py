import math
import os
import module.Common as Common
import module.dataProcessing
import module.excel_collection as excel_collection
import module.dataProcessing as dataProcessing
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
        return {"code":code, "매수가":df.iloc[-1]["하한선"+str(MV)]}
    else:
        pass

dfCodes = pd.DataFrame(columns=['code', 'buyPrice'])

df = dataProcessing.getStockCodes('KOSPI')
for idx, row in df.iterrows():
    try :
        print("{0} / {1}".format(idx, len(df)))
        result = BBandCheck(row['code'], 30, 2)
        if result:
            dfCodes.loc[len(dfCodes)] = [result['code'], round(result['매수가'], 0)]
    except Exception as e :
        dfCodes.loc[len(dfCodes)] = [result['code'], e]


# totalFilePath = "buyCode_"+datetime.now().strftime('%Y%m%d')+".xlsx"
# excel_collection.saveDFToAppendExcel(totalFilePath, "codes", dfCodes)

# totalJsonFilePath = "buyCode_"+datetime.now().strftime('%Y%m%d')+".json"
# excel_collection.saveDFToJson(totalJsonFilePath, dfCodes)

todayJsonFilePath = "buyCode.json"
excel_collection.saveDFToJson(todayJsonFilePath, dfCodes)