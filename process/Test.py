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

for i in range(3, 5) :
    print(i)

dicTest = {}
dicTest[1] = {}
dicTest[1]['color'] = 'green'
dicTest[1]['가격'] = 2222
print(dicTest)
print(dicTest[1].keys())

if 'color' in dicTest[1].keys() :
    print(1)