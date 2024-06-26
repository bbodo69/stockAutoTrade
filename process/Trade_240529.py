import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop, QSize
import time
import pandas as pd
import datetime
import module.dataProcessing as dataProcessing
import module.GoogleDriveDownload as gdd
import module.excel_collection as excel_collection
import module.LoadConfig as LoadConfig
import module.sender_collection as sender_collection
import json
import os


class Values():
    def __init__(self):  # 기본값 설정
        ####### 계좌 관련 변수
        self.account_num = 0

class MyWindow(QMainWindow):
    # QMainWindow 를 상속
    delay = 3.6

    def __init__(self):  # 기본값 설정

        ####### 계좌 관련 변수
        self.total_asset = 0
        self.deposit = 0
        self.out_deposit = 0
        self.avail_deposit = 0
        self.estimated_balance = 0
        self.account_num = account_num
        self.use_money = 0
        self.use_money_percent = 0
        self.account_list = []
        self.account_stock_dict = {}  # 보유종목

        super().__init__()

        # 종료 메세지 출력
        self.setMinimumSize(QSize(500, 100))
        self.setWindowTitle("Alert Message")

        # pybutton = QPushButton('버튼 눌러야 컴퓨터 계속 사용 가능', self)
        # pybutton.clicked.connect(self.clickMethod)
        # pybutton.resize(400, 30)
        # pybutton.move(50, 35)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        ### event ###
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrCondition.connect(self.receive_trCondition)
        self.kiwoom.OnReceiveConditionVer.connect(self.receive_VerCondition)
        self.kiwoom.OnReceiveChejanData.connect(self.receive_Chejan)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

    def receive_Chejan(self, sGubun, nItemCnt, sFidlist):
        print(sGubun, nItemCnt, sFidlist)

    def clickMethod(self):
        QMessageBox.about(self, "", "자동종료 취소")
        sys.exit()

    def receive_VerCondition(self, ret, msg):
        self.receive_VerCondition.exit()

    def receive_trCondition(self, screenNo, codes, conditionName, conditionIndex, inquiry):
        print("@@ trCondition 시작")
        if codes == "":
            print("@@ 검색결과 없음")
        self.codeList = codes.split(';')
        del self.codeList[-1]
        self.receive_trCondition_loop.exit()

    def event_connect(self, err_code):
        if err_code == 0:
            print("@@ 로그인 성공")
        self.login_event_loop.exit()

    ### 실행 함수###
    def kiwoom_login(self):
        print("@@ 로그인 시작")
        self.login_event_loop = QEventLoop()
        self.kiwoom.CommConnect()
        self.login_event_loop.exec_()

    # 종목 매수 (in_strAccount, in_strCode, out_result)
    def buy_Stock(self, code, amount, price, accountNumber):
        print("@@ 주식매수")
        self.kiwoom.SendOrder('지정가매수', '0101', accountNumber, 1, code, amount, price, '03', '')

    # 종목 매도 (in_strAccount, in_strCode, out_result)
    def sell_Stock(self, code, amount, price, accountNumber):
        print("@@ 주식매도")
        self.kiwoom.SendOrder('지정가매수', '0101', accountNumber, 2, code, amount, price, '03', '')

    # 코드리스트 필터링

    def receive_trdata(self, screen_no, rqname, trcode, recordname, sPrevNext, data_len, err_code, msg1, msg2):

        # 키움 API 는 요청, 수신으로 진행되기 때문에, 각 함수에 ret 값을 넣기가 어려움. 그래서 각 요청에 대한 수신값을 global 변수에 넣어서 저장해주고, 이것을 main 에서 사용
        global account_stock_dict
        global deposit
        global out_deposit
        global total_asset
        global stocksCnt
        global avail_deposit
        global estimated_balance

        print("요청이름 : " + rqname)

        # 예수금
        if rqname == "opw00001_req":
            print("rqName = opw00001_req")
            self.deposit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0,
                                                   "예수금")
            self.deposit = int(self.deposit)
            deposit = self.deposit

            self.out_deposit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0,
                                                       "출금가능금액")
            self.out_deposit = int(self.out_deposit)
            out_deposit = self.out_deposit


            self.avail_deposit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0,
                                                       "주문가능금액")
            self.avail_deposit = int(self.avail_deposit)
            avail_deposit = self.avail_deposit


            self.opw00001_req_loop.exit()

            print('deposit : {0}, out_deposit : {1}, avail_deposit : {2}'.format(deposit, out_deposit, avail_deposit))

        # 총매입금액
        if rqname == "opw00018_req":
            # print("rqName = opw00018_req")
            total_buy_money = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode, rqname, 0,
                                                      "총매입금액")
            self.total_buy_money = int(total_buy_money)

            self.estimated_balance = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0,
                                                         "총평가금액")
            estimated_balance = self.estimated_balance

            # 보유 종목 가져오기
            rows = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
            stocksCnt = rows
            # 계좌가 보유중인 종목의 갯수를 카운트해준다.
            print("보유종목수 : {0}".format(rows))

            if rows == 0:
                account_stock_dict = {}
                self.detail_account_mystock_loop.exit()

            for i in range(rows):
                code = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                               trcode, rqname, i, "종목번호")
                code = code.strip()[1:]
                code_nm = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                  trcode, rqname, i, "종목명")
                stock_quantity = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                         trcode, rqname, i, "보유수량")
                buy_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                    trcode, rqname, i, "매입가")  # 매입가 평균
                learn_rate = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                     trcode, rqname, i, "수익률(%)")
                current_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                        trcode, rqname, i, "현재가")
                total_chegual_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                              trcode, rqname, i, "매입금액")
                possible_quantity = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                            trcode, rqname, i, "매매가능수량")
                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict[code] = {}
                code_nm = code_nm.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                learn_rate = float(learn_rate.strip())
                current_price = int(current_price.strip())
                total_chegual_price = int(total_chegual_price.strip())
                possible_quantity = int(possible_quantity.strip())

                self.account_stock_dict[code].update({"종목명": code_nm})
                self.account_stock_dict[code].update({"보유수량": stock_quantity})
                self.account_stock_dict[code].update({"매입가": buy_price})
                self.account_stock_dict[code].update({"수익률(%)": learn_rate})
                self.account_stock_dict[code].update({"현재가": current_price})
                self.account_stock_dict[code].update({"매입금액": total_chegual_price})
                self.account_stock_dict[code].update({'매매가능수량': possible_quantity})

                account_stock_dict = self.account_stock_dict

                print("종목코드: %s - 종목명: %s - 보유수량: %s - 매입가:%s - 수익률: %s - 현재가: %s" % (
                    code, code_nm, stock_quantity, buy_price, learn_rate, current_price))
                # print(self.account_stock_dict.get('005930')['종목명']), # 가져올때
                #                print("sPrevNext : %s" % sPrevNext)
                #                print("계좌에 가지고 있는 종목은 %s " % rows)
                if sPrevNext == "2":
                    print(values.account_num)
                    self.detail_account_mystock_loop.exit()
                    self.detail_account_mystock(values.account_num, sPrevNext="2")
                else:
                    self.detail_account_mystock_loop.exit()

        if rqname == "opt10086_pre_req":
            self.preStart = self.kiwoom.dynamicCAll("CommGetData(QString, QString, QString, int, QString)",
                                                    trcode, "",
                                                    rqname, 0, "시가")
            self.preHigh = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                                                   trcode, "",
                                                   rqname, 0, "고가")
            self.preLow = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                                                  trcode, "",
                                                  rqname, 0, "저가")
            self.preEnd = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                                                  trcode, "",
                                                  rqname, 0, "종가")
            self.preDay = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                                                  trcode, "",
                                                  rqname, 0, "전일비")
            self.preUpDown = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)",
                                                     trcode, "",
                                                     rqname, 0, "등락률")
            # self.opt10086_pre_req_loop.exit()
            print("opt10086_pre_req 끝")

        if rqname == "opw00003_req":
            print("rqName = opw00003_req")
            self.total_asset = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "추정예탁자산")

            print(self.total_asset)
            self.total_asset = int(self.total_asset)
            total_asset = self.total_asset

            print("opw00003_req 끝")
            self.opw00003_req_loop.exit()



    def get_account_info(self):
        print("get_account_info 시작")
        account_list = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        self.account_list = account_list
        return account_list

    def detail_account_mystock(self, account, sPrevNext="0"):
        self.detail_account_mystock_loop = QEventLoop()
        print("detail_account_mystock 시작")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "구분")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00018_req", "opw00018", sPrevNext,
                                "0111")
        # CommRqData
        self.detail_account_mystock_loop.exec()
        print("detail_account_mystock 종료")

    def get_deposit(self, account, sPrevNext="0"):

        self.opw00001_req_loop = QEventLoop()

        print("get_deposit 시작")

        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "구분")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        # self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00001_req", "opw00001", sPrevNext, "0112")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00001_req", "opw00001", sPrevNext,
                                "0112")

        self.opw00001_req_loop.exec_()

    def get_total_asset(self, account, sPrevNext="0"):

        self.opw00003_req_loop =QEventLoop()
        print("get_total_asset 시작")

        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "상장폐지조회구분", "1")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00003_req", "opw00003", sPrevNext,
                                "0113")

        self.opw00003_req_loop.exec_()



if __name__ == "__main__":
    try:
        dfSellResult = pd.DataFrame(columns=['code', 'buyPrice', 'amount', 'sell'])
        dfBuyResult = pd.DataFrame(columns=['code', 'buyPrice', 'amount'])
        lineMessege = ""

        # 변수 클래스 저장
        values = Values()

        # 구글 드라이브 에서 마스터 파일 다운로드
        # gdd.GoogleDriveDownload('1efNPLvql1k2J4hrqO7EjJMDQiALhBiFJ', 'Master.xlsx')

        # Load json file, key와 value 형태로 저장
        config_filePath = "config.json"
        isConfigFile = os.path.isfile(config_filePath)
        if isConfigFile:
            with open(config_filePath, 'rt', encoding='UTF8') as json_file:
                config = json.load(json_file)
        else:
            print("config 파일 미존재")

        # 변수저장
        amount = config["order_price"]  # 주문 총 금액
        account_num = config["account_num"]  # 계좌번호
        values.account_num = account_num
        buyFlag = config["buy_flag"]
        buyRate = config["buy_rate"]
        sellRate = config["sell_rate"]
        stopLoss = config["stop_loss"]
        masterFilePath = config["masterFilePath"]

        useTradeAlgorithm = False

        df_targetCodesInfo = pd.DataFrame([])
        BizError = ""

        buyCodes = []

        app = QApplication(sys.argv)
        myWindow = MyWindow()

        myWindow.show()
        # 키움 로그인
        myWindow.kiwoom_login()

        # 계좌정보 가져오기 (계좌)
        print('계좌정보 : {0}'.format(myWindow.get_account_info()))
        if not account_num in myWindow.get_account_info():
            print("config 입력 계좌번호 미존재")

        # 예수금 가져오기
        myWindow.get_deposit(account_num)
        print("예수금 : {0}, 출금가능금액 : {1}, 주문가능금액 : {2}".format(deposit, out_deposit, avail_deposit))

        # "code" 열에 종목 코드 존재
        dfBuyList = pd.read_json(masterFilePath)

        # print(dfBuyList)

        myWindow.detail_account_mystock(account_num,
                                        0)  # ret = account_stock_dict[code] = {'종목명', '보유수량, '매입가, '수익률(%), '현재가, '매입금액, '매매가능수량'}

        # print(account_stock_dict)

        while (True):
            if datetime.datetime.now().hour >= 16 or datetime.datetime.now().hour <= 8:
                print(datetime.datetime.now().hour)
                break

            # 매도 진행, 계좌의 보유종목 조회
            myWindow.detail_account_mystock(account_num,0)  # ret = account_stock_dict[code] = {'종목명', '보유수량, '매입가, '수익률(%), '현재가, '매입금액, '매매가능수량'}

            if stocksCnt > 20:
                buyFlag = False

            # 매도 ::: 보유종목 있을시, 매도진행
            if len(account_stock_dict) > 0:
                for i in account_stock_dict:
                    try:
                        code = i
                        buy_price = int(account_stock_dict[i]['매입가'])
                        stockAmount = int(account_stock_dict[i]['보유수량'])
                        possibleQuantity = int(account_stock_dict[i]['매매가능수량'])
                        dfStockPrice = dataProcessing.GetStockPrice(code, 10)
                        # dfMinute = dataProcessing.GetStockPriceMinute(code)

                        nowPrice = dfStockPrice.iloc[-1]['종가']

                        print('매도가격 : {0}, 현재가격 : {1}'.format(buy_price * sellRate, nowPrice))

                        # 결과 DF 생성
                        if i not in dfSellResult['code'].values:
                            # 없으면 새로 생성
                            data = {'code': i, 'buyPrice': buy_price, 'amount': stockAmount, 'sell': 'N'}
                            dfSellResult = pd.concat([dfSellResult, pd.DataFrame([data])], ignore_index=True)

                        if buy_price * sellRate > nowPrice and buy_price * stopLoss < nowPrice:  # 체결가가 매입금액의 n% 이상일 때 진행
                            continue

                        if useTradeAlgorithm:  # 거래에 사용되는 알고리즘 있으면 여기서 지정
                            sellPrice = dataProcessing.CheckReturnPosition(dfStockPrice, "up", 3)  # 가격 반전 확인
                        else:
                            sellPrice = nowPrice

                        if sellPrice is None:  # 가격 반전이 나오지 않았을 경우, 다음 code 확인
                            continue

                        if possibleQuantity < 1:  # 매매가능수량이 없을 때, 다음 code 확인
                            continue

                        myWindow.sell_Stock(code, possibleQuantity, sellPrice, account_num)
                        dfSellResult.loc[i == dfSellResult['code'], ['sell']] = "Y"

                        lineMessege = lineMessege + "\n" + "매도 / " + code

                    except Exception as e:
                        BizError += "\n매도 : " + str(e)

            # 예수금 존재할 때만, 매수 시도
            myWindow.get_deposit(account_num)

            # 매수
            if buyFlag:
                for idx, row in dfBuyList.iterrows():
                    try:
                        if avail_deposit < amount:
                            break
                        code = row['code']
                        # dfMinute = dataProcessing.GetStockPriceMinute(code)
                        dfStock = dataProcessing.GetStockPrice(code, 10)
                        print('code : {2}, 매수가격 : {0}, 현재가격 : {1}'.format(int(row['buyPrice']) * buyRate, dfStock.iloc[-1]['종가'], code))
                        if int(dfStock.iloc[-1]['종가']) > int(row['buyPrice']):
                            continue

                        # if useTradeAlgorithm:  # 거래에 사용되는 알고리즘 있으면 여기서 구분
                        #     buyPrice = dataProcessing.CheckReturnPosition(dfMinute, "down", 3)  # 가격 반전 확인
                        # else:
                        #     buyPrice = int(dfStock.loc[0]['종가'])

                        buyPrice = int(dfStock.iloc[-1]['종가'])

                        quantity = amount // buyPrice

                        if buyPrice is None:
                            continue
                        if code in account_stock_dict:  # 보유 종목에 대해서 매수 진행 X
                            continue
                        if code in buyCodes:
                            continue

                        # 매수를 했으면 임시 배열에 넣기
                        buyCodes.append(code)

                        myWindow.buy_Stock(code, quantity, buyPrice, account_num)
                        lineMessege = lineMessege + "\n" + "매수 / " + code

                        # 결과 DF 생성
                        if row['code'] not in dfBuyResult['code'].values:
                            # 없으면 새로 생성
                            data = {'code': row['code'], 'buyPrice': buyPrice, 'amount': quantity}
                            dfBuyResult = pd.concat([dfBuyResult, pd.DataFrame([data])], ignore_index=True)

                    except Exception as e:
                        print('Err : {0}'.format(e))
                        BizError += "\n매수 : " + str(e)

            if datetime.datetime.now().hour > 16:
                break

            excel_collection.saveDFToJson("dfBuyResult.json", dfBuyResult)
            excel_collection.saveDFToJson("dfSellResult.json", dfSellResult)

            print(datetime.datetime.now())
            time.sleep(20)

        print("complete")
        if not BizError == "":
            # dToday = datetime.datetime.now().strftime("%Y-%m-%d")
            # sSubject = dToday + "Error_AutoTrade"
            # sSender = 'yrkim1989@gmail.com'
            # lstReceiver = ['yrkim1989@gmail.com', 'bbodo629@gmail.com']
            # sender_collection.SendEmail(sSubject, {BizError}, {}, sSender, lstReceiver)
            lineMessege += "\n에러발생"
            
        MyWindow.get_total_asset(myWindow, account_num, 0)
        nowDate = datetime.datetime.now().strftime('%Y.%m.%d')
        lineMessege = nowDate + "\n총잔고 : " + str(total_asset) + "\n주문가능금액 : " + str(avail_deposit) + "\n" + lineMessege

        sender_collection.SendLine(lineMessege)

        # 매수, 매도 진행 후 KOSPI 필터링 정보 JSON 파일 저장. process.ValidateStocks.saveSortingCode(saveFilePath) 함수 사용 밑에 넣기

    except Exception as e:
        print(e)
        print("Exception")