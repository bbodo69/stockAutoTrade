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

def testMain() :
  rootPath = 'C:\Python_Stocks'
  inputFolderPath = os.path.join(rootPath, 'input')
  outputFolderPath = os.path.join(rootPath, 'output')
  resultFolderPath = os.path.join(rootPath, 'result')
  imgFolderPath = os.path.join(rootPath, 'imgMV')
  masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')
  
  resultFileFolder = "../"
  resultFileName = "dailyConfirmCode.json"
  
  # 코스피 종목 받아오기
  sheetName = 'KOSPI'
  df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)
  
  # 결과 lst 생성
  lstResult = []
  dfResult = pd.DataFrame(columns=["code"])
  
  for idx, row in df.iterrows() :
    # 종목 시세 데이터 가져오기
    if "K" in row['code'] or "L" in row['code'] :
      continue

    #____________조건 넣기
    if dataProcessing.isDisparity(row['code'], 20, 0.97) :
      list_row = [row['code']]
      dfResult.loc[len(dfResult)] = list_row

    #____________위까지 조건 넣기
    # dfCode = dataProcessing.GetStockPrice(row['code'], 110)
    # dfCode = dataProcessing.standardizationStockSplit(dfCode)
  
    # dfShortMA = dataProcessing.GetMovingAverageRetDF(dfCode, 10)
    # dfLongMA = dataProcessing.GetMovingAverageRetDF(dfCode, 100)
    
    # isFlag = dataProcessing.isBetweenTwoMV(dfCode, dfLongMA, dfShortMA, 0)
  
    # print("{0} |||| {1}".format(len(df), idx+1))
    
    # if isFlag :
    #   imgFolderPath = os.path.join(rootPath, 'img_Confirm')
    #   imgFilePath = os.path.join(imgFolderPath, row['code'])
    #   list_row = [row['code']]
    #   dfResult.loc[len(dfResult)] = list_row
    #   Image.SaveDFImage(row['code'], dfCode, imgFilePath)
  
  dfResult.to_json(path_or_buf=os.path.join(resultFileFolder, resultFileName), orient="records")
  print("전체 : {0}, 대상 : {1}".format(len(df), len(lstResult)))

testMain()
