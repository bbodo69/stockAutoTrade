import json
import random
import module.dataProcessing as dataProcessing

p00_05, p05_10, p10_15, p15_20, p20_25, p25_30, p30_35, p35_40, p40_45, p45_50, p50_55, p55_60, p60_65, p65_70, p75_80 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
print(p00_05)
print(p00_05)

dicResult = {}
keys = ["p00_05", "p05_10", "p10_15", "p15_20", "p20_25", "p25_30", "p30_35", "p35_40", "p40_45", "p45_50", "p50_55", "p55_60", "p60_65", "p65_70", "p75_80", "m00_05", "m05_10", "m10_15", "m15_20", "m20_25", "m25_30", "m30_35", "m35_40", "m40_45", "m45_50", "m50_55", "m55_60", "m60_65", "m65_70", "m75_80"]
for i in keys :
    dicResult[i] = 0
print(keys)
lists = dicResult.items()
print(lists)

#x, y = zip(*keys)

try:
    dfCode = dataProcessing.GetStockPrice("005930", 300)
    tmpPrice = 0
    for idx_c, code in dfCode.iterrows():
        if tmpPrice == 0 :
            tmpPrice = code['종가']
            continue
        else :
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

except Exception as e:
    print(e)



