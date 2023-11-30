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

rootPath = 'C:\Python_Stocks'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'imgMV')

dfCode = dataProcessing.GetStockPrice("009320", 250)
# dfCode = dataProcessing.standardizationStockSplit(dfCode)
#
# date = module.dataProcessing.addDay(dfCode, '2023.10.17', -10)
#
# print(date)

# 3, 102 를 5 단위로 끊어 리스트 담기

# for i in range(3, 102) :
#     if i % 5 == 0 :
#         print(i)

# print(dataProcessing.dicMAUpCrossPoint(dfCode, 10, 60))
# module.Image.TestSaveImage(imgFolderPath, "009320", dfCode, {'2023.11.01':1425})

saveFilePath = "masterTest.json"


rootPath = 'C:\Python_Stocks'
inputFolderPath = os.path.join(rootPath, 'input')
outputFolderPath = os.path.join(rootPath, 'output')
resultFolderPath = os.path.join(rootPath, 'result')
imgFolderPath = os.path.join(rootPath, 'imgMV')

masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')
sheetName = 'KOSPI'
resultFilePath = os.path.join(resultFolderPath, 'result.xlsx')

# dfTotal = pd.DataFrame(columns=['종목코드', 'totalCnt', 'totalCnt0', 'totalCnt1', 'totalCnt2', 'period', 'avgPeriod'])

cntIdx = 0
avgSellPriod = 0
totalSellPeriod = 0

totalCnt = 0
totalBuyCnt = 0
totalSellBenefitCnt = 0
totalSellStopLoss = 0
sampleCnt = 300

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)  # 코스피 코드 받아오기

os.remove(saveFilePath)

df.to_json(saveFilePath, orient="records")
