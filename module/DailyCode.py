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

def DailyCode(filePath) :
  rootPath = 'C:\Python_Stocks'
  inputFolderPath = os.path.join(rootPath, 'input')
  masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')
  
  # 코스피 종목 받아오기
  sheetName = 'KOSPI'
  df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)
  
  # 결과 lst 생성
  lstResult = []
  dfResult = pd.DataFrame(columns=["code"])
  cnt = 0
  
  for idx, row in df.iterrows() :
    # 종목 시세 데이터 가져오기
    if "K" in row['code'] or "L" in row['code'] :
      continue

    # ____________조건 넣기
    if dataProcessing.isDisparity(row['code'], 20, 0.97):
      list_row = [row['code']]
      dfResult.loc[len(dfResult)] = list_row
      cnt += 1

    print("{0} // {1} // {2}".format(len(df), idx, cnt))

  dfResult.to_json(path_or_buf=filePath, orient="records")
  print("전체 : {0}, 대상 : {1}".format(len(df), len(lstResult)))

# DailyCode("dailyConfirmCode.json")
