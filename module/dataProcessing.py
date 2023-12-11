import time
import pandas as pd
import warnings
from datetime import datetime, timedelta
import exchange_calendars as ecals
import requests
import operator
from bs4 import BeautifulSoup

startTime = time.time()

######## FutureWarring 방지 ########
warnings.simplefilter(action='ignore', category=FutureWarning)  # FutureWarning 제거


### 한국거래소 영업일 계산
def calculateBusinessDay(day):
    # day = x 일때, x 일전 영업일을 출력]
    XKRX = ecals.get_calendar("XKRX")  # 한국 코드
    day = day * -1
    count = 0
    targetDay = 0
    dayCount = day + 2
    todayDay = ""

    for x in range(dayCount - 1):
        while targetDay != x + 1:
            if XKRX.is_session(datetime.today().date() - timedelta(days=count)):
                targetDay = targetDay + 1
            count = count + 1
        todayDay = str(datetime.today().date() - timedelta(days=count - 1)).replace("-", "")

    return todayDay


def dicHighestPrice(df, day):
    dicResult = {}

    for idx, row in df.iterrows():
        tmpFlag = False

        for i in range(1, day + 1):
            if idx + i < len(df):
                if row['고가'] < df.loc[idx + i]['고가']:
                    tmpFlag = True
                    break
            if idx - i > 0:
                if row['고가'] < df.loc[idx - i]['고가']:
                    tmpFlag = True
                    break
        if not tmpFlag:
            dicResult[row['날짜']] = row['고가']

    return dicResult


def dicLowestPrice(df, day):
    dicResult = {}

    for idx, row in df.iterrows():
        tmpFlag = False

        for i in range(1, day + 1):
            if idx + i < len(df):
                if row['저가'] > df.loc[idx + i]['저가']:
                    tmpFlag = True
                    break
            if idx - i > 0:
                if row['저가'] > df.loc[idx - i]['저가']:
                    tmpFlag = True
                    break
        if not tmpFlag:
            dicResult[row['날짜']] = row['저가']

    return dicResult


# n 일자 전후로 최소값, 최대값 유지 됬던 날짜의 주식정보
def RemainNDayPriceHighLowPrice(df, day, gubun):
    result = []

    for i in range(0, len(df) - 1):
        bContinue = True

        if gubun.upper() == "HIGH":
            iPrice = df.iloc[i]['고가']
        if gubun.upper() == "LOW":
            iPrice = df.iloc[i]['저가']

        # 최대값 날짜 구하기
        if gubun.upper() == "HIGH":
            if bContinue:
                for j in range(1, day):
                    iTargetDay = i - j
                    if iTargetDay < 0:
                        continue
                    if df.iloc[iTargetDay]['고가'] > iPrice:
                        bContinue = False
                    if not bContinue:
                        break

            if bContinue:
                for j in range(1, day):
                    iTargetDay = i + j
                    if iTargetDay > len(df.index) - 1:
                        continue
                    if df.iloc[iTargetDay]['고가'] > iPrice:
                        bContinue = False
                    if not bContinue:
                        break

        # 최소값 날짜 구하기
        if gubun.upper() == "LOW":
            if bContinue:
                for j in range(1, day):
                    iTargetDay = i - j
                    if iTargetDay < 0:
                        continue
                    if df.iloc[iTargetDay]['저가'] < iPrice:
                        bContinue = False
                    if not bContinue:
                        break

            if bContinue:
                for j in range(1, day):
                    iTargetDay = i + j
                    if iTargetDay > len(df.index) - 1:
                        continue
                    if df.iloc[iTargetDay]['저가'] < iPrice:
                        bContinue = False
                    if not bContinue:
                        break

        if bContinue:
            if len(result) == 0:
                result.append(df.iloc[i]['날짜'] + "^" + str(iPrice) + "^" + str(i))
            else:
                if result[-1].split("^")[1] != str(iPrice):
                    result.append(df.iloc[i]['날짜'] + "^" + str(iPrice) + "^" + str(i))

    return result


def UpPricePre5DayPattern(code):
    df = GetStockPrice(code, 250)
    cntH = 0
    cntL = 0
    pre1 = [cntH, cntL]
    pre2 = [cntH, cntL]
    pre3 = [cntH, cntL]
    pre4 = [cntH, cntL]
    pre5 = [cntH, cntL]

    df = df.reset_index(drop=True)

    dicIndexPattern = {}

    # 종가 상승 마감에 대해 전1일부터 전5일까지의 패턴
    for i in range(0, len(df.index) - 5):
        sTmp = ""
        if df.iloc[i]['종가'] > df.iloc[i]['시가']:  # 종가 상승 마감
            if df.iloc[i + 1]['종가'] > df.iloc[i + 1]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 2]['종가'] > df.iloc[i + 2]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 3]['종가'] > df.iloc[i + 4]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 4]['종가'] > df.iloc[i + 4]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp
            if df.iloc[i + 5]['종가'] > df.iloc[i + 5]['시가']:
                sTmp = "H" + sTmp
            else:
                sTmp = "L" + sTmp

            if sTmp not in dicIndexPattern.keys():
                dicIndexPattern[sTmp] = 1
            else:
                dicIndexPattern[sTmp] += 1

    print(len(df))
    print(sum(dicIndexPattern.values()))

    # 밸류 값에 대해 내림차순
    dicIndexPattern = sorted(dicIndexPattern.items(), key=operator.itemgetter(1), reverse=True)

    for key in dicIndexPattern:
        print(key)


def ExpectNextHighPrice(code, df):
    try:
        lstLowDays = RemainNDayPriceHighLowPrice(df, 30, "low")
        lstHighDays = RemainNDayPriceHighLowPrice(df, 30, "high")

        if len(lstLowDays) < 3 or len(lstHighDays) < 2:
            return None

        LowDay0 = datetime.strptime(lstLowDays[0].split("^")[0], "%Y.%m.%d")
        LowDay1 = datetime.strptime(lstLowDays[1].split("^")[0], "%Y.%m.%d")
        LowDay2 = datetime.strptime(lstLowDays[2].split("^")[0], "%Y.%m.%d")
        LowPrice0 = int(float(lstLowDays[0].split("^")[1]))
        LowPrice1 = int(float(lstLowDays[1].split("^")[1]))
        LowPrice2 = int(float(lstLowDays[2].split("^")[1]))

        LowDayDiff1 = int(str(LowDay0 - LowDay1).split(" ")[0])
        LowDayDiff2 = int(str(LowDay1 - LowDay2).split(" ")[0])

        LowPriceDiff1 = int(float(LowPrice0) - float(LowPrice1))
        LowPriceDiff2 = int(float(LowPrice1) - float(LowPrice2))
        dayPerLowPrice2 = int(LowPriceDiff2 / LowDayDiff2)

        HighDay1 = datetime.strptime(lstHighDays[0].split("^")[0], "%Y.%m.%d")
        HighDay2 = datetime.strptime(lstHighDays[1].split("^")[0], "%Y.%m.%d")

        HighPrice1 = int(float(lstHighDays[0].split("^")[1]))
        HighPrice2 = int(float(lstHighDays[1].split("^")[1]))

        HighDayDiff2 = int(str(HighDay1 - HighDay2).split(" ")[0])
        HighDayDiff1 = (LowDayDiff1 + LowDayDiff2 + HighDayDiff2) / 3

        # 계산값
        ExpectHighDay0 = HighDay1 + timedelta(days=HighDayDiff1)
        ExpectLowDay0 = LowDay1 + timedelta(days=HighDayDiff1)

        ExpectLowPrice0 = int(dayPerLowPrice2 * HighDayDiff1 + LowPrice1)
        ExpectHighPrice1 = int(dayPerLowPrice2 * HighDayDiff1 + HighPrice2)

        ExpectActHighPrice0 = dayPerLowPrice2 * LowDayDiff1 + HighPrice1
        ExpectAsmHighPrice0 = dayPerLowPrice2 * LowDayDiff1 + ExpectHighPrice1

        # 조건 예외사항 뽑기

        if ExpectHighDay0 < LowDay0:
            return None
        if LowDay0 < HighDay1:
            return None
        if ExpectLowPrice0 * 1.1 <= LowPrice0 or ExpectLowPrice0 * 0.9 >= LowPrice0:
            return None
        if ExpectHighPrice1 * 1.1 <= HighPrice1 or ExpectHighPrice1 * 0.9 >= HighPrice1:
            return None

        sReturn = "{0}" \
                  "code : {1}{0}" \
                  "ExpectLowDay0 : {2}{0}" \
                  "LowDay0 : {3}{0}" \
                  "LowDay1 : {4}{0}" \
                  "LowDay2 : {5}{0}" \
                  "LowPrice0 : {6}{0}{0}" \
                  "ExpectHighDay0 : {7}{0}" \
                  "HighDay1 : {8}{0}" \
                  "HighDay2 : {9}{0}" \
                  "ExpectActHighPrice0 : {10}{0}" \
                  "ExpectActHighPrice1 : {11}{0}" \
                  "LowPriceDiff1 : {12}{0}" \
            .format("<br>", code,
                    ExpectLowDay0.strftime("%Y.%m.%d"),
                    LowDay0.strftime("%Y.%m.%d"),
                    LowDay1.strftime("%Y.%m.%d"),
                    LowDay2.strftime("%Y.%m.%d"),
                    LowPrice0,
                    ExpectHighDay0.strftime("%Y.%m.%d"),
                    HighDay1.strftime("%Y.%m.%d"),
                    HighDay2.strftime("%Y.%m.%d"),
                    ExpectActHighPrice0,
                    ExpectAsmHighPrice0,
                    LowPriceDiff1)

    except Exception as e:
        return str(code) + "\n" + str(e)

    return sReturn


def GetStockPrice(code, count):
    # 한국 지수별 가격정보 가져오기
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    df = pd.DataFrame()
    url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, 1)
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    html = BeautifulSoup(res.text, 'lxml')
    pgrr = html.find('td', class_='pgRR').a['href']
    page = int(count / 10 + 1)

    if page > int(pgrr.split("=")[-1]) + 1:  # 총 페이지 보다 높으면 마지막 페이지 가져오기
        page = int(pgrr.split("=")[-1]) + 1

    for page in range(1, page):
        url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, page)
        res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        df = pd.concat([df, pd.read_html(res.text, header=0)[0]], axis=0)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    df = df.reset_index(drop=False)

    return df


def GetStockPriceWithPage(code, page):
    # 한국 지수별 가격정보 가져오기

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
    time = datetime.today().strftime('%Y%m%d')
    time = str(time) + ("180000")

    url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, 1)
    res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    html = BeautifulSoup(res.text, 'lxml')
    pgrr = html.find('td', class_='pgRR').a['href']

    if page == -1:  # page 를 -1 로 했을 경우 전체 페이지 가져오기
        page = pgrr.split("=")[-1]
        page = int(page) + 1

    if page > int(pgrr.split("=")[-1]) + 1:  # 총 페이지 보다 높으면 마지막 페이지 가져오기
        page = int(pgrr.split("=")[-1]) + 1

    df = pd.DataFrame()
    for i in range(1, page):
        url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}".format(code, time, i)
        res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        df = pd.concat([df, pd.read_html(res.text, header=0)[0]], axis=0)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    df = df.reset_index(drop=False)

    return df


def GetStockPriceMinute(code):
    # 한국 지수별 가격정보 가져오기
    try :
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
        time = datetime.today().strftime('%Y%m%d')
        time = str(time) + ("180000")
    
        url = "https://finance.naver.com/item/sise_time.naver?code={}&thistime={}&page={}".format(code, time, 1)
        res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        html = BeautifulSoup(res.text, 'lxml')
        pgrr = html.find('td', class_='pgRR').a['href']
        page = pgrr.split("=")[-1]
        page = int(page) + 1
        df = pd.DataFrame()
        for i in range(1, page):
            url = "https://finance.naver.com/item/sise_time.naver?code={}&thistime={}&page={}".format(code, time, i)
            res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
            df = pd.concat([df, pd.read_html(res.text, header=0)[0]], axis=0)
    except Exception as e :
        df = GetStockPrice(code, 20)
        df.rename(columns={"체결가": "종가"})
        print(df)
        time.time.sleep(30)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
    df = df.reset_index(drop=False)

    return df


def CheckReturnPosition(df, gubun, countTick):
    tick = GetTickFromMinuteDF(df)
    max = int(df.max()['체결가'])
    min = int(df.min()['체결가'])
    currentPrice = df.loc[0]['체결가']
    diffTickPrice = tick * countTick

    if gubun.upper() == 'UP':
        if currentPrice == max - diffTickPrice or currentPrice == max - diffTickPrice - tick:
            print("UP체결시각 : {0}, 체결가 : {1}".format(df.loc[0]['체결시각'], df.loc[0]['체결가']))
            return currentPrice

    if gubun.upper() == 'DOWN':
        if currentPrice == min + diffTickPrice or currentPrice == min + diffTickPrice + tick:
            print("DOWN체결시각 : {0}, 체결가 : {1}".format(df.loc[0]['체결시각'], df.loc[0]['체결가']))
            return currentPrice


def CheckReturnPositionInOrder(df, gubun, countTick):
    tick = GetTickFromMinuteDF(df)
    max = 0
    min = 9999999
    diffTickPrice = tick * countTick

    df = df.loc[::-1]

    if gubun.upper() == 'UP':

        for idx, row in df.iterrows():
            if row['체결가'] > max:
                max = row['체결가']
            if row['체결가'] + diffTickPrice == max:
                print("UP체결시각 : {0}, 체결가 : {1}".format(row['체결시각'], row['체결가']))

        if gubun.upper() == 'DOWN':

            for idx, row in df.iterrows():
                if row['체결가'] < min:
                    min = row['체결가']
                if row['체결가'] - diffTickPrice == min:
                    print("UP체결시각 : {0}, 체결가 : {1}".format(row['체결시각'], row['체결가']))


def GetTickFromDF(df):
    '''
    호가 단위
    2천원 미만  1원
    2천원 이상  ~5천원 미만	    5원
    5천원 이상  ~2만원 미만	    10원
    2만원 이상  ~5만원 미만	    50원
    5만원 이상  ~20만원 미만	    100원
    20만원 이상 ~50만원 미만	    500원
    50만원 이상              	1,000원
    '''

    price = int(df.iloc[0]['시가'])

    if price < 2000:
        return 1
    elif 2000 <= price < 5000:
        return 5
    elif 5000 <= price < 20000:
        return 10
    elif 20000 <= price < 50000:
        return 50
    elif 50000 <= price < 200000:
        return 100
    elif 200000 <= price < 500000:
        return 500
    elif 500000 <= price:
        return 1000


def GetTickFromMinuteDF(df):
    '''
    호가 단위
    2천원 미만  1원
    2천원 이상  ~5천원 미만	    5원
    5천원 이상  ~2만원 미만	    10원
    2만원 이상  ~5만원 미만	    50원
    5만원 이상  ~20만원 미만	    100원
    20만원 이상 ~50만원 미만	    500원
    50만원 이상              	1,000원
    '''

    df = df.iloc[::-1]
    price = int(df.iloc[0]['체결가'])

    if price < 2000:
        return 1
    elif 2000 <= price < 5000:
        return 5
    elif 5000 <= price < 20000:
        return 10
    elif 20000 <= price < 50000:
        return 50
    elif 50000 <= price < 200000:
        return 100
    elif 200000 <= price < 500000:
        return 500
    elif 500000 <= price:
        return 1000


def GetMovingAverage(df, day):
    # 이동평균선 계산
    dic = {}

    for idx, row in df.iterrows():

        if idx + day > len(df):
            break

        n = day

        tmp = 0
        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])
        movingAverage = tmp / n
        movingAverage = int(movingAverage)

        dic[row['날짜']] = movingAverage

    return dic

def GetMovingAverageRetDF(df, day):
    # 이동평균선 계산
    dfResult = pd.DataFrame(columns=['날짜', '종가'])

    for idx, row in df.iterrows():

        if idx + day > len(df):
            break

        n = day

        tmp = 0
        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])
        movingAverage = tmp / n
        movingAverage = int(movingAverage)

        dfResult.loc[len(dfResult)]= [row['날짜'], movingAverage]

    return dfResult

def GetDateFollowingMAPattern(df, day, gubun):
    '''
    :param df: 네이버 DF
    :param day: 이동평균선 날짜
    :param gubun: 'dduu' 같은 패턴
    :return:dic[날짜] = {'가격':이동평균가격}
    '''
    # GetPositionUseMA
    # df에 증감이 gubun을 따르는 day이동평균 인 지점을 dic['날짜'] = value 로 return

    # 이동평균 구하기
    dic = {}
    dicResult = {}

    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    # pd.set_option('display.max_colwidth', -1)

    for idx, row in df.iterrows():
        if idx + day > len(df):
            break

        n = day
        tmp = 0

        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])

        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dic[row['날짜']] = movingAverage
 
    for idx, key in enumerate(dic):
        if len(dic) < idx + len(gubun) + 1:
            break
        for idxJ, c in enumerate(gubun[::-1]):

            tmpFlag = False
            if c == 'u':
                if list(dic.values())[idx + idxJ] <= list(dic.values())[idx + idxJ + 1]:
                    tmpFlag = True
                    break

            if c == 'd':
                if list(dic.values())[idx + idxJ] >= list(dic.values())[idx + idxJ + 1]:
                    tmpFlag = True
                    break

        if tmpFlag == False:
            dicResult[key] = {'가격':dic[key]}
  
    return dicResult

def GetMV(df, day):
    # df에 증감이 gubun을 따르는 day이동평균 인 지점을 dic['날짜'] = value 로 return

    # 이동평균 구하기
    dic = {}

    for idx, row in df.iterrows():
        if idx + day > len(df):
            break

        n = day
        tmp = 0

        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])

        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dic[row['날짜']] = movingAverage

    return dic

def getUpDownMV(df, day, date):
    '''
    이동평균선의 상승, 하락추세를 리턴
    :param df: 네이버 시세 DF
    :param day: n 이동평균선
    :param date: 상승, 하락 추세 구할 날짜
    :return: 0 = up, 1 = down, 9 = df 길이 짧음.
    '''

    dfDateKey = df.set_index('날짜')
    idxDate = dfDateKey.index.get_loc(date)

    n = day
    targetMV = 0
    preMV = 0

    if idxDate + day >= len(df):
        return 9

    for j in range(0, n):
        targetMV += int(df.loc[idxDate + j]['종가'])

    for j in range(0, n):
        preMV += int(df.loc[idxDate + j + 1]['종가'])

    if targetMV > preMV :
        return 0
    else:
        return 1

def GetMVPattern(dic, gubun):

    dicResult = {}

    for idx, key in enumerate(dic):
        if len(dic) < idx + len(gubun) + 1:
            break

        check = True

        for idxJ, c in enumerate(gubun[::-1]):
            if c == 'u':
                if list(dic.values())[idx + idxJ] <= list(dic.values())[idx + idxJ + 1]:
                    check = False
                    break
            if c == 'd':
                if list(dic.values())[idx + idxJ] >= list(dic.values())[idx + idxJ + 1]:
                    check = False
                    break

        if check:
            dicResult[key] = dic[key]

    return dicResult

def checkStockSplit(df, day):
    for idx, row in df.iterrows():
        if idx > day:
            return True

        if idx + 1 > len(df):
            return True

        if df.loc[idx]['종가'] > df.loc[idx + 1]['종가'] * 1.6:
            print(idx)
            return False
        if df.loc[idx]['종가'] < df.loc[idx + 1]['종가'] * 0.4:
            print(idx)
            return False


def standardizationStockSplit(df):
    global gab

    gab = 1
    totalGab = 1

    for idx, row in df.iterrows():

        if idx + 2 > len(df):
            break

        gabCheck = True

        if df.loc[idx]['종가'] + df.loc[idx]['전일비'] == df.loc[idx + 1]['종가'] or df.loc[idx]['종가'] - df.loc[idx]['전일비'] == \
                df.loc[idx + 1]['종가']:
            gabCheck = False

        if gabCheck:
            if df.loc[idx]['종가'] > df.loc[idx + 1]['종가']:
                gab = (df.loc[idx]['종가'] - df.loc[idx]['전일비']) / df.loc[idx + 1]['종가']
                if totalGab != 1:
                    df.iloc[idx, df.columns.get_loc('종가')] = int(df.loc[idx]['종가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('시가')] = int(df.loc[idx]['시가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('고가')] = int(df.loc[idx]['고가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('저가')] = int(df.loc[idx]['저가'] * totalGab)
                totalGab = gab * totalGab
                continue

            if df.loc[idx]['종가'] < df.loc[idx + 1]['종가']:
                gab = (df.loc[idx]['종가'] + df.loc[idx]['전일비']) / df.loc[idx + 1]['종가']
                if totalGab != 1:
                    df.iloc[idx, df.columns.get_loc('종가')] = int(df.loc[idx]['종가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('시가')] = int(df.loc[idx]['시가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('고가')] = int(df.loc[idx]['고가'] * totalGab)
                    df.iloc[idx, df.columns.get_loc('저가')] = int(df.loc[idx]['저가'] * totalGab)
                totalGab = gab * totalGab
                continue

        if totalGab != 1:
            df.iloc[idx, df.columns.get_loc('종가')] = int(df.loc[idx]['종가'] * totalGab)
            df.iloc[idx, df.columns.get_loc('시가')] = int(df.loc[idx]['시가'] * totalGab)
            df.iloc[idx, df.columns.get_loc('고가')] = int(df.loc[idx]['고가'] * totalGab)
            df.iloc[idx, df.columns.get_loc('저가')] = int(df.loc[idx]['저가'] * totalGab)

    df = df.iloc[:-1]

    return df

'''
        # 병합
        if df.loc[idx]['종가'] > df.loc[idx+1]['종가'] * 1.3:
            gab = gab * (df.loc[idx]['종가'] - df.loc[idx]['전일비']) / df.loc[idx+1]['종가']
            totalGab = totalGab * gab
            print(df.loc[idx]['날짜'])
            print(totalGab)
            continue

        # 분할
        if df.loc[idx]['종가'] < df.loc[idx+1]['종가'] * 0.7:
            tmpGab = df.loc[idx + 1]['종가'] / (df.loc[idx]['종가'] + df.loc[idx]['전일비'])
            gab = 1/tmpGab
            totalGab = totalGab * gab
            print(df.loc[idx]['날짜'])
            print(totalGab)
            continue

        if totalGab != 1:
            df.iloc[idx, df.columns.get_loc('종가')] = df.loc[idx]['종가'] * totalGab
            df.iloc[idx, df.columns.get_loc('시가')] = df.loc[idx]['시가'] * totalGab
            df.iloc[idx, df.columns.get_loc('고가')] = df.loc[idx]['고가'] * totalGab
            df.iloc[idx, df.columns.get_loc('저가')] = df.loc[idx]['저가'] * totalGab
    df = df.iloc[:-1]

    return df
'''

# 최신 최저가 최고가 구하기
def getFirstHighLowPrice(df, day, gubun1, gubun2):
    # gunun1 = n 일 동안 고, 저 유지
    # gubun2 = 최고, 최저

    ret = 0

    return ret

def getSecondHighLowPrice(df, date, day, gubun):
    # date = 시작되는 date
    # day = n 일 동안 고, 저 유지
    # gunun = n 일 동안 고, 저 유지

    ret = 0

    return ret

def getGubunPriceUseDate(df, listDate):

    # 날짜 데이터를 가지고, 종가, 고가, 저가, 시가 가져오기
    dicResult = {}

    dfDateKey = df.set_index('날짜')

    for i in listDate:
        dicResult[i] = {}
        dicResult[i]['종가'] = dfDateKey.loc[i]['종가']
        dicResult[i]['고가'] = dfDateKey.loc[i]['고가']
        dicResult[i]['저가'] = dfDateKey.loc[i]['저가']
        dicResult[i]['시가'] = dfDateKey.loc[i]['시가']

    return dicResult
        
def GetMostPriceFromDF(df, targetDate, day, gubun, n):
    '''
    :param df:
    :param date: 대상 날짜
    :param day:  유지 기간
    :param gubun: '고가', '저가' 구분
    :param n: 뽑을 갯수
    :return:
    '''

    dic = {}
    tmpKey = n

    dfDateKey = df.set_index('날짜')

    idxTargetDate = dfDateKey.index.get_loc(targetDate)

    while n != 0:

        for i in range(1, len(df)): # 대상 날짜에서 과거날짜 반복

            checkMost = True

            targetIdx = idxTargetDate + i # 비교날짜 인덱스 추출

            if targetIdx + 1 >= len(df):
                n -= 1
                break

            mostPrice = df.loc[targetIdx]['종가'] # 첫 비교날짜 가격 추출

            for j in range(1, day + 1): # 비교 날짜 앞뒤 날짜 추출 후 가격 최고, 최저 유지 비교
                # print('targetIdx : i')

                afterTargetIdx = targetIdx - j
                beforeTargetIdx = targetIdx + j

                if afterTargetIdx > idxTargetDate :

                    if gubun == '고가':
                        if mostPrice < df.loc[afterTargetIdx]['종가']:
                            checkMost = False
                            break

                    if gubun == '저가':
                        if mostPrice > df.loc[afterTargetIdx]['종가']:
                            checkMost = False
                            break

                if beforeTargetIdx < len(df) :
                    if gubun == '고가':
                        if mostPrice < df.loc[beforeTargetIdx]['종가']:
                            checkMost = False
                            break

                    if gubun == '저가':
                        if mostPrice > df.loc[beforeTargetIdx]['종가']:
                            checkMost = False
                            break

            if checkMost == True:
                dic[tmpKey - n] = {}
                dic[tmpKey - n]['날짜'] = df.loc[targetIdx]['날짜']
                dic[tmpKey - n]['가격'] = df.loc[targetIdx]['종가']
                n -= 1

            if n == 0:
                break

    if len(dic) == 0:
        return None

    return dic

def GetMostPriceOneSideFromDF(df, targetDate, day, gubun, n, continueDay):
    '''
    :param df:
    :param date: 대상 날짜
    :param day:  유지 기간
    :param gubun: '고가', '저가' 구분
    :param n: 뽑을 갯수
    :param continueDay : 반대되는 방향에서 최소, 최대값이 되기 위한 일수
    :return:
    '''

    dic = {}
    tmpKey = n

    dfDateKey = df.set_index('날짜')

    idxTargetDate = dfDateKey.index.get_loc(targetDate)

    while n != 0:

        for i in range(1, len(df)): # 대상 날짜에서 과거날짜 반복

            checkMostBefore = True
            checkMostAfter = True

            targetIdx = idxTargetDate + i # 비교날짜 인덱스 추출

            if targetIdx + 1 >= len(df):
                n -= 1
                break

            mostPrice = df.loc[targetIdx][gubun] # 첫 비교날짜 가격 추출

            for j in range(1, day + 1): # 비교 날짜 전 가격 최고, 최저 유지 비교

                beforeTargetIdx = targetIdx + j
                afterTargetIdx = targetIdx - j

                if beforeTargetIdx < len(df) and checkMostBefore and targetIdx - continueDay > 0:
                    if gubun == '고가':
                        for k in range(0, continueDay+1):
                            if k == 1:
                                continue
                            if mostPrice < df.loc[beforeTargetIdx - k][gubun] :
                                checkMostBefore = False
                                break

                    if gubun == '저가':
                        for k in range(0, continueDay+1):
                            if k == 1:
                                continue
                            if mostPrice > df.loc[beforeTargetIdx - k][gubun] :
                                checkMostBefore = False
                                break

                if afterTargetIdx >= 0 and checkMostAfter and targetIdx + continueDay < len(df):
                    if gubun == '고가':
                        for k in range(0, continueDay+1):
                            if k == 1:
                                continue
                            if mostPrice < df.loc[afterTargetIdx + k][gubun] :
                                checkMostAfter = False
                                break

                    if gubun == '저가':
                        for k in range(0, continueDay+1):
                            if k == 1:
                                continue
                            if mostPrice > df.loc[afterTargetIdx + k][gubun] :
                                checkMostAfter = False
                                break

                if checkMostBefore == False and checkMostAfter == False:
                    break

            if checkMostBefore == True or checkMostAfter == True:
                dic[tmpKey - n] = {}
                dic[tmpKey - n]['날짜'] = df.loc[targetIdx]['날짜']
                dic[tmpKey - n]['가격'] = df.loc[targetIdx][gubun]
                n -= 1

            if n == 0:
                break

    if len(dic) == 0:
        return None

    return dic

def GetMostPriceBeforeTargetDate(df, targetDate, day, gubun, n):
    '''
    :param df:
    :param date: 대상 날짜
    :param day:  유지 기간
    :param gubun: '고가', '저가' 구분
    :param n: 뽑을 갯수
    :return:
    '''

    dic = {}
    tmpKey = n

    dfDateKey = df.set_index('날짜')

    idxTargetDate = dfDateKey.index.get_loc(targetDate)

    while n != 0:

        for i in range(1, len(df)): # 대상 날짜에서 과거날짜 반복

            checkMost = True

            targetIdx = idxTargetDate + i # 비교날짜 인덱스 추출

            if targetIdx + 1 >= len(df):
                n -= 1
                break

            mostPrice = df.loc[targetIdx][gubun] # 첫 비교날짜 가격 추출

            for j in range(1, day + 1): # 비교 날짜 앞뒤 날짜 추출 후 가격 최고, 최저 유지 비교
                # print('targetIdx : i')

                beforeTargetIdx = targetIdx + j

                if beforeTargetIdx < len(df) :
                    if gubun == '고가':
                        if mostPrice < df.loc[beforeTargetIdx][gubun]:
                            checkMost = False
                            break

                    if gubun == '저가':
                        if mostPrice > df.loc[beforeTargetIdx][gubun]:
                            checkMost = False
                            break

            if checkMost == True:
                dic[tmpKey - n] = {}
                dic[tmpKey - n]['날짜'] = df.loc[targetIdx]['날짜']
                dic[tmpKey - n]['가격'] = df.loc[targetIdx][gubun]
                n -= 1

            if n == 0:
                break

    if len(dic) == 0:
        return None

    return dic

def GetMostPriceBeforeAfter(df, targetDate, before, after, gubun, n):
    '''
    :param df:
    :param targetDate: 대상 날짜
    :param before:  대상날짜 전 유지 기간
    :param after:  대상날짜 후 유지 기간
    :param gubun: '고가', '저가' 구분
    :param n: 뽑을 갯수
    :return:
    '''
    
    # if targetDate not in str(df['날짜']):
    #     print(targetDate)
    #     return None

    if df['날짜'].str.contains('targetDate').any():
        return None

    dic = {}
    tmpKey = n

    dfDateKey = df.set_index('날짜')

    idxTargetDate = dfDateKey.index.get_loc(targetDate)

    while n != 0:

        for i in range(1, len(df)): # 대상 날짜에서 과거날짜 반복

            checkMost = True

            targetIdx = idxTargetDate + i # 비교날짜 인덱스 추출

            if targetIdx + 1 >= len(df):
                n -= 1
                break

            mostPrice = df.loc[targetIdx]['종가'] # 첫 비교날짜 가격 추출

            for j in range(1, after + 1): # 비교 날짜 앞뒤 날짜 추출 후 가격 최고, 최저 유지 비교
                # print('targetIdx : i')

                afterTargetIdx = targetIdx - j

                if afterTargetIdx > -1 :

                    if gubun == '고가':
                        if mostPrice < df.loc[afterTargetIdx]['종가']:
                            checkMost = False
                            break

                    if gubun == '저가':
                        if mostPrice > df.loc[afterTargetIdx]['종가']:
                            checkMost = False
                            break
                else:
                    checkMost = False
                    break

            if not checkMost:
                continue

            for j in range(1, before + 1): # 비교 날짜 앞뒤 날짜 추출 후 가격 최고, 최저 유지 비교
                # print('targetIdx : i')

                beforeTargetIdx = targetIdx + j

                if beforeTargetIdx < len(df) :
                    if gubun == '고가':
                        if mostPrice < df.loc[beforeTargetIdx]['종가']:
                            checkMost = False
                            break

                    if gubun == '저가':
                        if mostPrice > df.loc[beforeTargetIdx]['종가']:
                            checkMost = False
                            break

            if checkMost == True:
                dic[tmpKey - n] = {}
                dic[tmpKey - n]['날짜'] = df.loc[targetIdx]['날짜']
                dic[tmpKey - n]['가격'] = df.loc[targetIdx]['종가']
                n -= 1

            if n == 0:
                break

    if len(dic) == 0:
        return None

    return dic

def getTrandLine(df, startDate, endDate, gubun):

    dfDateKey = df.set_index('날짜')
    startDateIdx = dfDateKey.index.get_loc(startDate)
    endDateIdx = dfDateKey.index.get_loc(endDate)
    diffDay = startDateIdx - endDateIdx

    startDatePrice = df.loc[startDateIdx][gubun]
    endDatePrice = df.loc[endDateIdx][gubun]
    diffPrice = endDatePrice - startDatePrice

    result = round(diffPrice / diffDay, 3)

    return result

def compareTwoDate(date1, date2):
    if date1 > date2:
        return True
    else:
        return False


def getProfitLoss(df, buyDate, profitPrice, lossPrice):
    '''
    :param df: 네이버 시세 DF
    :param buyDate: 손절 익절, 시작할 날짜
    :param profitPrice: 익절 가격
    :param LossPrice: 손절 가격
    :return: 0 = 익절, 1 = 손절, 9 = 두 해당사항 없음.
    '''

    dfDateKey = df.set_index('날짜')
    idxBuyDate = dfDateKey.index.get_loc(buyDate)

    for i in range(1, idxBuyDate+1) :
        targetIdx = idxBuyDate - i

        if df.loc[targetIdx]['고가'] >= profitPrice:
            return 0
        if df.loc[targetIdx]['저가'] < lossPrice:
            return 1

    return 9

def standardizaionPriceUseMV(df, day):
    '''
    :param df: 네이버 시세 DF
    :param day: n 이동평균선
    :return: 표준화된 df
    '''

    dfResult = df.head(0)
    dfResult = dfResult.drop(['index', '전일비', '거래량'], axis= 1)
    BreakFlag = False

    for idx, row in df.iterrows():

        EndPrice = 0
        StartPrice = 0
        HighPrice = 0
        LowPrice = 0

        for j in range(0, day):
            if len(df) <= idx + j + 1:
                BreakFlag = True
                break

            # 이동평균선 구해주기
            EndPrice += df.loc[idx+j]['종가']
            StartPrice += df.loc[idx + j]['시가']
            HighPrice += df.loc[idx + j]['고가']
            LowPrice += df.loc[idx + j]['저가']

        if BreakFlag:
            break

        EndPriceMV = EndPrice / day
        StartPriceMV = StartPrice / day
        HighPriceMV = HighPrice / day
        LowPriceMV = LowPrice / day

        standardEndPriceMV = round(row['종가'] / EndPriceMV, 4)
        standardStartPriceMV = round(row['시가'] / StartPriceMV, 4)
        standardHighPriceMV = round(row['고가'] / HighPriceMV, 4)
        standardLowPriceMV = round(row['저가'] / LowPriceMV, 4)

        # dataRow 추가
        dfResult.loc[len(dfResult)] = [row['날짜'], standardEndPriceMV, standardStartPriceMV, standardHighPriceMV, standardLowPriceMV]

    return dfResult

def standardizaionPriceUseMVRateDFPrice(df, day):
    '''
    :param df: 네이버 시세 DF
    :param day: n 이동평균선
    :return: 표준화된 df
    '''

    dfResult = df.head(0)
    dfResult = dfResult.drop(['index', '전일비', '거래량'], axis= 1)
    BreakFlag = False
    maxPrice = df['종가'].max()
    minPrice = df['종가'].min()
    medianPrice = round((maxPrice + minPrice) / 2, 3)

    for idx, row in df.iterrows():

        EndPrice = 0
        StartPrice = 0
        HighPrice = 0
        LowPrice = 0

        for j in range(0, day):
            if len(df) <= idx + j + 1:
                BreakFlag = True
                break

            # 이동평균선 구해주기
            EndPrice += df.loc[idx+j]['종가']
            StartPrice += df.loc[idx + j]['시가']
            HighPrice += df.loc[idx + j]['고가']
            LowPrice += df.loc[idx + j]['저가']

        if BreakFlag:
            break

        EndPriceMV = EndPrice / day
        StartPriceMV = StartPrice / day
        HighPriceMV = HighPrice / day
        LowPriceMV = LowPrice / day

        standardEndPriceMV = round(row['종가'] / EndPriceMV * medianPrice, 4)
        standardStartPriceMV = round(row['시가'] / StartPriceMV * medianPrice, 4)
        standardHighPriceMV = round(row['고가'] / HighPriceMV * medianPrice, 4)
        standardLowPriceMV = round(row['저가'] / LowPriceMV * medianPrice, 4)

        # dataRow 추가
        dfResult.loc[len(dfResult)] = [row['날짜'], standardEndPriceMV, standardStartPriceMV, standardHighPriceMV, standardLowPriceMV]

    return dfResult

def addDay(df, date, day):
    '''
    df = 네이버 종목명 주식 가격정보
    date = 추가 되어질 대상 날짜
    day = 추가 되어질 날짜 기간
    return = date 정보
    '''
    
    # reverse df
    df = df.loc[::-1]
    df = df.reset_index(drop=True)
    dfDateKey = df.set_index('날짜')
    idxDate = dfDateKey.index.get_loc(date)

    # df 에 해당 날짜가 없을 경우, 0 return
    if idxDate + day > len(df) + 1 : 
        return 0
    idxDate += day
    return df.loc[idxDate]['날짜']

def dicMAUpCrossPoint(df, MAUp, MADown) :

    '''
    :param df: 네이버 주식정보
    :param MAUp: 이동평균선 n 값
    :param MADown: 이동평균선 n 값
    :return: dicResult : 2중 딕셔너리 : 키 = 날짜, 값 = [가격, 구분], ex) dicResult['20231106']['가격'] = 1385
    '''

    dicResult = {}
    isTmp = False
    # MAStart 이평선
    dfMAUp = pd.DataFrame(columns=['날짜', '가격'])
    for idx, row in df.iterrows():
        if idx + max(MADown, MAUp) > len(df):
            break
        n = MAUp
        tmp = 0
        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])
        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dfMAUp.loc[len(dfMAUp)]= [row['날짜'], movingAverage]
    # MAEnd 이평선
    dfMADown = pd.DataFrame(columns=['날짜', '가격'])
    for idx, row in df.iterrows():
        if idx + max(MADown, MAUp) > len(df):
            break
        n = MADown
        tmp = 0
        for j in range(0, n):
            tmp += int(df.loc[idx + j]['종가'])
        movingAverage = tmp / n
        movingAverage = int(movingAverage)
        dfMADown.loc[len(dfMADown)]= [row['날짜'], movingAverage]
    # 이평선 돌파 혹은 하강 구하기
    for idx, row in dfMADown.iterrows() :
        if isTmp :
            if int(dfMADown.loc[idx]['가격']) > int(dfMAUp.loc[idx]['가격']) :
                dicResult[dfMADown.loc[idx]['날짜']] = {'가격':dfMADown.loc[idx]['가격']}
                isTmp = False
                continue

        if int(dfMADown.loc[idx]['가격']) < int(dfMAUp.loc[idx]['가격']) :
            isTmp = True
        else :
            isTmp = False

    return dicResult

    # 이동평균선 구하기

def calculTrade(df, lstDate, buyRate, takeBenefitRate, stopLossRate, adjustDay=None) :
    '''
    :param df: 네이버 주식정보
    :param lstDate: 매수할 날짜 리스트
    :param buyRate: 매수가 %
    :param takeBenefitRate: 익절가 %
    :param stopLossRate: 손절가 %
    :return dicResult : {'총':0, '매수:0, '익절':0, '손절':0}
    '''
    dicResult = {'총':0, '매수':0, '익절':0, '손절':0}
    dicResult['총'] = len(lstDate)

    for i in lstDate :
        DateIdx = df.index[df.날짜 == i][0]
        DateIdx = DateIdx - adjustDay
        if DateIdx < 0 :
            DateIdx = 0
            
        # 매수 시점 가격 정보
        # startPrice = int(df.loc[DateIdx]['시가'])
        startPrice = int(df.loc[DateIdx+1]['종가'])
        lowPrice = int(df.loc[DateIdx]['저가'])
        highPrice = int(df.loc[DateIdx]['고가'])

        # 매수, 매도 가격
        buyPrice = startPrice * buyRate
        sellPriceBenefit = round(buyPrice * takeBenefitRate, 2)
        sellPriceStopLoss = round(buyPrice * stopLossRate, 2)

        # 매수 플래그
        buyFlag = False
        SellFlagbenefit = False
        sellFlagstopLoss = False

        if buyPrice > lowPrice :
            print(df.loc[DateIdx]['날짜'])
            buyFlag = True
            dicResult['매수'] += 1
        else :
            continue # 매수 하지 않았다면, 매도까지 프로세스 진행하지 않는다.

        for i in range(1, DateIdx) :
            if DateIdx == 0:
                continue
            targetDateIdx = DateIdx - i
            targetHighPrice = df.loc[targetDateIdx]['고가']
            targetLowPrice = df.loc[targetDateIdx]['저가']

            if sellPriceBenefit < targetHighPrice : # 익절
                dicResult['익절'] += 1
                print("익절 : {0} // {1} // {2}".format(df.loc[targetDateIdx]['날짜'], sellPriceBenefit, buyPrice))
                break

            if sellPriceStopLoss > targetLowPrice : # 손절
                dicResult['손절'] += 1
                print("손절 : {0} // {1} // {2}".format(df.loc[targetDateIdx]['날짜'], sellPriceStopLoss, buyPrice))
                break

    return dicResult

def CrossDateStockPriceAndMV(df, dfMA, gubun) :
    '''
    주가가 이평선을 돌파한 지점의 날짜를 저장
    :param df: 네이버 주식정보
    :param dfMA: 이평선 정보
    :param gubun : "u" = 하락에서 상승, "d" 상승에서 하락
    :return dicResult : {'날짜':0, '종가:0, '익절':0, '손절':0}
    '''

    df = df.set_index('날짜')
    dicResult = {}
    tmp = False
    for idx, i in dfMA.iterrows() : # dfMA 반복. 날짜를 키 값으로 받아서 df 가격정보 추출
        if gubun.upper() == "U" :
            if tmp : # 앞 일자에서 조건을 만족
                if i['종가'] >= df.loc[i['날짜']]['종가'] :
                    dicResult[i['날짜']] = {'가격' : i['종가']}
                    tmp = False
                    continue
            if i['종가'] < df.loc[i['날짜']]['종가'] :
                tmp = True
            else :
                tmp = False
            
        elif gubun.upper() == "D" :
            if tmp : 
                if i['종가'] <= df.loc[i['날짜']]['종가'] :
                    dicResult[i['날짜']] = {'가격' : i['종가']}
                    tmp = False
                    continue
            if i['종가'] > df.loc[i['날짜']]['종가'] :
                tmp = True
            else :
                tmp = False
    
    return dicResult

def dateOfBetweenTwoMV(df, dfLongMA, dfShortMA) :
    '''
    주가가 긴 이동평균선 아래, 짧은 이동평균선 위에 존재하는 날짜들을 return
    :param df: 네이버 주식정보
    :param dfLongMA : 기간이 긴 이동평균선 DF
    :param dfShortMA : 기간이 짧은 이동평균선 DF
    :return dicResult : 2중 딕셔너리 : 키 = 날짜, 값 = [가격, 구분], ex) dicResult['20231106']['가격'] = 1385
    '''

    dicResult = {}

    for idx, row in df.iterrows():
        if idx > len(dfLongMA) :
            break
        currentPrice = df.loc[idx]['종가']
        longPrice = dfLongMA.loc[idx]['종가']
        shortPrice = dfShortMA.loc[idx]['종가']
        date = df.loc[idx]['날짜']

        if currentPrice < longPrice and currentPrice > shortPrice :
            dicResult[date] = {}
            dicResult[date].update({"가격": currentPrice})
    
    return dicResult

def isBetweenTwoMV(df, dfLongMA, dfShortMA, day) :
    '''
    주가가 긴 이동평균선 아래, 짧은 이동평균선 위에 존재하는 날짜들을 return
    :param df: 네이버 주식정보
    :param dfLongMA : 기간이 긴 이동평균선 DF
    :param dfShortMA : 기간이 짧은 이동평균선 DF
    :param day : df idx 0일자, 현재일 기준 + day 전일에 대해 조건을 구함
    :return 두 이평선 사이에 주가가 있으면 True, 그렇지 않으면 False
    '''
    currentPrice = df.loc[0+day]['종가']
    longPrice = dfLongMA.loc[0+day]['종가']
    shortPrice = dfShortMA.loc[0+day]['종가']

    if currentPrice < longPrice and currentPrice > shortPrice :
        return True
    else :
        return False
  

