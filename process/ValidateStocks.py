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
import module.sender_collection as sender_collection

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
sampleCnt = 10

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

# df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)  # 코스피 코드 받아오기

# if sampleCnt == 0:
#     sampleCnt = len(df)
#
# dfSample = df.sample(sampleCnt).sort_index()

# print(dfSample)


def sectionsCount():
    dicResult = {}
    keys = ["p75_80", "p70_75", "p65_70", "p60_65", "p55_60", "p50_55", "p45_50", "p40_45", "p35_40", "p30_35",
            "p25_30", "p20_25", "p15_20", "p10_15", "p05_10", "p00_05", "m00_05", "m05_10", "m10_15", "m15_20",
            "m20_25",
            "m25_30", "m30_35", "m35_40", "m40_45", "m45_50", "m50_55", "m55_60", "m60_65", "m65_70", "m70_75",
            "m75_80"]
    for i in keys:
        dicResult[i] = 0

    dfSample = df.sample(sampleCnt).sort_index()
    dfSample.reset_index()

    tmpPrice = 0
    for idx, row in dfSample.iterrows():
        try:
            dfCode = dataProcessing.GetStockPrice(row['code'], 300)
            dfCode = dataProcessing.standardizationStockSplit(dfCode)
            for idx_c, code in dfCode.iterrows():
                if tmpPrice == 0:
                    tmpPrice = code['종가']
                    continue
                else:
                    if 75 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 80:
                        dicResult['p75_80'] += 1
                    elif 70 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 75:
                        dicResult['p70_75'] += 1
                    elif 65 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 70:
                        dicResult['p65_70'] += 1
                    elif 60 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 65:
                        dicResult['p60_65'] += 1
                    elif 55 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 60:
                        dicResult['p55_60'] += 1
                    elif 50 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 55:
                        dicResult['p50_55'] += 1
                    elif 45 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 50:
                        dicResult['p45_50'] += 1
                    elif 40 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 45:
                        dicResult['p40_45'] += 1
                    elif 35 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 40:
                        dicResult['p35_40'] += 1
                    elif 30 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 35:
                        dicResult['p30_35'] += 1
                    elif 25 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 30:
                        dicResult['p25_30'] += 1
                    elif 20 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 25:
                        dicResult['p20_25'] += 1
                    elif 15 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 20:
                        dicResult['p15_20'] += 1
                    elif 10 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 15:
                        dicResult['p10_15'] += 1
                    elif 5 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 10:
                        dicResult['p05_10'] += 1
                    elif 0 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 5:
                        dicResult['p00_05'] += 1
                    elif -5 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < 0:
                        dicResult['m00_05'] += 1
                    elif -10 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -5:
                        dicResult['m05_10'] += 1
                    elif -15 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -10:
                        dicResult['m10_15'] += 1
                    elif -20 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -15:
                        dicResult['m15_20'] += 1
                    elif -25 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -20:
                        dicResult['m20_25'] += 1
                    elif -30 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -25:
                        dicResult['m25_30'] += 1
                    elif -35 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -30:
                        dicResult['m30_35'] += 1
                    elif -40 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -35:
                        dicResult['m35_40'] += 1
                    elif -45 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -40:
                        dicResult['m40_45'] += 1
                    elif -50 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -45:
                        dicResult['m45_50'] += 1
                    elif -55 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -50:
                        dicResult['m50_55'] += 1
                    elif -60 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -55:
                        dicResult['m55_60'] += 1
                    elif -65 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -60:
                        dicResult['m60_65'] += 1
                    elif -70 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -65:
                        dicResult['m65_70'] += 1
                    elif -75 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -70:
                        dicResult['m70_75'] += 1
                    elif -80 <= (tmpPrice - code['종가']) * 1000 / tmpPrice < -75:
                        dicResult['m75_80'] += 1
                tmpPrice = code['종가']
            print("{0} // {1}".format(len(dfSample), idx))
        except Exception as e:
            print(e)
            print(row['code'])

    print(dicResult)
    lists = dicResult.items()  # sorted by key, return a list of tuples
    x, y = zip(*lists)  # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.show()


def saveSortingCode(saveFilePath):
    '''
    KOSPI 종목을 받아와 필터링 후 json 형태로 파일 저장
    :param saveFilePath : json 파일의 저장 위치
    '''
    # 변수 지정
    dfResult = pd.Dataframe(columns=['code'])

    # KOSPI DF 저장
    dfCode = pd.DataFrame()

    # dfKOSPI 에 조건 부합 Code 분류
    for idx, row in dfCode.iterrows():
        # 초기화
        dfCode = dataProcessing.GetStockPrice(row['code'], 30)

        # 배당락, 병합, 분할 표준화
        dfCode = dataProcessing.standardizationStockSplit(dfCode)
        dfShortMA = dataProcessing.GetMovingAverageRetDF(dfCode, 10)
        dfLongMA = dataProcessing.GetMovingAverageRetDF(dfCode, 100)

        # Code 조건 필터링
        isResult = dataProcessing.isBetweenTwoMV(df, dfLongMA, dfShortMA, 0)

        # 조건에 부합할 경우, dfFilteredCode 에 해당 코드 넣기
        if isResult:
            rowData = [row['code']]
            dfResult.loc[len(dfResult)] = rowData

    # dfResult -> json 파일 변환
    os.remove(saveFilePath)
    dfResult.to_json(saveFilePath, orient="records")


def calculResult(MA, buyRate, takeBenefitRate, stopLossRate):
    try:
        dfSample = df.sample(sampleCnt).sort_index()
        cntIdx = 1
        totalCnt = 0
        totalBuyCnt = 0
        totalSellBenefitCnt = 0
        totalSellStopLoss = 0
        totalTime = 0

        # Total df 생성
        dfTotal = pd.DataFrame(columns=['code', '총', '매수', '익절', '손절'])

        totalFilePath = os.path.join(imgFolderPath,
                                     'total_' + str(MA) + '_' + str(buyRate) + '_' + str(takeBenefitRate) + '_' + str(
                                         stopLossRate) + '.xlsx')

        for idx, row in dfSample.iterrows():
            lstDate = []
            # _______________________아래로
            # # 초기화
            dfCode = dataProcessing.GetStockPrice(row['code'], 300)
            # # 배당락, 병합, 분할 표준화
            # dfCode = dataProcessing.standardizationStockSplit(dfCode)
            startTime = time.time()
            # # # 이동평균선 구하기
            # # dfMAtarget = dataProcessing.GetMovingAverageRetDF(dfCode, MA)

            # lstScatterDic = []

            # # dicGetDateFollowingMAPattern = dataProcessing.CrossDateStockPriceAndMV(dfCode, dfMAtarget, 'd')
            # dicGetDateFollowingMAPattern = dataProcessing.dicMAUpCrossPoint(dfCode, MA, 100)

            # for i in dicGetDateFollowingMAPattern:
            #     dicGetDateFollowingMAPattern[i]['color'] = 'red'
            # lstScatterDic.append(dicGetDateFollowingMAPattern)

            # for i in lstScatterDic:
            #     for j in i:
            #         lstDate.append(j)
            dfDis = dataProcessing.DisparityRetDF(row['code'], 300, MA)

            tmp = -1
            print(dfDis)
            for idx2, row2 in dfDis.iterrows():
                if row2['종가'] > 97:
                    tmp = int(row2['종가'])
                    tmp2 = row2['날짜']
                    continue
                if tmp != -1 and int(row2['종가']) < 97:
                    lstDate.append(tmp2)
                    # lstDate.append(row2['날짜'])
                    print(tmp2)
                    print(row2['날짜'])
                    tmp = -1
                    continue
                tmp = -1

            # ______________________ lstDate 에 날짜 형식으로 넣어주기

            dicTmpResult = dataProcessing.calculTrade(df=dfCode, lstDate=lstDate, buyRate=buyRate,
                                                      takeBenefitRate=takeBenefitRate, stopLossRate=stopLossRate,
                                                      adjustDay=1)
            totalCnt += dicTmpResult['총']
            totalBuyCnt += dicTmpResult['매수']
            totalSellBenefitCnt += dicTmpResult['익절']
            totalSellStopLoss += dicTmpResult['손절']

            # 매도, 매수, 익절, 손절 계산 구하기
            print(row['code'])
            print('::: 총 갯수 : {0}, 총 매수 : {1}, 총 익절 : {2}, 총 손절 : {3}'.format(dicTmpResult['총'],
                                                                              dicTmpResult['매수'],
                                                                              dicTmpResult['익절'],
                                                                              dicTmpResult['손절']))
            list_row = [row['code'], dicTmpResult['총'], dicTmpResult['매수'], dicTmpResult['익절'], dicTmpResult['손절']]
            dfTotal.loc[len(dfTotal)] = list_row

            print('{0} / {1} ::: 총 갯수 : {2}, 총 매수 : {3}, 총 익절 : {4}, 총 손절 : {5}'.format(cntIdx,
                                                                                        len(dfSample),
                                                                                        totalCnt,
                                                                                        totalBuyCnt,
                                                                                        totalSellBenefitCnt,
                                                                                        totalSellStopLoss))
            cntIdx += 1

            # 소요시간 출력
            totalTime += time.time() - startTime
            avgTime = round(((totalTime / cntIdx)), 2)
            print("평균 개당 소요 시간 : {0} 초".format(avgTime))

        # Total 정보 입력
        list_row = ['Total', totalCnt, totalBuyCnt, totalSellBenefitCnt, totalSellStopLoss]
        dfTotal.loc[len(dfTotal)] = list_row
        print("totalBuyCnt : {0}, totalBuyCnt : {1}".format(totalBuyCnt, totalBuyCnt))
        list_row = ['비율', totalCnt, round(totalBuyCnt * 100 / totalBuyCnt, 1),
                    round(totalSellBenefitCnt * 100 / totalBuyCnt, 1),
                    round(totalSellStopLoss * 100 / totalBuyCnt, 1)]
        dfTotal.loc[len(dfTotal)] = list_row

        # Total Excel 저장
        excel_collection.saveDFToNewExcel(totalFilePath, 'Total', dfTotal)

        # 라인 보내기
        totalremain = totalBuyCnt - totalSellBenefitCnt - totalSellStopLoss
        benefitPerBuy = round(((totalSellBenefitCnt * (
                takeBenefitRate - 0.005) + totalSellStopLoss * (
                                        stopLossRate - 0.005) + totalremain) - totalBuyCnt) / totalBuyCnt * 100,
                              2)
        messageInfo = '\n조건 : {6}\n총 갯수 : {0}\n총 매수 : {1}\n총 익절 : {2}\n총 손절 : {3}\n총 유지 : {4}\n총매입가의이익률(%) : {5}'.format(
            totalCnt,
            totalBuyCnt,
            totalSellBenefitCnt,
            totalSellStopLoss,
            totalremain,
            benefitPerBuy,
            str(MA) + '_' + str(buyRate) + '_' + str(takeBenefitRate) + '_' + str(stopLossRate))
        Common.SendLine(messageInfo)

    except Exception as e:
        print(e)

    # 컴퓨터 강제종료
    # os.system("shutdown -s -t 300")


def createGraphLineAndScatter(MA):
    '''
    조건 설정
    1. 10 이평선이 'duu' 패턴을 따르는 경우
    '''
    # 폴더 초기화
    imgFolderPath = os.path.join(rootPath, 'img' + '_' + str(MA))
    Common.clearFolder(imgFolderPath)
    dfSample = df.sample(sampleCnt).sort_index()

    totalFilePath = os.path.join(imgFolderPath, 'total.xlsx')

    cntIdx = 1

    totalCnt = 0
    totalBuyCnt = 0
    totalSellBenefitCnt = 0
    totalSellStopLoss = 0

    totalTime = 0

    # Total df 생성
    dfTotal = pd.DataFrame(columns=['code', '총', '매수', '익절', '손절'])

    for idx, row in dfSample.iterrows():
        try:
            # 초기화
            dfCode = dataProcessing.GetStockPrice(row['code'], 250)
            dfDateKey = dfCode.set_index('날짜')

            dicScatterDate = {}
            imgFilePath = os.path.join(imgFolderPath, row['code'])
            MVInfo = []
            dicIfResult = {}
            # 배당락, 병합, 분할 표준화
            dfCode = dataProcessing.standardizationStockSplit(dfCode)
            targetDate = datetime.datetime.now().strftime('%Y.%m.%d')
            dfMA = dataProcessing.GetMovingAverageRetDF(dfCode, MA)

            startTime = time.time()

            '''
            2023-11-10
            dfMA = dfMA.set_index('날짜')
            # 일자별 이평선 상승여부 확인 
            dicMVUpDate = module.dataProcessing.GetDateFollowingMAPattern(dfCode, MA, "u") # 내림차순 정렬
            # 일자별 코드 정보
            for idx, codeRow in dfCode.iterrows():
                if len(dfCode) < idx + 2:
                    break
                # 변수 설정
                date = codeRow['날짜']   
                highPrice = codeRow['고가']
                endPrice = codeRow['종가']
                lowPrice = codeRow['저가']
                if date not in dfMA.index :
                    continue
                dateMA = dfMA.loc[date]['종가']
                
                # 조건 설정1. 이평선이 상승중일 때,
                if date not in dicMVUpDate :
                    continue
                # 조건 설정2. 이평선 아래 위인지 확인
                if len(MVInfo) > 2 :
                    MVInfo.pop(0)
                if int(endPrice) < dateMA :
                    MVInfo.append('d')
                else : 
                    MVInfo.append('u')
                # 조건 부합 되었을 때,
                if ''.join(MVInfo) == 'ddu' :
                    date = module.dataProcessing.addDay(dfCode, date, 2)
                    highPrice = dfDateKey.loc[date]['고가']
                    endPrice = dfDateKey.loc[date]['종가']
                    lowPrice = dfDateKey.loc[date]['저가']

                    dicScatterDate[date] = {}
                    dicScatterDate[date]['가격'] = endPrice
                    dicScatterDate[date]['구분'] = 1
            if len(dicScatterDate) == 0 :
                continue
            '''
            '''
            # 매수, 매도 비율 산출
            for i in dicScatterDate.keys():
                totalCnt += 1
                dicBuySellInfo = module.resultBuySell.GetBuySellResultUseDatePriceExpireDate(dfCode, i, 0.98, 1.01, 30)
                if dicBuySellInfo['구분'] == '1' :
                    totalCnt0 += 1
                    pass
                elif dicBuySellInfo['구분'] == '2' :
                    totalCnt1 += 1
                else : 
                    totalCnt2 += 1
            '''
            # dfMA = dfMA.reset_index(drop=True)
            dfMA = dfMA.reset_index()
            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'],savePath=imgFilePath)
            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'], savePath=imgFilePath)
            # Image.SaveDFImageWithScatter4(df=dfCode, x='날짜', dicScatterData, title=row['code'], savePath=imgFilePath)
            # Image.SaveDFImageWithScatterWithMA(dfCode, dfMA, '날짜', dicScatterDate, "", "", title=row['code'], savePath=imgFilePath)

            ''' 
            그물망 이평선 포함한 이미지 저장
            MAStart = 20
            MAEnd = 80
            MADiff = 10
            Image.SaveDFNetImageWithScatterWithMA(dfCode, MAStart, MAEnd, MADiff, '날짜', dicScatterDate, "", "", title=row['code'], savePath=imgFilePath)
            '''

            # 라인 정보 lst [df, x축 값, y축 값, linestyle, color 저장] ex) [df, '날짜', '가격', 'dashed', 'black']
            dfMA10 = dataProcessing.GetMovingAverageRetDF(dfCode, 10)
            dfMA20 = dataProcessing.GetMovingAverageRetDF(dfCode, 20)
            dfMA30 = dataProcessing.GetMovingAverageRetDF(dfCode, 30)
            dfMA40 = dataProcessing.GetMovingAverageRetDF(dfCode, 40)
            dfMA50 = dataProcessing.GetMovingAverageRetDF(dfCode, 50)
            dfMA60 = dataProcessing.GetMovingAverageRetDF(dfCode, 60)
            dfMA70 = dataProcessing.GetMovingAverageRetDF(dfCode, 70)
            dfMA80 = dataProcessing.GetMovingAverageRetDF(dfCode, 80)
            dfMA90 = dataProcessing.GetMovingAverageRetDF(dfCode, 90)
            dfMA100 = dataProcessing.GetMovingAverageRetDF(dfCode, 100)
            dfMAtarget = dataProcessing.GetMovingAverageRetDF(dfCode, MA)

            lstPlotDF = []
            lstPlotDF.append([dfCode, '날짜', '종가', 'solid', 'black'])
            lstPlotDF.append([dfCode, '날짜', '저가', 'solid', 'blue'])
            lstPlotDF.append([dfCode, '날짜', '고가', 'solid', 'red'])
            lstPlotDF.append([dfMA10, '날짜', '종가', 'dotted', 'green'])
            lstPlotDF.append([dfMA20, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA30, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA40, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA50, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA60, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA70, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA80, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA90, '날짜', '종가', 'dotted', 'gray'])
            lstPlotDF.append([dfMA100, '날짜', '종가', 'dotted', 'orange'])

            # 점 정보 lst 에 :::::: 값으로 2중 dic 저장 ex) {'날짜' : {'가격' : 가격}} <-- 기본
            dicGetDateFollowingMAPattern = {}
            '''
            dicGetDateFollowingMAPattern = dataProcessing.GetDateFollowingMAPattern(dfCode, 10, "duu")

            # 이평선 100이 하강/상승할 때,
            for i in dicGetDateFollowingMAPattern.copy().keys() :
                if dataProcessing.getUpDownMV(dfCode, 100, i) == 0 :
                    continue
                else :
                    del dicGetDateFollowingMAPattern[i]
            '''
            lstScatterDic = []

            dicGetDateFollowingMAPattern = dataProcessing.CrossDateStockPriceAndMV(dfCode, dfMAtarget, 'u')
            for i in dicGetDateFollowingMAPattern:
                dicGetDateFollowingMAPattern[i]['color'] = 'red'
            lstScatterDic.append(dicGetDateFollowingMAPattern)
            '''
            dicGetDateFollowingMAPattern = dataProcessing.CrossDateStockPriceAndMV(dfCode, dfMA10, 'u')
            for i in dicGetDateFollowingMAPattern:
                dicGetDateFollowingMAPattern[i]['color'] = 'red'
            lstScatterDic.append(dicGetDateFollowingMAPattern)

            dicGetDateFollowingMAPattern = dataProcessing.CrossDateStockPriceAndMV(dfCode, dfMA50, 'u')
            for i in dicGetDateFollowingMAPattern:
                dicGetDateFollowingMAPattern[i]['color'] = 'blue'
            lstScatterDic.append(dicGetDateFollowingMAPattern)
            
            dicGetDateFollowingMAPattern = dataProcessing.CrossDateStockPriceAndMV(dfCode, dfMA100, 'u')
            for i in dicGetDateFollowingMAPattern:
                dicGetDateFollowingMAPattern[i]['color'] = 'green'
            lstScatterDic.append(dicGetDateFollowingMAPattern)
            '''

            Image.SaveImage(savePath=imgFilePath, title=row['code'], lstPlotDF=lstPlotDF, lstScatterDic=lstScatterDic)
            # 매수 조건 날짜 리스트 저장
            # lstDate = list(dicScatterDate.keys()) # 매수 조건 날짜 리스트화
            lstDate = []
            for i in lstScatterDic:
                for j in i:
                    lstDate.append(j)

            # 거래 조건 계산

            takeBenefitRate = 1.02
            stopLossRate = 0.95
            buyRate = 0.99

            lstbuyRate = [0.97, 0, 98, 0, 99]
            lstTakeBenefitRate = [1.015, 1.02, 1.025]
            lstStopLossRate = [0.95, 0.93, 0.91]

            dicTmpResult = dataProcessing.calculTrade(df=dfCode, lstDate=lstDate, buyRate=buyRate,
                                                      takeBenefitRate=takeBenefitRate, stopLossRate=stopLossRate,
                                                      adjustDay=1)
            totalCnt += dicTmpResult['총']
            totalBuyCnt += dicTmpResult['매수']
            totalSellBenefitCnt += dicTmpResult['익절']
            totalSellStopLoss += dicTmpResult['손절']

            # 매도, 매수, 익절, 손절 계산 구하기
            print(row['code'])
            print('::: 총 갯수 : {0}, 총 매수 : {1}, 총 익절 : {2}, 총 손절 : {3}'.format(dicTmpResult['총'],
                                                                              dicTmpResult['매수'],
                                                                              dicTmpResult['익절'],
                                                                              dicTmpResult['손절']))
            list_row = [row['code'], dicTmpResult['총'], dicTmpResult['매수'], dicTmpResult['익절'], dicTmpResult['손절']]
            dfTotal.loc[len(dfTotal)] = list_row

            print('{0} / {1} ::: 총 갯수 : {2}, 총 매수 : {3}, 총 익절 : {4}, 총 손절 : {5}'.format(cntIdx,
                                                                                        len(dfSample),
                                                                                        totalCnt,
                                                                                        totalBuyCnt,
                                                                                        totalSellBenefitCnt,
                                                                                        totalSellStopLoss))
            cntIdx += 1

            # 소요시간 출력
            totalTime += time.time() - startTime
            avgTime = round(((totalTime / cntIdx)), 2)
            print("평균 개당 소요 시간 : {0} 초".format(avgTime))
        except Exception as e:
            print(e)

    # Total 정보 입력
    list_row = ['Total', totalCnt, totalBuyCnt, totalSellBenefitCnt, totalSellStopLoss]
    dfTotal.loc[len(dfTotal)] = list_row
    print("totalBuyCnt : {0}, totalBuyCnt : {1}".format(totalBuyCnt, totalBuyCnt))
    list_row = ['비율', totalCnt, round(totalBuyCnt * 100 / totalBuyCnt, 1),
                round(totalSellBenefitCnt * 100 / totalBuyCnt, 1), round(totalSellStopLoss * 100 / totalBuyCnt, 1)]
    dfTotal.loc[len(dfTotal)] = list_row

    # Total Excel 저장
    excel_collection.saveDFToNewExcel(totalFilePath, 'Total', dfTotal)

    # 라인 보내기
    totalremain = totalBuyCnt - totalSellBenefitCnt - totalSellStopLoss
    benefitPerBuy = round(((totalSellBenefitCnt * (
                takeBenefitRate - 0.005) + totalSellStopLoss * stopLossRate + totalremain) - totalBuyCnt) / totalBuyCnt * 100,
                          2)
    messageInfo = '\n총 갯수 : {0}\n총 매수 : {1}\n총 익절 : {2}\n총 손절 : {3}\n총 유지 : {4}\n총매입가의이익률(%) : {5}'.format(totalCnt,
                                                                                                           totalBuyCnt,
                                                                                                           totalSellBenefitCnt,
                                                                                                           totalSellStopLoss,
                                                                                                           totalremain,
                                                                                                           benefitPerBuy)
    Common.SendLine(messageInfo)

    # 컴퓨터 강제종료
    # os.system("shutdown -s -t 300")


def usingMostPrice(day, n, MA):
    # 폴더 초기화
    imgFolderPath = os.path.join(rootPath, 'imgMostPrice' + '_' + str(day) + '_' + str(MA))
    Common.clearFolder(imgFolderPath)

    dfSample = df.sample(50).sort_index()

    cntIdx = 1

    for idx, row in dfSample.iterrows():
        try:
            # if row['code'] != '003570':
            #     continue

            # 초기화
            dfCode = dataProcessing.GetStockPrice(row['code'], 250)
            dicScatterDate = {}
            imgFilePath = os.path.join(imgFolderPath, row['code'])

            # 배당락, 병합, 분할 표준화
            dfCode = dataProcessing.standardizationStockSplit(dfCode)
            targetDate = datetime.datetime.now().strftime('%Y.%m.%d')
            dfMA = dataProcessing.GetMovingAverageRetDF(dfCode, MA)
            dfMA = dfMA.set_index('날짜')

            for idx, codeRow in dfCode.iterrows():
                if len(dfCode) < idx + 2:
                    break
                prePrice = dfCode.loc[idx + 1]['종가']
                date = codeRow['날짜']
                highPrice = codeRow['고가']
                endPrice = codeRow['종가']
                lowPrice = codeRow['저가']

                if date in dfMA.index and int(dfMA.loc[date]) > prePrice and int(dfMA.loc[date]) < highPrice:
                    dicScatterDate[date] = {}
                    dicScatterDate[date]['가격'] = int(dfMA.loc[date])
                    dicScatterDate[date]['구분'] = 1

            '''
            dicMostHighPrice = dataProcessing.GetMostPriceOneSideFromDF(df=dfCode , targetDate=targetDate, day=day, gubun="고가", n=n, continueDay = 2)
            dicMostLowPrice = dataProcessing.GetMostPriceOneSideFromDF(df=dfCode, targetDate=targetDate, day=day, gubun="저가", n=n, continueDay = 2)

            dicMostHighPriceScatter = {}
            dicMostLowPriceScatter = {}
            '''

            # 이평선 상승인 경우
            '''
            if dicMostHighPrice is None or dicMostLowPrice is None:
                continue

            for i in dicMostHighPrice :
                if dataProcessing.getUpDownMV(df=dfCode, day=MA, date=dicMostHighPrice[i]['날짜']) != 0:
                    continue
                dicMostHighPriceScatter[dicMostHighPrice[i]['날짜']] = dicMostHighPrice[i]['가격']

            for i in dicMostLowPrice :
                if dataProcessing.getUpDownMV(df=dfCode, day=MA, date=dicMostLowPrice[i]['날짜']) != 0:
                    continue
                dicMostLowPriceScatter[dicMostLowPrice[i]['날짜']] = dicMostLowPrice[i]['가격']
            '''

            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'],savePath=imgFilePath)
            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'], savePath=imgFilePath)
            # 그래프 이미지 저장
            Image.SaveDFImageWithScatter4(df=dfCode, x='날짜', dicScatterData=dicScatterDate, title=row['code'],
                                          savePath=imgFilePath)

            # 작업 통계 내기
            lstDate = list(dicScatterDate.keys())  # 매수 조건 날짜 리스트화
            dicTmpResult = dataProcessing.calculTrade(df=dfCode, lstDate=lstDate, buyRate=0.99, takeBenefitRate=1.15,
                                                      stopLossRate=0.95, adjustDay=0)

            # print('{0} / {1} ::: totalCnt : {2}, totalCnt0 : {3}, totalCnt1 : {4}, totalCnt2 : {5}'.format(cntIdx, len(dfSample), totalCnt, totalCnt0, totalCnt1, totalCnt2))
            cntIdx += 1
        except Exception as e:
            print(e)


def useMVPattern(mvPattern):
    # 폴더 생성
    imgSaveFolderPath = imgFolderPath + "_" + mvPattern
    if not os.path.exists(imgSaveFolderPath):
        os.makedirs(imgSaveFolderPath)

    # 폴더 초기화
    Common.clearFolder(imgSaveFolderPath)

    iBuyCnt = 0
    iSellCnt = 0
    iSellProfitCnt = 0
    iSellLossCnt = 0
    iNotSellCnt = 0

    for idx, row in df.iterrows():
        # if row['code'] != '003570':
        #     continue
        print(row['code'])

        # 초기화
        dfCode = dataProcessing.GetStockPrice(row['code'], 250)
        dfDateKey = dfCode.set_index('날짜')
        imgFilePath = os.path.join(imgSaveFolderPath, row['code'])

        dicScatterDate = {}

        # 배당락, 병합, 분할 표준화
        dfCode = dataProcessing.standardizationStockSplit(dfCode)

        # 결과 변수 저장
        dic = dataProcessing.GetDateFollowingMAPattern(df=dfCode, day=5, gubun=mvPattern)

        maxPrice = dfCode['종가'].max()
        minPrice = dfCode['종가'].min()

        # 유효 Date Dic 추출

        # 이동평균 따르는 dic 반복
        for i in dic:

            isSell = False

            idxTargetDate = dfDateKey.index.get_loc(i)
            buyPrice = dfCode.loc[idxTargetDate]['시가'] * 0.995
            sellPrice = buyPrice * 1.025
            upDownMV = dataProcessing.getUpDownMV(df=dfCode, day=60, date=i)
            dicMostHigh = dataProcessing.GetMostPriceFromDF(df=dfCode, targetDate=i, day=7, n=2, gubun='고가')
            dicMostLow = dataProcessing.GetMostPriceFromDF(df=dfCode, targetDate=i, day=7, n=2, gubun='저가')

            #### 넘길 조건 추가 영영 ###
            # 비어있으면 넘기기

            if upDownMV != 0:
                continue

            if dicMostHigh is None or dicMostLow is None:
                continue

            # 고가 2개 미만이면 넘기기.
            if len(dicMostHigh) < 2 or len(dicMostLow) < 2:
                continue

            # 최근 고가가 이전 고가보다 가격이 낮으면 넘기기.
            if dicMostHigh[0]['가격'] < dicMostHigh[1]['가격']:
                continue

            if dicMostHigh[0]['날짜'] > dicMostLow[0]['날짜']:
                continue

            #########################

            # 사지 못하는 경우
            if buyPrice < dfCode.loc[idxTargetDate]['저가']:
                continue

            # 밑에는 사는 경우.
            iBuyCnt += 1

            # 위 날짜 데이터 이후 날짜들 확인
            for j in range(0, idxTargetDate + 1):
                tmpIdx = idxTargetDate - j
                if tmpIdx < 0:
                    break

                # 익절
                if sellPrice < dfCode.loc[tmpIdx]['고가']:
                    dicScatterDate[dfCode.loc[idxTargetDate]['날짜']] = {}
                    dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['가격'] = buyPrice
                    dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['구분'] = 1
                    dicScatterDate[dicMostHigh[0]['날짜']] = {}
                    dicScatterDate[dicMostHigh[0]['날짜']]['가격'] = dicMostHigh[0]['가격']
                    dicScatterDate[dicMostHigh[0]['날짜']]['구분'] = 3
                    dicScatterDate[dicMostHigh[1]['날짜']] = {}
                    dicScatterDate[dicMostHigh[1]['날짜']]['가격'] = dicMostHigh[1]['가격']
                    dicScatterDate[dicMostHigh[1]['날짜']]['구분'] = 3
                    dicScatterDate[dicMostLow[0]['날짜']] = {}
                    dicScatterDate[dicMostLow[0]['날짜']]['가격'] = dicMostLow[0]['가격']
                    dicScatterDate[dicMostLow[0]['날짜']]['구분'] = 4
                    dicScatterDate[dicMostLow[1]['날짜']] = {}
                    dicScatterDate[dicMostLow[1]['날짜']]['가격'] = dicMostLow[1]['가격']
                    dicScatterDate[dicMostLow[1]['날짜']]['구분'] = 4
                    Image.SaveDFImageWithScatter2(df=dfCode, savePath=imgFilePath, dicScatterData=dicScatterDate,
                                                  x='날짜', y='종가', title=row['code'])
                    iSellProfitCnt += 1
                    isSell = True

                if isSell:
                    break

            # 팔리지 않은 경우
            if not isSell:
                dicScatterDate[dfCode.loc[idxTargetDate]['날짜']] = {}
                dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['가격'] = buyPrice
                dicScatterDate[dfCode.loc[idxTargetDate]['날짜']]['구분'] = 0
                iNotSellCnt += 1
                # print("날짜 : {0}, 가격 : {1} / 날짜 : {2}, 가격 : {3}".format(dicMostHigh[0]['날짜'], dicMostHigh[0]['가격'], dicMostHigh[1]['날짜'], dicMostHigh[1]['가격']))

                dicScatterDate[dicMostHigh[0]['날짜']] = {}
                dicScatterDate[dicMostHigh[0]['날짜']]['가격'] = dicMostHigh[0]['가격']
                dicScatterDate[dicMostHigh[0]['날짜']]['구분'] = 3
                dicScatterDate[dicMostHigh[1]['날짜']] = {}
                dicScatterDate[dicMostHigh[1]['날짜']]['가격'] = dicMostHigh[1]['가격']
                dicScatterDate[dicMostHigh[1]['날짜']]['구분'] = 3
                dicScatterDate[dicMostLow[0]['날짜']] = {}
                dicScatterDate[dicMostLow[0]['날짜']]['가격'] = dicMostLow[0]['가격']
                dicScatterDate[dicMostLow[0]['날짜']]['구분'] = 4
                dicScatterDate[dicMostLow[1]['날짜']] = {}
                dicScatterDate[dicMostLow[1]['날짜']]['가격'] = dicMostLow[1]['가격']
                dicScatterDate[dicMostLow[1]['날짜']]['구분'] = 4

        if len(dicScatterDate) > 0:
            Image.SaveDFImageWithScatter2(df=dfCode, savePath=imgFilePath, dicScatterData=dicScatterDate, x='날짜',
                                          y='종가', title=row['code'])

        if iBuyCnt == 0 or iSellProfitCnt == 0:
            print("{0}/{1} | {2}, {3}, {4} | {5}".format(idx + 1, len(df), iBuyCnt, iSellProfitCnt, iNotSellCnt, 0))
        else:
            print("{0}/{1} | {2}, {3}, {4} | {5}".format(idx + 1, len(df), iBuyCnt, iSellProfitCnt, iNotSellCnt,
                                                         round(iSellProfitCnt / iBuyCnt, 3)))

    # 결과 엑셀 생성
    excelFileName = imgSaveFolderPath + "/result.xlsx"
    if iBuyCnt == 0 or iSellProfitCnt == 0:
        data = [[iBuyCnt, iSellProfitCnt, iNotSellCnt, 0]]
    else:
        data = [[iBuyCnt, iSellProfitCnt, iNotSellCnt, round(iSellProfitCnt / iBuyCnt, 3)]]
    dfResultExcel = pd.DataFrame(data, columns=['매수', '매도', '매도실패', '매도/매수'])
    # dfResultExcel = dfResultExcel.reset_index(drop=True, inplace=True)
    dfResultExcel.to_excel(excelFileName)


def useMostPattern():
    # 폴더 초기화
    Common.clearFolder(imgFolderPath)

    iBuyCnt = 0
    iSellCnt = 0
    iSellProfitCnt = 0
    iSellLossCnt = 0
    iNotSellCnt = 0

    for idx, row in df.iterrows():

        # 초기화
        dfCode = dataProcessing.GetStockPrice(row['code'], 250)
        dfDateKey = dfCode.set_index('날짜')
        imgFilePath = os.path.join(imgFolderPath, row['code'])

        dicScatterDate = {}

        # 배당락, 병합, 분할 표준화
        dfCode = dataProcessing.standardizationStockSplit(dfCode)

        # 결과 변수 저장
        dicMostLow = dataProcessing.GetMostPriceBeforeAfter(df=dfCode, before=15, after=3, n=5, gubun='저가',
                                                            targetDate='2023.07.17')
        dicMostHigh = dataProcessing.GetMostPriceBeforeAfter(df=dfCode, before=15, after=3, n=5, gubun='저가',
                                                             targetDate='2023.07.17')

        maxPrice = dfCode['종가'].max()
        minPrice = dfCode['종가'].min()

        # 유효 Date Dic 추출

        if dicMostLow is None:
            continue

        for i in dicMostLow:
            dicScatterDate[dicMostLow[i]['날짜']] = {}
            dicScatterDate[dicMostLow[i]['날짜']]['가격'] = dicMostLow[i]['가격']
            dicScatterDate[dicMostLow[i]['날짜']]['구분'] = 0

        # 이미지 저장
        if len(dicScatterDate) > 0:
            Image.SaveDFImageWithScatter2(df=dfCode, savePath=imgFilePath, dicScatterData=dicScatterDate, x='날짜',
                                          y='종가', title=row['code'])


def startdardizationDF():
    imgFolderPath = os.path.join(rootPath, 'startdardizationDF2')
    # 폴더 초기화
    Common.clearFolder(imgFolderPath)
    df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)  # 코스피 코드 받아오기

    for idx, row in df.iterrows():
        # 초기화
        dfCode = dataProcessing.GetStockPrice(row['code'], 350)
        standardizationDF = dataProcessing.standardizaionPriceUseMVRateDFPrice(dfCode, 120)
        imgFilePath = os.path.join(imgFolderPath, row['code'])
        Image.SaveDFImage2DF(df1=dfCode, df2=standardizationDF, code=row['code'], sFilePath=imgFilePath)
        print("{0}/{1}".format(idx + 1, len(df)))


def ValidateGoldenCross(code, dateLength, MVDay1, MVDay2):
    # MVDay1 으로 이동평균 기간 큰것 지정
    if MVDay1 < MVDay2:
        temp = MVDay1
        MVDay1 = MVDay2
        MVDay2 = temp

    imgFolderPath = os.path.join(rootPath, 'startdardizationDF3')
    imgFilePath = os.path.join(imgFolderPath, code)

    df = dataProcessing.GetStockPrice(code, dateLength)

    dicScatter = {}
    dicMV1 = dataProcessing.GetMV(df, MVDay1)
    dicMV2 = dataProcessing.GetMV(df, MVDay2)
    dfDiff = pd.DataFrame(columns=['날짜', '종가'])

    for i in dicMV1:
        endDiffPrice = dicMV2[i] - dicMV1[i]
        dfDiff.loc[len(dfDiff)] = [i, endDiffPrice]

        # 하강 돌파
        if len(dfDiff) - 1 > 0:
            if dfDiff.loc[len(dfDiff) - 2]['종가'] * dfDiff.loc[len(dfDiff) - 1]['종가'] < 0 and \
                    dfDiff.loc[len(dfDiff) - 2]['종가'] < 0:
                dicScatter[i] = {}
                dicScatter[i]['가격'] = dicMV1[i]
                dicScatter[i]['구분'] = 0

        # 상승 돌파
        if len(dfDiff) - 1 > 0:
            if dfDiff.loc[len(dfDiff) - 2]['종가'] * dfDiff.loc[len(dfDiff) - 1]['종가'] < 0 and \
                    dfDiff.loc[len(dfDiff) - 2]['종가'] > 0:
                dicScatter[i] = {}
                dicScatter[i]['가격'] = dicMV1[i]
                dicScatter[i]['구분'] = 1

    Image.SaveDFImageWithScatter2(df=df, savePath=imgFilePath, dicScatterData=dicScatter, title=code, x='날짜', y='종가')

def validPattern(df, profit, loss, gubun) :
    dfPer = pd.DataFrame(columns=['상한', '하한', '손익'])

    tmpIdx = 0
    tmpIdx2 = 0

    try :

        for idx, row in df.iterrows():
            tmpIdx2 += 1
            if tmpIdx2 % 10 == 0:
                tmpIdx += 1

            if not os.path.exists(datetime.datetime.now().strftime('%Y.%m.%d')):
                # 디렉토리 생성
                os.makedirs(datetime.datetime.now().strftime('%Y.%m.%d'))

            totalFilePath = datetime.datetime.now().strftime('%Y.%m.%d') + "/" + gubun + "/excel"+str(tmpIdx)+".xlsx"

            print("{0} / {1}".format(tmpIdx2, len(df)))

            code = row['code']
            dfCode = dataProcessing.GetStockPrice(code, 600)
            # dfCode = dataProcessing.addMV(dfCode, 5)
            # dfCode = dataProcessing.addMV(dfCode, 20)
            # dfCode = dataProcessing.addMV(dfCode, 60)
            # dfCode = dataProcessing.addMVTrend(dfCode, 5)
            # dfCode = dataProcessing.addMVTrend(dfCode, 20)
            # dfCode = dataProcessing.addMVTrend(dfCode, 60)
            # dfCode = dataProcessing.addDisparity(dfCode, 60)
            # dfCode = dataProcessing.addBolengerBand(dfCode, 20, 2)
            # dfCode = dataProcessing.addBBTrend(dfCode, 30, 2)
            # dfCode = dataProcessing.addMACD(dfCode, 26, 12, 9)
            dfCode = dataProcessing.addRSI(dfCode, 14)

            # dfCode['매수판단1'] = dfCode['종가'] - dfCode['하한선20'].shift()
            for idx2, row2 in dfCode.iterrows():

                if(dfCode.index.get_loc(idx2) + 1 >= len(dfCode)):
                    continue
                if(dfCode.index.get_loc(idx2) - 5 < 0):
                    continue
                # next2_date = dfCode.index[dfCode.index.get_loc(idx2) + 2]
                next_date = dfCode.index[dfCode.index.get_loc(idx2) + 1]
                pre_date = dfCode.index[dfCode.index.get_loc(idx2) - 1]
                pre2_date = dfCode.index[dfCode.index.get_loc(idx2) - 2]
                pre3_date = dfCode.index[dfCode.index.get_loc(idx2) - 3]
                pre4_date = dfCode.index[dfCode.index.get_loc(idx2) - 4]
                pre5_date = dfCode.index[dfCode.index.get_loc(idx2) - 5]

                # RSI 검사
                if not (float(dfCode.loc[pre_date]['RSI']) < 30 and float(dfCode.loc[pre2_date]['RSI']) < 30 and float(dfCode.loc[pre3_date]['RSI']) < 30 and float(dfCode.loc[pre4_date]['RSI']) < 30 and float(dfCode.loc[pre5_date]['RSI']) < 30):
                    continue

                # 이격도 조건 검사
                # if not (float(dfCode.loc[pre_date]['이격도60']) < 80):
                #     continue

                # MACD 검사
                # if not (dfCode.loc[pre2_date]['MACD'] < dfCode.loc[pre2_date]['signal'] and dfCode.loc[pre_date]['MACD'] > dfCode.loc[pre_date]['signal']):
                #     continue

                # 이평선 추세 검사
                # if not dfCode.loc[pre_date]['상승추세60']:
                #     continue
                # if not(not dfCode.loc[pre_date]['상승추세60'] and not dfCode.loc[pre_date]['상승추세20'] and dfCode.loc[pre_date]['상승추세5'] and dfCode.loc[pre2_date]['상승추세5'] and dfCode.loc[pre3_date]['상승추세5'] and dfCode.loc[pre4_date]['상승추세5']):
                #     continue
                # if not (dfCode.loc[pre_date]['이평선60'] < dfCode.loc[pre_date]['이평선20'] < dfCode.loc[pre_date]['이평선5']):
                #     continue
                # if not (dfCode.loc[pre2_date]['이평선60'] < dfCode.loc[pre2_date]['이평선20'] < dfCode.loc[pre2_date]['이평선5']):
                #     continue
                # if not (dfCode.loc[pre3_date]['이평선60'] < dfCode.loc[pre3_date]['이평선20'] < dfCode.loc[pre3_date]['이평선5']):
                #     continue

                # 매수가 정하기
                # dfCode.at[idx2, '매수가'] = round(dfCode.loc[idx2]['시가']*0.98, 1)

                buy_price = dfCode.loc[idx2]['시가']

                dfCode.at[idx2, '매수가'] = buy_price
                dfCode.at[idx2, '매수'] = "Y"
                high_price = dfCode.loc[next_date:]['고가'].max()
                low_price = dfCode.loc[next_date:]['저가'].min()

                dfCode.at[idx2, '매수가대비%고'] = round(high_price / buy_price, 3) * 100
                dfCode.at[idx2, '매수가대비%저'] = round(low_price / buy_price, 3) * 100
                # if dfCode.loc[pre_date]['종가'] < buy_price < dfCode.loc[idx2]['고가'] and dfCode.loc[idx2]['시가'] < buy_price:
                #     dfCode.at[idx2, '매수'] = "Y"

                    # high_price = dfCode.loc[next2_date:]['고가'].max()
                    # low_price = dfCode.loc[next2_date:]['저가'].min()

                    # dfCode.at[idx2, '매수가대비%고'] = round(high_price / buy_price, 3) * 100
                    # dfCode.at[idx2, '매수가대비%저'] = round(low_price / buy_price, 3) * 100
                # if(dfCode.loc[idx2]['저가'] < dfCode.loc[pre_date]['하한선20'] and dfCode.loc[idx2]['상승추세20'] and dfCode.loc[idx2]['상승추세60']) :
                # if (dfCode.loc[idx2]['저가'] < dfCode.loc[pre_date]['하한선30'] and dfCode.loc[idx2]['하한선추세30'] and dfCode.loc[idx2]['거래량'] > 0):
                # if dfCode.loc[next_date]['저가'] < dfCode.loc[idx2]['하한선30'] and dfCode.loc[idx2]['하한선추세30'] and dfCode.loc[pre_date]['하한선추세30'] and dfCode.loc[next_date]['거래량'] > 0:
                    # buy_price = dfCode.loc[pre_date]['하한선30']
                    # high_price = dfCode.loc[next_date:]['고가'].max()
                    # low_price = dfCode.loc[next_date:]['저가'].min()
                    #
                    # dfCode.at[idx2, '매수가'] = buy_price
                    # dfCode.at[idx2, '매수이후최고가'] = high_price
                    # dfCode.at[idx2, '매수가대비%고'] = round(high_price / buy_price, 3) * 100
                    # dfCode.at[idx2, '매수이후최저가'] = low_price
                    # dfCode.at[idx2, '매수가대비%저'] = round(low_price / buy_price, 3) * 100
                    # dfCode.at[idx2, '매수'] = "Y"

                    # dfCode.at[idx2, '매수가'] = buy_price
                    # dfCode.at[idx2, '매수이후최고가'] = high_price
                    # dfCode.at[idx2, '매수가대비%고'] = round(high_price / buy_price, 3) * 100
                    # dfCode.at[idx2, '매수이후최저가'] = low_price
                    # dfCode.at[idx2, '매수가대비%저'] = round(low_price / buy_price, 3) * 100
                    # dfCode.at[idx2, '매수'] = "Y"

                    # buy_price = dfCode.loc[idx2]['하한선30']
                    # high_price = dfCode.loc[next2_date:]['고가'].max()
                    # low_price = dfCode.loc[next2_date:]['저가'].min()
                    #
                    # dfCode.at[next_date, '매수가'] = buy_price
                    # dfCode.at[next_date, '매수이후최고가'] = high_price
                    # dfCode.at[next_date, '매수가대비%고'] = round(high_price / buy_price, 3) * 100
                    # dfCode.at[next_date, '매수이후최저가'] = low_price
                    # dfCode.at[next_date, '매수가대비%저'] = round(low_price / buy_price, 3) * 100
                    # dfCode.at[next_date, '매수'] = "Y"

            dfCode = dataProcessing.addInOut(dfCode, profit, loss)

            # for idx3, row3 in dfCode.iterrows():
            #     if '매수' not in dfCode.columns:
            #         break
            #     if '수익' not in dfCode.columns:
            #         break
            #     if (dfCode.index.get_loc(idx3) + 1 >= len(dfCode)):
            #         continue
            #     next_date = dfCode.index[dfCode.index.get_loc(idx3) + 1]
            #     if row3['매수'] == "Y":
            #         dfPer.loc[len(dfPer)] = [row3['매수가대비%고'], row3['매수가대비%저'], dfCode.at[next_date, '수익']]
            excel_collection.saveDFToAppendExcel(totalFilePath.replace(".xlsx", "_" + str(profit) +"_" + str(loss) +".xlsx"), code, dfCode)
            dfPer = dataProcessing.addPer(dfCode, dfPer)

    except Exception as e:
        dfPer.loc[len(dfPer)] = ["Err", "", e]

    tmpFilePath = datetime.datetime.now().strftime('%Y.%m.%d') + "/" + gubun + "/percent.xlsx"
    excel_collection.saveDFToAppendExcel(tmpFilePath.replace(".xlsx", "_" + str(profit) +"_" + str(loss) +".xlsx"), "percent", dfPer)
    # os.system("shutdown /s /t 60")

#########################Main
'''
mvPattern = ['uudd', 'uuddu']

for i in mvPattern:
    useMVPattern(i)
'''
###########################

# for idx, row in df.iterrows():
#     try:
#         startTime = time.time()
#         print(row['code'])
#         ValidateGoldenCross(code=row['code'], dateLength=350, MVDay1=120,MVDay2=60)
#         print("{0} / {1} - success : {2}".format(idx + 1, len(df), round(time.time() - startTime, 2)))
#     except Exception as e

#         print("{0} / {1} - fail : {2}".format(idx+1, len(df), e))
'''
for i in [20, 30, 40, 50, 60]:
    for j in [10, 20, 30, 60]:
        MVAndMostPrice(i, 30, j)
'''
# for i in [10, 50, 100] :
#     createGraphLineAndScatter(i)

lstProfit = [1.053]
lstLoss = [0.503]

# pd.set_option('display.max_columns', None)  # 전체 열 보기



# df = dataProcessing.getStockCodes('KOSPI')
# # df = df.sample(2).sort_index()
#
# for i in lstProfit :
#     for j in lstLoss :
#         bolengerBand(df, i, j, 'KOSPI')
#
# lineMessege = "코스피 검증 완료"
#
# sender_collection.SendLine(lineMessege)

stockGubun = 'KOSPI'
df = dataProcessing.getStockCodes(stockGubun)
# df = df.sample(5).sort_index()

for i in lstProfit:
    for j in lstLoss:
        validPattern(df, i, j, stockGubun)

stockGubun = 'KOSDAQ'
df = dataProcessing.getStockCodes(stockGubun)
# df = df.sample(5).sort_index()

for i in lstProfit:
    for j in lstLoss:
        validPattern(df, i, j, stockGubun)

lineMessege = stockGubun + " 검증 완료"

sender_collection.SendLine(lineMessege)

os.system('shutdown -s -t 60')


# for MA in lstMA :
#     for buyRate in lstbuyRate:
#         for takeBenefitRate in lstTakeBenefitRate :
#             for stopLossRate in lstStopLossRate :
#                 calculResult(MA, buyRate, takeBenefitRate, stopLossRate)

# pd.set_option('display.max_rows', None)
# print(dataProcessing.DisparityRetDF("005930", 200, 20))

# lstCode = []
# for idx, i in df.iterrows() :
#     lstCode.append(str(i['code']))
# print(dataProcessing.CodesAveragePriceInfo(lstCode, 300))
# # 라인 보내기
# Common.SendLine(dataProcessing.CodesAveragePriceInfo(lstCode, 300)['시가'], dataProcessing.CodesAveragePriceInfo(lstCode, 300)['고가'], dataProcessing.CodesAveragePriceInfo(lstCode, 300)['저가'], dataProcessing.CodesAveragePriceInfo(lstCode, 300)['종가'])
