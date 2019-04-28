import csv
import math
from operator import itemgetter
import re

def findSD(start, end, listDates, mean, rows):
    sd = 0.0
    v = 0.0
    total = end - start + 1
    while (start <= end):
        v = float(mean - float(rows[listDates[start]][2]))
        v  = v *v
        sd = sd + v
        start = start + 1

    sd = sd / (total)
    sd = math.sqrt(sd)
    return sd

def findMean(start, end, listDates, rows):
    mean = 0.0
    total  = end - start + 1
    while (start <= end):
        mean = mean + float(rows[listDates[start]][2])
        start = start + 1

    mean = mean/(total)
    return mean

def findProfit(start, end, listDates, rows):
    share = float(rows[listDates[start]][2])
    max_profit = 0
    startDate = rows[listDates[start]][1]
    endDate = rows[listDates[start]][1]
    tempStartDate = rows[listDates[start]][1]
    start = start+1;
    while start <= end:
        if int(rows[listDates[start]][2]) > share:
            if int(rows[listDates[start]][2]) - share > max_profit:
                max_profit = int(rows[listDates[start]][2]) - share
                endDate = rows[listDates[start]][1]
                startDate = tempStartDate
            else:
                share = int(rows[listDates[start]][2])
                tempStartDate = rows[listDates[start]][1]
        start = start + 1
        
    print("Buy Date %s \n", startDate)
    print("Sell Date %s \n", endDate)
    print("Profit : Rs {} \n".format(max_profit * 100))

def evaluateShares(start, end, stock, stock_dist, rows):
    listDates = stock_dist[stock]
    s  = -1
    e = -1
    
    for i in range(0, len(listDates)):
        if start <= rows[listDates[i]][1]:
            s = i
            break
        
    for i in range(len(listDates)- 1, -1, -1):
        if end >= rows[listDates[i]][1]:
            e = i
            break
        
    if (s == -1 or e == -1):
        print("Date entered by you are out of range")
        return
    
    print("Here is you result :- \n")
    mean  = findMean(s, e, listDates, rows)
    print("Mean - {} \n".format(mean))
    sd = findSD(s, e, listDates, mean, rows)
    print("Std :- {} \n".format(sd))

    findProfit(s, e,listDates, rows)
    
def closetString(str1, str2, m, n):  
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
            if i == 0: 
                dp[i][j] = j
            elif j == 0: 
                dp[i][j] = i
                
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
           
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        
                                   dp[i-1][j],       
                                   dp[i-1][j-1])
    return dp[m][n]

def getDict(j, rows):
    stock_dict = dict()
    for i in range(0, len(rows)):
        if rows[i][j] not in stock_dict.keys():
            stock_dict[rows[i][j]] = []
            
    for i in range(0, len(rows)):
        stock_dict[rows[i][j]].append(i)

    return stock_dict

def main():
    filename = "abc.csv"

    fields = [] 
    rows = [] 
    with open(filename, 'r') as csvfile: 
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        k = 0
        for row in csvreader: 
            rows.append(row)
            if rows[k][2] =="":
                rows[k][2] = rows[k-1][2]
            k = k + 1

        rows.sort(key=itemgetter(1))
        stock_dict = dict()
        stock_dict = getDict(0, rows)
        print(stock_dict)

    while (1):
        val = input("Welcome Agent! Which stock you need to process?:-") 
        print(val)
        minValues = []
        flag = 0
        stockName = ""
        for key in stock_dict.keys():
            if key == val:
                flag = 1
                stockName == val
                break;
            
        if flag == 0:
            for key in stock_dict.keys():
                print(key)
                m = closetString(key, val, len(key), len(val))
                minValues.append(m)

            dist = min(minValues)

            i = 0;
            for key in stock_dict.keys():
                if minValues[i] == dist:
                    print("Oops! Do you mean %s y or n :", key)
                    value = input()
                    if value == "y":
                        stockName = key
                        break
                i = i +1
                    


        if stockName == "":
            print("Sorry there are not any stock matching our preference")
            more = input("Do you want to continue? (y or n)")
            if more != "y":
                break
            else:
                continue
        
        startDate  = input("From which date you want to start:-")
        endDate    = input( "Till which date you want to analyze :-")

        if (startDate > endDate):
            print("You entered wrong Dates endDate cannot be smaller than StartDate")
            more = input("Do you want to continue? (y or n)")
            
            if more != "y":
                break
            else:
                continue
            
        elif(not re.search("^\d{4}[-](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d\d$",startDate)):
            print("Plese Enter Startdate in format YYYY-Mon-DD")
            more = input("Do you want to continue? (y or n)")
            if more != "y":
                break
            else:
                continue
            
        elif(not re.search("^\d{4}[-](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[-]\d\d$",endDate)):
            print("Plese Enter Enddate in format YYYY-Mon-DD")
            more = input("Do you want to continue? (y or n)")
            if more != "y":
                break
            else:
                continue
                  
        else:
            evaluateShares(startDate, endDate, stockName, stock_dict, rows)

        more = input("Do you want to continue? (y or n)")

        if more != "y":
            break

if __name__== "__main__":
    print("HELLO")
    main()
