import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop, QSize
import time
import pandas as pd
import datetime
import module.Common as Common
import module.dataProcessing as dataProcessing
import module.GoogleDriveDownload as gdd
import module.excel_collection as excel_ceollection
import module.LoadConfig as LoadConfig
# import module.sender_collection as sender_collection
import json
import os
import random

class MyWindow(QMainWindow):
    # QMainWindow 를 상속
    delay = 3.6

    def __init__(self):  # 기본값 설정

        ####### 계좌 관련 변수
        self.deposit = 0
        self.out_deposit = 0
        self.account_num = "8065202611"
        self.use_money = 0
        self.use_money_percent = 0
        self.account_list = []
        self.account_stock_dict = {}  # 보유종목
        self.not_signed_account_dict = {}

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

        # loop 생성
        self.tr_event_loop = QEventLoop()

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

        try :
            # 키움 API 는 요청, 수신으로 진행되기 때문에, 각 함수에 ret 값을 넣기가 어려움. 그래서 각 요청에 대한 수신값을 global 변수에 넣어서 저장해주고, 이것을 main 에서 사용
            global account_stock_dict
            global deposit
            global out_deposit
            global stocksCnt
            global not_signed_account_dict
    
            print("요청이름 : " + rqname)
    
            # 미체결
            if rqname == "opt10075_req" :
                print("rqName = opt10075_req")
                stock_code = {}
                cnt = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
    
                for i in range(cnt):
                    stock_code = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종목코드")
                    stock_code = stock_code.strip()
    
                    stock_order_number = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문번호")
                    stock_order_number = int(stock_order_number)
    
                    stock_name = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "종목명")
                    stock_name = stock_name.strip()
    
                    stock_order_type = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문구분")
                    stock_order_type = stock_order_type.strip().lstrip('+').lstrip('-')
    
                    stock_order_price = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문가격")
                    stock_order_price = int(stock_order_price)
    
                    stock_order_quantity = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문수량")
                    stock_order_quantity = int(stock_order_quantity)
    
                    stock_not_signed_quantity = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "미체결수량")
                    stock_not_signed_quantity = int(stock_not_signed_quantity)
    
                    stock_signed_quantity = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "체결량")
                    stock_signed_quantity = int(stock_signed_quantity)
    
                    stock_present_price = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "현재가")
                    stock_present_price = int(
                        stock_present_price.strip().lstrip('+').lstrip('-'))
    
                    stock_order_status = self.kiwoom.dynamicCall(
                        "GetCommData(QString, QString, int, QString)", trcode, rqname, i, "주문상태")
                    stock_order_status = stock_order_status.strip()
    
                    if not stock_code in self.not_signed_account_dict:
                        self.not_signed_account_dict[stock_code] = {}
    
                    self.not_signed_account_dict[stock_code].update(
                        {'종목명': stock_name})
                    self.not_signed_account_dict[stock_code].update(
                        {'주문구분': stock_order_type})
                    self.not_signed_account_dict[stock_code].update(
                        {'주문가격': stock_order_price})
                    self.not_signed_account_dict[stock_code].update(
                        {'주문수량': stock_order_quantity})
                    self.not_signed_account_dict[stock_code].update(
                        {'미체결수량': stock_not_signed_quantity})
                    self.not_signed_account_dict[stock_code].update(
                        {'체결량': stock_signed_quantity})
                    self.not_signed_account_dict[stock_code].update(
                        {'현재가': stock_present_price})
                    self.not_signed_account_dict[stock_code].update(
                        {'주문상태': stock_order_status})
    
                not_signed_account_dict = self.not_signed_account_dict
                
                if sPrevNext == "2":
                    self.not_signed_account(2)
                else:
                    # self.opt10075_req_loop.exit()
                    self.tr_event_loop.exit()
                
    
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
    
                # self.opw00001_req_loop.exit()
                self.tr_event_loop.exit()
    
                print('deposit : {0}, out_deposit : {1}'.format(deposit, out_deposit))
    
            # 총매입금액
            if rqname == "opw00018_req":
                # print("rqName = opw00018_req")
                total_buy_money = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode, rqname, 0,
                                                          "총매입금액")
                self.total_buy_money = int(total_buy_money)
                # 보유 종목 가져오기
                rows = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
                stocksCnt = rows
                # 계좌가 보유중인 종목의 갯수를 카운트해준다.
                print("보유종목수 : {0}".format(rows))
    
                if rows == 0:
                    account_stock_dict = {}
                    # self.detail_account_mystock_loop.exit()
                    self.tr_event_loop.exit()
    
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
                        continue
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
    
                    print("종목코드: %s - 종목명: %s - 보유수량: %s - 매입가:%s - 수익률: %s - 현재가: %s" % (
                        code, code_nm, stock_quantity, buy_price, learn_rate, current_price))
                    # print(self.account_stock_dict.get('005930')['종목명']), # 가져올때
                    #                print("sPrevNext : %s" % sPrevNext)
                    #                print("계좌에 가지고 있는 종목은 %s " % rows)
    
                    account_stock_dict = self.account_stock_dict
                    ''' # 2 페이지 넘어갈때 처리 필요. 
                    if sPrevNext == "2":
                        self.detail_account_mystock(self.account_num, sPrevNext="2")
                    else:
                        self.cancel_screen_number("0111")
                        self.detail_account_mystock_loop.exit()
                    '''
                    # self.cancel_screen_number("0111")
                    # self.detail_account_mystock_loop.exit()
                    self.tr_event_loop.exit()
        except Exception as e :
            print("{0} Err _ {1}".format(rqname, e))
            


                    
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
            self.tr_event_loop.exit()
            # self.opt10086_pre_req_loop.exit()
            print("opt10086_pre_req 끝")

    def get_account_info(self):
        print("get_account_info 시작")
        account_list = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        self.account_list = account_list
        return account_list

    def detail_account_mystock(self, account, sPrevNext="0"):
        self.detail_account_mystock_loop = QEventLoop()
        print("sPrevNest = {0}, isRunningLoop = {1}".format(sPrevNext, self.detail_account_mystock_loop.isRunning()))
        print("detail_account_mystock 시작")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "구분")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00018_req", "opw00018", sPrevNext,
                                "0111")

        # if not self.detail_account_mystock_loop.isRunning():
        #     self.detail_account_mystock_loop.exec_()
        if not self.tr_event_loop.isRunning():
            self.tr_event_loop.exec_()
        print("detail_account_mystock 종료")

    def get_deposit(self, account, pw, sPrevNext="0"):

        self.opw00001_req_loop = QEventLoop()

        print("get_deposit 시작")

        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", pw)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "구분")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        # self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00001_req", "opw00001", sPrevNext, "0112")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opw00001_req", "opw00001", sPrevNext,
                                "0112")

        # self.opw00001_req_loop.exec_()
        if not self.tr_event_loop.isRunning():
            self.tr_event_loop.exec_()

    # 미체결 확인 함수, https://steady-coding.tistory.com/335 참고
    def not_signed_account(self, account, nPrevNext="0"):

        # self.opt10075_req_loop = QEventLoop()
        print("not_signed_account 시작")

        self.kiwoom.dynamicCall("SetInputValue(QString, QString)",
                         "계좌번호", account)
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "전체종목구분", "0")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "opt10075_req", "opt10075", nPrevNext, "0113")

        # if not self.opt10075_req_loop.isRunning():
        #     self.opt10075_req_loop.exec_()
        if not self.tr_event_loop.isRunning():
            self.tr_event_loop.exec_()

    def cancel_screen_number(self, screen_no):
        self.dynamicCall("DisconnectRealData(QString)", screen_no)


if __name__ == "__main__":
    # read Config data
    config_filePath = "config.json"
    dailyConfirmCode_filePath = "dailyConfirmCode.json"
    isConfigFile = os.path.isfile(config_filePath)

    if isConfigFile:
        with open(config_filePath, 'rt', encoding='UTF8') as json_file:
            config = json.load(json_file)
    else:
        print("config 파일 미존재")

    # read confirmCodeFile
    with open(dailyConfirmCode_filePath, 'rt', encoding='UTF8') as json_file:
        codes = json.load(json_file)

    # for row in codes :
    #     print(row['code'])

    # save basic values
    amount = config["order_price"]  # 주문 총 금액
    account_num = config["account_num"]  # 계좌번호
    buyFlag = config["buy_flag"]
    buyRate = float(config["buy_rate"])
    sellRate = float(config["sell_rate"])
    stopLoss = float(config["stop_loss"])
    pw = "0000"

    # start kiwoom API
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()

    # 키움 로그인
    myWindow.kiwoom_login()
    # print('계좌정보 : {0}'.format(myWindow.get_account_info())) # 보유 계좌 정보 불러오기
    myWindow.get_deposit(account_num, pw) # 예수금, 출금가능금액 가져오기, ret = deposit(예수금), out_deposit(출금가능금액)
    # print("예수금 : {0}, 출금가능금액 : {1}".format(deposit, out_deposit))
    # myWindow.detail_account_mystock(account_num, 0)  # ret = account_stock_dict[code] = {'종목명', '보유수량, '매입가, '수익률(%), '현재가, '매입금액, '매매가능수량'}

    while (True):
        if datetime.datetime.now().hour >= 16:
            print(datetime.datetime.now().hour)
            break
    
        # 매도 진행, 계좌의 보유종목 조회
        myWindow.detail_account_mystock(account_num,
                                        0)  # ret = account_stock_dict[code] = {'종목명', '보유수량, '매입가, '수익률(%), '현재가, '매입금액, '매매가능수량'}
        # 미체결 조회
        myWindow.not_signed_account(account_num,
                                        0)
    
        if stocksCnt > 50:
            messageInfo = '보유종목 갯수 : {0}'.format(stocksCnt)
            Common.SendLine(messageInfo)
            buyFlag = False
    
        # 매도 ::: 보유종목 있을시, 매도진행
        if len(account_stock_dict) > 0:
            for i in account_stock_dict:
                try:
                    code = i
                    buy_price = int(account_stock_dict[i]['매입가'])
                    stockAmount = int(account_stock_dict[i]['보유수량'])
                    possibleQuantity = int(account_stock_dict[i]['매매가능수량'])
                    dfMinute = dataProcessing.GetStockPriceMinute(code)
                    print('매도가격 : {0}, 현재가격 : {1}'.format(buy_price * sellRate, dfMinute.loc[0]['체결가']))
    
                    if buy_price * sellRate > dfMinute.loc[0]['체결가']:  # 체결가가 매입금액의 n% 이상일 때 진행
                        continue
                    # if useTradeAlgorithm:  # 거래에 사용되는 알고리즘 있으면 여기서 지정
                    #     sellPrice = dataProcessing.CheckReturnPosition(dfMinute, "up", 3)  # 가격 반전 확인
                    # else:
                    #    sellPrice = int(dfMinute.loc[0]['체결가'])
                    sellPrice = int(dfMinute.loc[0]['체결가'])
                    if sellPrice is None:  # 가격 반전이 나오지 않았을 경우, 다음 code 확인
                        continue
                    if possibleQuantity < 1:  # 매매가능수량이 없을 때, 다음 code 확인
                        continue
                    myWindow.sell_Stock(code, possibleQuantity, sellPrice, account_num)
                    time.sleep(0.3)
                    # 라인 보내기
                    messageInfo = '\n총 종목코드 : {0}\n총 수량 : {1}\n총 매도가 : {2}'.format(code, possibleQuantity, sellPrice)
                    Common.SendLine(messageInfo)
                    
                except Exception as e:
                    # BizError += "\n매도 : " + str(e)
                    # 라인 보내기
                    messageInfo = '매도 Err : {0}'.format(e)
                    Common.SendLine(messageInfo)
    
        # 예수금 존재할 때만, 매수 시도
        myWindow.get_deposit(account_num, pw)

        # 매수

        if buyFlag:
            for row in codes:
                try:
                    codes = random.sample(codes, 30) # 코스피 중 n개 샘플 먼저 진행
                    if out_deposit < amount:
                        break
                    code = row['code']
                    # dfMinute = dataProcessing.GetStockPriceMinute(code)
                    dfStock = dataProcessing.GetStockPrice(code, 20)
                    print('매수가격 : {0}, 현재가격 : {1}'.format(int(int(dfStock.loc[0]['시가']) * buyRate),
                                                          dfStock.loc[0]['종가']))
                    
                    if int(dfStock.loc[0]['종가']) > int(int(dfStock.loc[0]['시가']) * buyRate):
                        continue
    
                    # if useTradeAlgorithm:  # 거래에 사용되는 알고리즘 있으면 여기서 구분
                    #     buyPrice = dataProcessing.CheckReturnPosition(dfMinute, "down", 3)  # 가격 반전 확인
                    # else:
                    #     buyPrice = int(dfStock.loc[0]['종가'])
                    buyPrice = int(dfStock.loc[0]['종가'])
                    
                    quantity = amount // buyPrice
    
                    if buyPrice is None:
                        continue

                    if code in account_stock_dict or code in not_signed_account_dict:  # 보유 종목, 미체결 종목에 대해서 매수 진행 X
                        continue

                    tmpOut_deposit = out_deposit
                    myWindow.buy_Stock(code, quantity, buyPrice, account_num)
                    time.sleep(0.3)
                    # 예수금 존재할 때만, 매수 시도
                    myWindow.get_deposit(account_num, pw)
                    if tmpOut_deposit == out_deposit:
                        # 라인 보내기
                        messageInfo = '\n실패\n종목코드 : {0}\n총 수량 : {1}\n매수가 : {2}\n예수금 : {3}'.format(code, quantity, buyPrice, out_deposit)
                        Common.SendLine(messageInfo)
                        continue
                    # 라인 보내기
                    messageInfo = '\n종목코드 : {0}\n총 수량 : {1}\n매수가 : {2}\n예수금 : {3}'.format(code, quantity, buyPrice, out_deposit)
                    
                    Common.SendLine(messageInfo)
                    
                except Exception as e:
                    print('매수 Err : {0}'.format(e))
                    # BizError += "\n매수 : " + str(e)

                    # 라인 보내기
                    messageInfo = '매수 Err : {0}'.format(e)
                    Common.SendLine(messageInfo)

        time.sleep(20)
        if datetime.datetime.now().hour > 20:
            break

    # try:
    #     app = QApplication(sys.argv)
    #     myWindow = MyWindow()
    #
    #     myWindow.show()
    #     # 키움 로그인
    #     myWindow.kiwoom_login()

    #     # Load json file, key와 value 형태로 저장
    #     config_filePath = "config.json"
    #     isConfigFile = os.path.isfile(config_filePath)
    #     if isConfigFile:
    #         with open(config_filePath, 'rt', encoding='UTF8') as json_file:
    #             config = json.load(json_file)
    #     else:
    #         print("config 파일 미존재")
    #
    #     # 변수저장
    #     amount = config["order_price"]  # 주문 총 금액
    #     account_num = config["account_num"]  # 계좌번호
    #     buyFlag = config["buy_flag"]
    #     buyRate = config["buy_rate"]
    #     sellRate = config["sell_rate"]
    #     stopLoss = config["stop_loss"]
    #     masterFilePath = config["masterFilePath"]
    #
    #     useTradeAlgorithm = False
    #
    #     df_targetCodesInfo = pd.DataFrame([])
    #     BizError = ""
    #
    #     myWindow.show()
    #     # 키움 로그인
    #     myWindow.kiwoom_login()
    #
    #     # 계좌정보 가져오기 (계좌)
    #     print('계좌정보 : {0}'.format(myWindow.get_account_info()))
    #     if not account_num in myWindow.get_account_info():
    #         print("config 입력 계좌번호 미존재")
    #
    #     # 예수금 가져오기
    #     myWindow.get_deposit(account_num)
    #     print("예수금 : {0}, 출금가능금액 : {1}".format(deposit, out_deposit))
    #
    #     # "code" 열에 종목 코드 존재
    #     # dfBuyList = pd.read_json(masterFilePath)
    #


    #     while (True):
    #         if datetime.datetime.now().hour >= 16:
    #             print(datetime.datetime.now().hour)
    #             break
    #
    #         # 매도 진행, 계좌의 보유종목 조회
    #         myWindow.detail_account_mystock(account_num,
    #                                         0)  # ret = account_stock_dict[code] = {'종목명', '보유수량, '매입가, '수익률(%), '현재가, '매입금액, '매매가능수량'}
    #
    #         if stocksCnt > 20:
    #             buyFlag = False
    #
    #         # 매도 ::: 보유종목 있을시, 매도진행
    #         if len(account_stock_dict) > 0:
    #             for i in account_stock_dict:
    #                 try:
    #                     code = i
    #                     buy_price = int(account_stock_dict[i]['매입가'])
    #                     stockAmount = int(account_stock_dict[i]['보유수량'])
    #                     possibleQuantity = int(account_stock_dict[i]['매매가능수량'])
    #                     dfMinute = dataProcessing.GetStockPriceMinute(code)
    #
    #                     print('매도가격 : {0}, 현재가격 : {1}'.format(buy_price * sellRate, dfMinute.loc[0]['체결가']))
    #
    #                     if buy_price * sellRate > dfMinute.loc[0]['체결가']:  # 체결가가 매입금액의 n% 이상일 때 진행
    #                         continue
    #
    #                     if useTradeAlgorithm:  # 거래에 사용되는 알고리즘 있으면 여기서 지정
    #                         sellPrice = dataProcessing.CheckReturnPosition(dfMinute, "up", 3)  # 가격 반전 확인
    #                     else:
    #                         sellPrice = int(dfMinute.loc[0]['체결가'])
    #
    #                     if sellPrice is None:  # 가격 반전이 나오지 않았을 경우, 다음 code 확인
    #                         continue
    #
    #                     if possibleQuantity < 1:  # 매매가능수량이 없을 때, 다음 code 확인
    #                         continue
    #
    #                     myWindow.sell_Stock(code, possibleQuantity, sellPrice, account_num)
    #                 except Exception as e:
    #                     BizError += "\n매도 : " + str(e)
    #
    #         # 예수금 존재할 때만, 매수 시도
    #         myWindow.get_deposit(account_num)
    #
    #         # 매수
    #         if buyFlag:
    #             for row in codes:
    #                 try:
    #                     if deposit < amount:
    #                         break
    #                     code = row['code']
    #                     # dfMinute = dataProcessing.GetStockPriceMinute(code)
    #                     dfStock = dataProcessing.GetStockPrice(code)
    #                     print('code : {0}'.format(code))
    #                     print('매수가격 : {0}, 현재가격 : {1}'.format(int(int(dfStock.loc[0]['시가']) * buyRate),
    #                                                           dfStock.loc[0]['종가']))
    #
    #                     if int(dfStock.loc[0]['종가']) > int(int(dfStock.loc[0]['시가']) * buyRate):
    #                         continue
    #
    #                     if useTradeAlgorithm:  # 거래에 사용되는 알고리즘 있으면 여기서 구분
    #                         buyPrice = dataProcessing.CheckReturnPosition(dfMinute, "down", 3)  # 가격 반전 확인
    #                     else:
    #                         buyPrice = int(dfStock.loc[0]['종가'])
    #
    #                     quantity = amount // buyPrice
    #
    #                     if buyPrice is None:
    #                         continue
    #                     if code in account_stock_dict:  # 보유 종목에 대해서 매수 진행 X
    #                         continue
    #                     myWindow.buy_Stock(code, quantity, buyPrice, account_num)
    #                 except Exception as e:
    #                     print('Err : {0}'.format(e))
    #                     BizError += "\n매수 : " + str(e)
    #
    #         if datetime.datetime.now().hour > 16:
    #             break
    #
    #         time.sleep(20)
    #
    #     if not BizError == "":
    #         dToday = datetime.now().strftime("%Y-%m-%d")
    #         sSubject = dToday + "Error_AutoTrade"
    #         sSender = 'yrkim1989@gmail.com'
    #         lstReceiver = ['yrkim1989@gmail.com', 'bbodo629@gmail.com']
    #
    #         sender_collection.SendEmail(sSubject, {BizError}, {}, sSender, lstReceiver)
    #     print("complete")
    #
    #     # 매수, 매도 진행 후 KOSPI 필터링 정보 JSON 파일 저장. process.ValidateStocks.saveSortingCode(saveFilePath) 함수 사용 밑에 넣기
    #
    # except Exception as e:
    #     # if datetime.datetime.now().hour < 16:
    #     #     os.system("shutdown -s -t 60")
    #     print(e)
    #     print("Exception")
    #
    # # app.exec_()
    #
