import matplotlib.pyplot as plt
import module.dataProcessing as dataProcessing
import os
import pandas as pd

'''
이미지 사용 함수 구현
'''
def TestSaveImage(sFilePath, code, df, dic) :
    # 라인 그리기
    setPlot(df=df, x='날짜', y='종가')

    # 점찍기
    for i in dic :
        setScatter(x=i, y=dic[i])

    plt.title(code)
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()

# 점찍기

# def setScatter(x, y) :
#     plt.scatter(x, y)

def setScatter(x, y, color=None) :
    plt.scatter(x, y, color = color)

# 라인 그리기

# def setPlot(df, x, y) :
#     '''
#     :param df: plot 할 df 
#     :param x: x 축에 들어갈 df 열
#     :param y: y 축에 들어갈 df 열
#     '''
#     plt.plot(df[x], df[y])

def setPlot(df, x, y, label=None) :
    '''
    :param df: plot 할 df 
    :param x: x 축에 들어갈 df 열
    :param y: y 축에 들어갈 df 열
    '''
    plt.plot(df[x], df[y], label = label)


def SaveDFImage(code, df, sFilePath):
    tmpFolder = os.path.dirname(sFilePath)

    if not os.path.isdir(tmpFolder):
        os.makedirs(tmpFolder)

    # df 를 이미지로 저장

    plt.figure(figsize=(20, 15))
    plt.axhline(y=1, color='r', linestyle='-')

    plt.plot(df['날짜'], df['종가'])
    plt.title(code)

    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()
    plt.close("all")

def SaveDFImage2DF(code, df1, df2, sFilePath):
    tmpFolder = os.path.dirname(sFilePath)

    if not os.path.isdir(tmpFolder):
        os.makedirs(tmpFolder)

    # df 를 이미지로 저장

    medianY = round((df1['종가'].max() + df1['종가'].min()) / 2, 3)

    plt.figure(figsize=(20, 15))
    plt.axhline(y=medianY, color='r', linestyle='--')

    plt.plot(df1['날짜'], df1['종가'], color='Black')
    plt.plot(df2['날짜'], df2['종가'], color='Orange', linestyle='--')
    plt.title(code)

    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df1) / 2, len(df1) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()
    plt.close("all")

def SaveDFImageMinute(code, df, sFilePath):
    # df 를 이미지로 저장
    plt.plot(df['체결시각'], df['체결가'])

    plt.title(code)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithScatter(code, df, sFilePath):
    lstHighDayPriceIdx = dataProcessing.RemainNDayPriceHighLowPrice(df, 30, "High")
    lstLowDayPriceIdx = dataProcessing.RemainNDayPriceHighLowPrice(df, 30, "Low")

    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    for i in lstHighDayPriceIdx:
        xPoint = i.split("^")[0]
        yPoint = int(float(i.split("^")[1]))
        plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기

    for i in lstLowDayPriceIdx:
        xPoint = i.split("^")[0]
        yPoint = int(float(i.split("^")[1]))
        plt.scatter(xPoint, yPoint, color="Blue")  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(code)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()

def SaveDFImageAddInfo(code, df, sFilePath, iBuyPrice, iExpectPrice, sExpectHighDay0):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.axhline(y=iExpectPrice, color='Blue', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))
    plt.text(0, iExpectPrice * 0.98, str(iExpectPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code) + " / " + sExpectHighDay0)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithBuyPrice(code, df, sFilePath, iBuyPrice):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code))
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()
    plt.close("all")


def SaveDFImageWithScatter2(df, x, y, dicScatterData, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''
    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df[y])
    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']
        plt.axvline(x = i, linestyle = 'dotted', color='gray')
        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
            facecolor = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
            facecolor = 'none'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'
            facecolor = 'black'
        elif dicScatterData[i]['구분'] == 3:
            color = 'Green'
            facecolor = 'Green'
        elif dicScatterData[i]['구분'] == 4:
            color = 'Yellow'
            facecolor = 'Yellow'
        plt.scatter(xPoint, yPoint, color=color, facecolor=facecolor)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(savePath)
    plt.clf()
    plt.close("all")

def SaveDFImageWithScatter3(df, x, dicScatterData, dicTotalHighPrice, dicTotalLowPrice, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)

    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color, s=100)  # 위치에 점 찍기

    for i in dicTotalLowPrice:
        xPoint = i
        yPoint = dicTotalLowPrice[i]
        plt.scatter(xPoint, yPoint, color='yellow', s=100)  # 위치에 점 찍기

    for i in dicTotalHighPrice:
        xPoint = i
        yPoint = dicTotalHighPrice[i]
        plt.scatter(xPoint, yPoint, color='green', s=100)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()
    plt.close("all")

def SaveDFImageWithScatter4(df, x, dicScatterData, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)

    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()

def SaveDFImageWithScatterWithMA(df, dfMA, x, dicScatterData, dicTotalHighPrice, dicTotalLowPrice, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')
    plt.plot(dfMA[x], dfMA['종가'])

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)
    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color, s=100)  # 위치에 점 찍기
    if len(dicTotalLowPrice) > 0 :
        for i in dicTotalLowPrice:
            xPoint = i
            yPoint = dicTotalLowPrice[i]
            plt.scatter(xPoint, yPoint, color='yellow', s=100)  # 위치에 점 찍기
    if len(dicTotalHighPrice) > 0 :
        for i in dicTotalHighPrice:
            xPoint = i
            yPoint = dicTotalHighPrice[i]
            plt.scatter(xPoint, yPoint, color='green', s=100)  # 위치에 점 찍기
    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()
    plt.close("all")

def SaveDFNetImageWithScatterWithMA(df, MAStart, MAEnd, MADiff, x, dicScatterData, dicTotalHighPrice, dicTotalLowPrice, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param MAStart: 그물망 이동평균선 시작 n 날짜
    :param MAEnd: 그물망 이동평균선 끝 n 날짜
    :param MADiff: 시작, 끝 n 날짜 간격
    :param x: x 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분'], 생략가능
    :param dicTotalHighPrice : key : '날짜',  value : ['가격', '구분'], 생략가능
    :param dicTotalLowPrice : key : '날짜',  value : ['가격', '구분'], 생략가능
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')

    # 그물망 이동평균선 계산

    for i in range(MAStart, MAEnd) :
        if i % MADiff != 0 :
            continue
        day = i
        dfNet = pd.DataFrame(columns=['날짜', '종가'])
        movingAverage = 0

        for idx, row in df.iterrows():

            if idx + day > len(df):
                break
            n = day
            tmp = 0
            for j in range(0, n):
                tmp += int(df.loc[idx + j]['종가'])
            movingAverage = tmp / n
            movingAverage = int(movingAverage)

            dfNet.loc[len(dfNet)]= [row['날짜'], movingAverage]

        plt.plot(dfNet[x], dfNet['종가'], linestyle='dotted', label=day)
        # plt.plot(dfNet[x], dfNet['종가'], linestyle='dotted', color='gray')


    if len(dicScatterData) > 0 :
        for i in dicScatterData:
            xPoint = i
            yPoint = dicScatterData[i]['가격']

            if dicScatterData[i]['구분'] == 0:
                color = 'blue'
            elif dicScatterData[i]['구분'] == 1:
                color = 'red'
            elif dicScatterData[i]['구분'] == 2:
                color = 'black'

            plt.scatter(xPoint, yPoint, color=color, s=100)  # 위치에 점 찍기

    if len(dicTotalLowPrice) > 0 :
        for i in dicTotalLowPrice:
            xPoint = i
            yPoint = dicTotalLowPrice[i]
            plt.scatter(xPoint, yPoint, color='yellow', s=100)  # 위치에 점 찍기

    if len(dicTotalHighPrice) > 0 :
        for i in dicTotalHighPrice:
            xPoint = i
            yPoint = dicTotalHighPrice[i]
            plt.scatter(xPoint, yPoint, color='green', s=100)  # 위치에 점 찍기

    plt.title(title)
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()
    plt.close("all")

def SaveDFImageWithScatterWithMAWithAddDate(df, dfMA, x, dicScatterData, dicTotalHighPrice, dicTotalLowPrice, title, savePath):
    '''
    :param df: 네이버 주식 시세 df, dataProcess.GetStockInfo 결과값
    :param x: x 축
    :param y: y 축
    :param dicScatterData: key : '날짜',  value : ['가격', '구분']
    :param title: 이미지 상당 제목명
    :param savePath: 이미지 파일 저장위치
    :return:
    '''

    # df 를 이미지로 저장
    plt.figure(figsize=(20, 15))
    plt.plot(df[x], df['종가'], label = 'end')
    plt.plot(df[x], df['고가'], label='high', linestyle='dashed')
    plt.plot(df[x], df['저가'], label='low', linestyle='dashed')
    plt.plot(dfMA[x], dfMA['종가'])

    # for i in dicScatterData:
    #     print(i)
    # print(dicScatterData)

    for i in dicScatterData:
        xPoint = i
        yPoint = dicScatterData[i]['가격']

        if dicScatterData[i]['구분'] == 0:
            color = 'blue'
        elif dicScatterData[i]['구분'] == 1:
            color = 'red'
        elif dicScatterData[i]['구분'] == 2:
            color = 'black'

        plt.scatter(xPoint, yPoint, color=color, s=100)  # 위치에 점 찍기

    dfTemp = df.set_index('날짜')

    for i in dicTotalLowPrice:
        xPoint = i
        yPoint = dicTotalLowPrice[i]
        plt.scatter(xPoint, yPoint, color='blue', s=100)  # 위치에 점 찍기

        tmpIdxTargetDate = dfTemp.index.get_loc(i)
        tmpIdxTargetDate = tmpIdxTargetDate - 3
        if tmpIdxTargetDate >= 0:
            dateTemp = df.loc[tmpIdxTargetDate]['날짜']
            startPriceTemp = df.loc[tmpIdxTargetDate]['시가']
            plt.scatter(dateTemp, startPriceTemp, color='orange', s=30)  # 위치에 점 찍기

        tmpIdxTargetDate = dfTemp.index.get_loc(i)
        tmpIdxTargetDate = tmpIdxTargetDate - 4
        if tmpIdxTargetDate >= 0:
            dateTemp = df.loc[tmpIdxTargetDate]['날짜']
            startPriceTemp = df.loc[tmpIdxTargetDate]['시가']
            plt.scatter(dateTemp, startPriceTemp, color='orange', s=30)  # 위치에 점 찍기

        tmpIdxTargetDate = dfTemp.index.get_loc(i)
        tmpIdxTargetDate = tmpIdxTargetDate - 5
        if tmpIdxTargetDate >= 0:
            dateTemp = df.loc[tmpIdxTargetDate]['날짜']
            startPriceTemp = df.loc[tmpIdxTargetDate]['시가']
            plt.scatter(dateTemp, startPriceTemp, color='orange', s=30)  # 위치에 점 찍기




    for i in dicTotalHighPrice:
        xPoint = i
        yPoint = dicTotalHighPrice[i]
        plt.scatter(xPoint, yPoint, color='Red', s=100)  # 위치에 점 찍기

        tmpIdxTargetDate = dfTemp.index.get_loc(i)
        tmpIdxTargetDate = tmpIdxTargetDate - 3
        if tmpIdxTargetDate >= 0:
            dateTemp = df.loc[tmpIdxTargetDate]['날짜']
            startPriceTemp = df.loc[tmpIdxTargetDate]['시가']
            plt.scatter(dateTemp, startPriceTemp, color='black', s=30)  # 위치에 점 찍기

        tmpIdxTargetDate = dfTemp.index.get_loc(i)
        tmpIdxTargetDate = tmpIdxTargetDate - 4
        if tmpIdxTargetDate >= 0:
            dateTemp = df.loc[tmpIdxTargetDate]['날짜']
            startPriceTemp = df.loc[tmpIdxTargetDate]['시가']
            plt.scatter(dateTemp, startPriceTemp, color='black', s=30)  # 위치에 점 찍기

        tmpIdxTargetDate = dfTemp.index.get_loc(i)
        tmpIdxTargetDate = tmpIdxTargetDate - 5
        if tmpIdxTargetDate >= 0:
            dateTemp = df.loc[tmpIdxTargetDate]['날짜']
            startPriceTemp = df.loc[tmpIdxTargetDate]['시가']
            plt.scatter(dateTemp, startPriceTemp, color='black', s=30)  # 위치에 점 찍기

    # plt.grid(color='gray', linestyle='--')
    plt.title(title)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()
    plt.close("all")


def SaveDFImageAddInfo(code, df, sFilePath, iBuyPrice, iExpectPrice, sExpectHighDay0):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.axhline(y=iExpectPrice, color='Blue', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))
    plt.text(0, iExpectPrice * 0.98, str(iExpectPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code) + " / " + sExpectHighDay0)
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()


def SaveDFImageWithBuyPrice(code, df, sFilePath, iBuyPrice):
    # df 를 이미지로 저장
    # plt.plot(df['날짜'], df['종가'], label=code)
    plt.plot(df['날짜'], df['종가'])

    # y 라인 그리기
    plt.axhline(y=iBuyPrice, color='Black', linestyle='-')
    plt.text(0, iBuyPrice * 1.02, str(iBuyPrice))

    # plt.scatter(xPoint, yPoint, color="red")  # 위치에 점 찍기
    # plt.text(xPoint, yPoint, str(yPoint))  # 위치에 텍스트 추가

    # 그리드 설정
    # plt.grid(color='gray', linestyle='--')
    plt.title(str(code))
    # plt.legend(loc='upper left')
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(df) - 1], rotation=30)  # x 축 thick 지정 갯수 출력
    plt.savefig(sFilePath)
    plt.clf()

def SaveImage(savePath, title, lstPlotDF, lstScatterDic=None):
    
    # :param savePath: 
    # :param title:
    # :param lstPlotDF: 값으로 [df, x축 값, y축 값, linestyle, color 저장] ex) [df, '날짜', '가격', 'dashed', 'black']
    # :param lstScatterDic: 값으로 2중 dic 저장 ex) {'날짜' : {'가격' : 가격, 'color' : color}}
    # :param x: plot x 축
    # :param y: plot y 축

    plt.figure(figsize=(20, 15))
    
    # 라인 그리기
    for lst in lstPlotDF :
        df = lst[0]
        xThick = lst[1]
        yThick = lst[2]
        lineStyle = lst[3]
        color = lst[4]

        if (not lineStyle is None or not lineStyle == "") and (not color is None or not color == "") :
            plt.plot(df[xThick], df[yThick], linestyle=lineStyle, color=color)
        elif not lineStyle is None or not lineStyle == "" :
            plt.plot(df[xThick], df[yThick], linestyle=lineStyle)
        elif not color is None or not color == "" :
            plt.plot(df[xThick], df[yThick], color=color)
        else :
            plt.plot(df[xThick], df[yThick])

    # for df in lstPlotDFDashed :
    #     plt.plot(df[x], df[y], linestyle='dashed')

    # for df in lstPlotDFDotted :
    #     plt.plot(df[x], df[y], linestyle='dotted')

    # 점 찍기
    if len(lstScatterDic) > 0 :
        for dic in lstScatterDic :
            for i in dic :
                # dic 형태, {'날짜' : {'가격' : 가격}}
                xPoint = i
                yPoint = dic[i]['가격']
                if 'color' in dic[i].keys() :
                    plt.scatter(xPoint, yPoint, s=400, color=dic[i]['color'], alpha=0.5)               # 위치에 점 찍기
                else :
                    plt.scatter(xPoint, yPoint, s=400, color='red', alpha=0.5)
    
    plt.title(title)
    plt.gca().invert_xaxis()  # x 축 반전
    plt.xticks([0, len(df) / 2, len(lstPlotDF[0][0]) - 1], rotation=30)  # x 축 thick 지정 갯수 출력

    plt.savefig(savePath)
    plt.clf()
    plt.close("all")
            
            
        
        
        



    
    
