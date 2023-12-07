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
masterFilePath = os.path.join(inputFolderPath, 'Master.xlsx')

# 코스피 종목 받아오기
sheetName = 'KOSPI'
df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)

for idx, row in df.itertools() :
  print(row)
