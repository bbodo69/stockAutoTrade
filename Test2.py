class test() :
     def __init__(self): # 기본값 설정
        ####### 계좌 관련 변수
        self.deposit = 0
        self.out_deposit = 0
        self.account_num = account_num
        self.use_money = 0
        self.use_money_percent = 0
        self.account_list = []
        self.account_stock_dict = {}    # 보유종목

t = test()
t.deposit = 10

print(t.deposit)
