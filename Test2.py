import module.dataProcessing as dataProcessing

dfStock = dataProcessing.GetStockPrice("001530", 20)

print(dfStock)