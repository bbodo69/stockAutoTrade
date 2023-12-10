import json
import random

dicTest = {1 : "1", 2 : "2"}

print(dicTest)

if 2 in dicTest :
    print(1)

with open("dailyConfirmCode.json", 'rt', encoding='UTF8') as json_file:
    codes = json.load(json_file)

print(type(codes))

print(random.sample(codes,50))