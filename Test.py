import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import QEventLoop, QSize
import time
import pandas as pd
import datetime
import module.dataProcessing as dataProcessing
import module.GoogleDriveDownload as gdd
import module.excel_collection as excel_ceollection
import module.LoadConfig as LoadConfig
# import module.sender_collection as sender_collection
import json
import os

class MyWindow(QMainWindow):
    # QMainWindow 를 상속
    delay = 3.6

    def __init__(self):  # 기본값 설정

        ####### 계좌 관련 변수
        self.deposit = 0
        self.out_deposit = 0
        self.account_num = None
        self.use_money = 0
        self.use_money_percent = 0
        self.account_list = []
        self.account_stock_dict = {}  # 보유종목

        super().__init__()

        # 종료 메세지 출력
        self.setMinimumSize(QSize(500, 100))
        self.setWindowTitle("Alert Message")

        pybutton = QPushButton('버튼 눌러야 컴퓨터 계속 사용 가능', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(400, 30)
        pybutton.move(50, 35)

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
        global stocksCnt

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

            self.opw00001_req_loop.exit()

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
                    self.detail_account_mystock(sPrevNext="2")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()

    myWindow.show()
    # 키움 로그인
    myWindow.kiwoom_login()
    print('계좌정보 : {0}'.format(myWindow.get_account_info()))
    myWindow.get_deposit("8065202611")
    print("예수금 : {0}, 출금가능금액 : {1}".format(deposit, out_deposit))

    # myWindow.buy_Stock("005930", 1, 72000, "8065202611")

    myWindow.detail_account_mystock(8065202611,
                                             0)  # ret = account_stock_dict[code] = {'종목명', '보유수량, '매입가, '수익률(%), '현재가, '매입금액, '매매가능수량'}
    time.sleep(20000)

    for i in account_stock_dict :
        print(account_stock_dict[i])


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
    #     dfBuyList = pd.read_json(masterFilePath)
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
    #             for idx, row in dfBuyList.iterrows():
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