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
import numpy
from pykrx import stock
from datetime import datetime, timedelta


def testMain() :
  rootPath = 'C:\Python_Stocks'
  inputFolderPath = os.path.join(rootPath, 'input')
  outputFolderPath = os.path.join(rootPath, 'output')
  resultFolderPath = os.path.join(rootPath, 'result')
  imgFolderPath = os.path.join(rootPath, 'imgMV')
  masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')
  
  resultFileFolder = "../"
  resultFileName = "dailyConfirmCode.json"
  

def BBand(code, mv, k) :
  dfCode = dataProcessing.GetStockPrice(code, 200)
  dfCode = dataProcessing.standardizationStockSplit(dfCode)
  dfCode = dfCode.iloc[::-1]

  dfCode['이평'] = dfCode['종가'].rolling(window=mv).mean()
  dfCode['std'] = dfCode['종가'].rolling(window=mv).std()
  dfCode['BBand상'] = round((dfCode['이평'] + k * dfCode['std']))
  dfCode['BBand하'] = round((dfCode['이평'] - k * dfCode['std']))

  return dfCode

# retBBand = BBand('005930', 20, 2)
#
# print(retBBand.to_string())
# print(retBBand)
#
#
pd.set_option('display.max_columns', None) # 전체 열 보기
# pd.set_option('display.max_rows', None) # 전체 행 보기
#
# # 종목코드와 종목명 가져오기
# stock_list = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="ALL")})
# stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
# stock_list.head()
#
#
#
# ticker = stock_list.loc[stock_list['종목명']=='삼성SDI', '종목코드']
# print(stock_list.loc[stock_list['종목코드']=='006400', '종목코드'])
# print(ticker)
# df = stock.get_market_ohlcv_by_date(fromdate="20230101", todate="20240515", ticker="002880")
#
# print(df)

# # 칼럼명 영문명으로 변경
# # 시가(Open), 고가(High), 저가(Low), 종가(Close), 거래량(Volume)
# df = df.rename(columns={'시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
#
# # 중심선, 상단밴드, 하단밴드 계산
# df['ma20'] = df['Close'].rolling(window=20).mean() # 20일 이동평균
# df['stddev'] = df['Close'].rolling(window=20).std() # 20일 이동표준편차
# df['upper'] = df['ma20'] + 2*df['stddev'] # 상단밴드
# df['lower'] = df['ma20'] - 2*df['stddev'] # 하단밴드
# df = df[19:]
# print(df)



  # # 결과 lst 생성
  # lstResult = []
  # dfResult = pd.DataFrame(columns=["code"])
  # cnt = 0
  #
  # for idx, row in df.iterrows() :
  #   # 종목 시세 데이터 가져오기
  #   if "K" in row['code'] or "L" in row['code'] :
  #     continue
  #
  #   #____________조건 넣기
  #   if dataProcessing.isDisparity(row['code'], 20, 0.97) :
  #     list_row = [row['code']]
  #     dfResult.loc[len(dfResult)] = list_row
  #     cnt += 1
  #
  #   print("{0} // {1} // {2}".format(len(df), idx, cnt))
  #
  #   #____________위까지 조건 넣기
  #   # dfCode = dataProcessing.GetStockPrice(row['code'], 110)
  #   # dfCode = dataProcessing.standardizationStockSplit(dfCode)
  #
  #   # dfShortMA = dataProcessing.GetMovingAverageRetDF(dfCode, 10)
  #   # dfLongMA = dataProcessing.GetMovingAverageRetDF(dfCode, 100)
  #
  #   # isFlag = dataProcessing.isBetweenTwoMV(dfCode, dfLongMA, dfShortMA, 0)
  #
  #   # print("{0} |||| {1}".format(len(df), idx+1))
  #
  #   # if isFlag :
  #   #   imgFolderPath = os.path.join(rootPath, 'img_Confirm')
  #   #   imgFilePath = os.path.join(imgFolderPath, row['code'])
  #   #   list_row = [row['code']]
  #   #   dfResult.loc[len(dfResult)] = list_row
  #   #   Image.SaveDFImage(row['code'], dfCode, imgFilePath)
  #
  # dfResult.to_json(path_or_buf=os.path.join(resultFileFolder, resultFileName), orient="records")
  # print("전체 : {0}, 대상 : {1}".format(len(df), len(lstResult)))

# testMain()

#
# print(dataProcessing.GetStockPriceByNaver("006400", 100))
#
# df = stock.get_market_ohlcv_by_date(fromdate="20230101", todate="20240515", ticker="006400")
# df['전일비'] = df['종가'] - df['종가'].shift()
# print(df)

print((datetime.now() - timedelta(days=100)).strftime("%Y%m%d"))

dfSellResult = pd.DataFrame(columns=['code', 'buyPrice', 'amount', 'sell'])
dfBuyResult = pd.DataFrame(columns=['code', 'buyPrice', 'amount'])

dfSellResult.loc[len(dfSellResult)] = ["1", "1", "1", "1"]
dfSellResult.loc[len(dfSellResult)] = ["2", "2", "2", "2"]
dfSellResult.loc[len(dfSellResult)] = ["3", "3", "3", "3"]



# 결과 DF 생성
testString = "3";
if testString in dfSellResult['code'].values:
  # 해당 code 가 있으면 업데이트,
  dfSellResult.loc[testString == dfSellResult['code'], ['sell']] = "Y"
  # 없으면 새로 생성
else :
  data = {'code': testString, 'buyPrice': testString, 'amount': testString, 'sell': 'N'}
  dfSellResult = pd.concat([dfSellResult, pd.DataFrame([data])], ignore_index=True)



print(dfSellResult)
