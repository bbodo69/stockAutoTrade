import module.dataProcessing as dataProcessing
import pandas as pd
import random
import json

dailyConfirmCode_filePath = "dailyConfirmCode.json"

# read confirmCodeFile
with open(dailyConfirmCode_filePath, 'rt', encoding='UTF8') as json_file:
    codes = json.load(json_file)


# df = pd.DataFrame(columns=['1', '2'])
#
# for i in range(0, 10) :
#     list_row = [1, 2]
#     df.loc[len(df)] = list_row
#
# print(df)
print(len(codes))
if len(codes) > 30 :
    codes = random.sample(codes, 30)
else :
    pass
print(len(codes))

test = [{1:1, 2:2, 3:3, 4:4, 5:5, 6:6}]

# if len(test) > 3 :
#     random.sample(test, 3)
# else :
#     pass
# print(test)
# random.sample(test, 2)