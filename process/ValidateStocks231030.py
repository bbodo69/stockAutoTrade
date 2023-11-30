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
sheetName = 'KOSPI'
resultFilePath = os.path.join(resultFolderPath, 'result.xlsx')

dfTotal = pd.DataFrame(columns=['종목코드', 'totalCnt', 'totalCnt0', 'totalCnt1', 'totalCnt2', 'period', 'avgPeriod'])

avgSellPriod = 0
totalSellPeriod = 0
totalCnt = 0
totalCnt0 = 0
totalCnt1 = 0
totalCnt2 = 0

# 이동평균 증감 패턴에 따른 과거 데이터 매도 매수 파악

df = excel_collection.readExcelToDataFrame(masterFilePath, sheetName)  # 코스피 코드 받아오기

def MVAndMostPrice(day, MA):
    '''
    1. 이평선 상승
    2. 금일, 전일 주가가 이평선 아래
    '''

    # 폴더 초기화
    imgFolderPath = os.path.join(rootPath, 'imgMostPrice'+'_'+str(day)+'_'+str(MA))
    Common.clearFolder(imgFolderPath)
    dfSample = df.sample(50).sort_index()
    cntIdx = 1

    for idx, row in dfSample.iterrows():
        try:
            # 초기화
            dfCode = dataProcessing.GetStockPrice(row['code'], 250)
            dicScatterDate = {}
            imgFilePath = os.path.join(imgFolderPath, row['code'])

            # 배당락, 병합, 분할 표준화
            dfCode = dataProcessing.standardizationStockSplit(dfCode)
            targetDate = datetime.datetime.now().strftime('%Y.%m.%d')
            dfMA = dataProcessing.GetMovingAverageRetDF(dfCode, MA)
            dfMA = dfMA.set_index('날짜')

            # dfMA 날짜가 키값
            '''
            for dicMVUpDate 돌린다
            item 값이 날짜로 나타난다.
            
            1. item 의 종가 값이 이평선 아래 인지.
            2. item + 1 종가 값도 이평선 아래 인지
            '''

            # 일자별 코드 정보
            for idx, codeRow in dfCode.iterrows():
                if len(dfCode) < idx + 2:
                    break

                # 일자별 이평선 상승여부 확인
                dicMVUpDate = module.dataProcessing.GetDateFollowingMAPattern(dfCode, day, "u") # 내림차순 정렬

                print(dicMVUpDate)

                time.sleep(1000)

                # for date in dicMVUpDate:

                # 컬럼 값으로 DF index 가져오기
                # print(dfCode.날짜[dfCode.날짜 == '2023.10.17'].index.tolist())


                prePrice = dfCode.loc[idx + 1]['종가']
                date = codeRow['날짜']
                highPrice = codeRow['고가']
                endPrice = codeRow['종가']
                lowPrice = codeRow['저가']

                if date in dfMA.index and int(dfMA.loc[date]) > prePrice and int(dfMA.loc[date]) < highPrice:
                    dicScatterDate[date] = {}
                    dicScatterDate[date]['가격'] = int(dfMA.loc[date])
                    dicScatterDate[date]['구분'] = 1

            # 주가가 이평선 돌파

            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'],savePath=imgFilePath)
            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'], savePath=imgFilePath)

            Image.SaveDFImageWithScatter4(df=dfCode, x='날짜', dicScatterData=dicScatterDate, title=row['code'],
                                          savePath=imgFilePath)

            print('{0} / {1} ::: totalCnt : {2}, totalCnt0 : {3}, totalCnt1 : {4}, totalCnt2 : {5}'.format(cntIdx,
                                                                                                           len(dfSample),
                                                                                                           totalCnt,
                                                                                                           totalCnt0,
                                                                                                           totalCnt1,
                                                                                                           totalCnt2))
            cntIdx += 1
        except Exception as e:
            print(e)

def usingMostPrice(day,n, MA):

    # 폴더 초기화
    imgFolderPath = os.path.join(rootPath, 'imgMostPrice'+'_'+str(day)+'_'+str(MA))
    Common.clearFolder(imgFolderPath)

    dfSample = df.sample(50).sort_index()

    cntIdx = 1

    for idx, row in dfSample.iterrows():
        try:
            # if row['code'] != '003570':
            #     continue

            # 초기화
            dfCode = dataProcessing.GetStockPrice(row['code'],250)
            dicScatterDate = {}
            imgFilePath = os.path.join(imgFolderPath, row['code'])

            # 배당락, 병합, 분할 표준화
            dfCode = dataProcessing.standardizationStockSplit(dfCode)
            targetDate = datetime.datetime.now().strftime('%Y.%m.%d')
            dfMA = dataProcessing.GetMovingAverageRetDF(dfCode, MA)
            dfMA = dfMA.set_index('날짜')

            for idx, codeRow in dfCode.iterrows():
                if len(dfCode) < idx + 2 :
                    break
                prePrice = dfCode.loc[idx+1]['종가']
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

            # 주가가 이평선 돌파

            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'],savePath=imgFilePath)
            # Image.SaveDFImageWithScatterWithMAWithAddDate(df=dfCode, dfMA=dfMA, x='날짜', dicScatterData=dicScatterDate, dicTotalHighPrice=dicMostHighPriceScatter, dicTotalLowPrice=dicMostLowPriceScatter, title=row['code'], savePath=imgFilePath)

            Image.SaveDFImageWithScatter4(df=dfCode, x='날짜', dicScatterData=dicScatterDate, title=row['code'],savePath=imgFilePath)

            print('{0} / {1} ::: totalCnt : {2}, totalCnt0 : {3}, totalCnt1 : {4}, totalCnt2 : {5}'.format(cntIdx, len(dfSample), totalCnt, totalCnt0, totalCnt1, totalCnt2))
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
            if dicMostHigh[0]['가격'] < dicMostHigh[1]['가격'] :
                continue

            if dicMostHigh[0]['날짜'] > dicMostLow[0]['날짜'] :
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
                if tmpIdx < 0 :
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

        if len(dicScatterDate) > 0 :
            Image.SaveDFImageWithScatter2(df=dfCode, savePath=imgFilePath, dicScatterData=dicScatterDate, x='날짜', y='종가', title=row['code'])

        if iBuyCnt == 0 or iSellProfitCnt == 0:
            print("{0}/{1} | {2}, {3}, {4} | {5}".format(idx + 1, len(df), iBuyCnt, iSellProfitCnt, iNotSellCnt, 0))
        else:
            print("{0}/{1} | {2}, {3}, {4} | {5}".format(idx + 1, len(df), iBuyCnt, iSellProfitCnt, iNotSellCnt, round(iSellProfitCnt/iBuyCnt , 3)))

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
        if len(dicScatterDate) > 0 :
            Image.SaveDFImageWithScatter2(df=dfCode, savePath=imgFilePath, dicScatterData=dicScatterDate, x='날짜', y='종가', title=row['code'])

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
            if dfDiff.loc[len(dfDiff) - 2]['종가'] * dfDiff.loc[len(dfDiff)-1]['종가'] < 0 and dfDiff.loc[len(dfDiff) - 2]['종가'] < 0:
                dicScatter[i] = {}
                dicScatter[i]['가격'] = dicMV1[i]
                dicScatter[i]['구분'] = 0
        
        # 상승 돌파
        if len(dfDiff) - 1 > 0:
            if dfDiff.loc[len(dfDiff) - 2]['종가'] * dfDiff.loc[len(dfDiff)-1]['종가'] < 0 and dfDiff.loc[len(dfDiff) - 2]['종가'] > 0:
                dicScatter[i] = {}
                dicScatter[i]['가격'] = dicMV1[i]
                dicScatter[i]['구분'] = 1

    Image.SaveDFImageWithScatter2(df=df, savePath=imgFilePath, dicScatterData=dicScatter, title=code, x='날짜', y='종가')

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
#     except Exception as e:
#         print("{0} / {1} - fail : {2}".format(idx+1, len(df), e))

for i in [20, 30, 40, 50, 60]:
    for j in [10, 20, 30, 60]:
        usingMostPrice(i, 30, j)
