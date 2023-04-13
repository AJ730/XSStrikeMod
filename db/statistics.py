import re
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import warnings
import seaborn as sns

warnings.filterwarnings("ignore")

print("")
print("")

conn = sqlite3.connect("output.db")
c = conn.cursor()
c.execute("SELECT COUNT(Distinct webpage) FROM 'vulnerability'")
distinctCount = int(c.fetchone()[0])
print("the amount of distinct webpages in the DB with outputs is: ", distinctCount)

c.execute("SELECT COUNT(webpage) FROM 'vulnerability' ")
totalCount = int(c.fetchone()[0])
print("the total amount of webpages in the DB with is: ", totalCount)

c.execute("SELECT Distinct status FROM 'vulnerability'")
statuslist = list(map(lambda x: x[0], c.fetchall()))
print("all different statusses: " + str(statuslist))

print("")

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'No Change'")
noChangeCount = c.fetchone()[0]
print("amount of time 'No Change' was encountered: " + str(noChangeCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Not Crawled'")
notCrawledCount = c.fetchone()[0]
print("amount of time 'Not Crawled' was encountered: " + str(notCrawledCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Server Error'")
serverErrorCount = c.fetchone()[0]
print("amount of time 'Server Error' was encountered: " + str(serverErrorCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Maybe Blocked'")
maybeBlockedCount = c.fetchone()[0]
print("amount of time 'Maybe Blocked' was encountered: " + str(maybeBlockedCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Blocked'")
BlockedCount = c.fetchone()[0]
print("amount of time 'Blocked' was encountered: " + str(BlockedCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Unknown Response'")
unknownResponseCount = c.fetchone()[0]
print("amount of time 'Unknown Response' was encountered: " + str(unknownResponseCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Banned'")
bannedCount = c.fetchone()[0]
print("amount of time 'Banned' was encountered: " + str(bannedCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Succeeded'")
succeededCount = c.fetchone()[0]
print("amount of time 'Succeeded' was encountered: " + str(succeededCount))

print("")
print("'No Change' percentagewise: " + str(noChangeCount / totalCount * 100) + "%")
print("'Not Crawled' percentagewise: " + str(notCrawledCount / totalCount * 100) + "%")
print("'Server Error' percentagewise: " + str(serverErrorCount / totalCount * 100) + "%")
print("'Maybe Blocked' percentagewise: " + str(maybeBlockedCount / totalCount * 100) + "%")
print("'Blocked' percentagewise: " + str(BlockedCount / totalCount * 100) + "%")
print("'Unknown Response' percentagewise: " + str(unknownResponseCount / totalCount * 100) + "%")
print("'Banned' percentagewise: " + str(bannedCount / totalCount * 100) + "%")
print("'Succeeded' percentagewise: " + str(succeededCount / totalCount * 100) + "%")

print("")

### WAF SECTION ###

c.execute("SELECT Distinct WAF FROM 'vulnerability'")
waflist = list(map(lambda x: x[0], c.fetchall()))
print("All different WAF: " + str(waflist))

######################## PIE CHART ########################
c.execute(
    "SELECT WAF, COUNT(*) FROM (SELECT DISTINCT webpage, WAF FROM 'vulnerability' WHERE WAF IS NOT 'False') GROUP BY WAF")

waflistcount = sorted(c.fetchall(), key=lambda kv: kv[1], reverse=True)
print("Amount of occurances for each WAF: ", waflistcount)

noneCount = ("No WAF", waflistcount[0][1])
otherCount = ("WAF", sum(j for i, j in waflistcount[1:]))

waflistcount = [noneCount, otherCount]

wafs, wafcounts = zip(*waflistcount)
indices = np.arange(len(waflistcount))
plt.pie(wafcounts, startangle=90, autopct='%1.00f%%')
plt.title("Percentage of crawled websites with or without WAF")
plt.legend(wafs)
plt.autoscale()
plt.show()
########################################################################

######################## PIE CHART ########################
c.execute(
    "SELECT WAF, COUNT(*) FROM (SELECT webpage, WAF, status FROM 'vulnerability' WHERE status='Blocked') GROUP BY status, WAF")

waflistcount = sorted(c.fetchall(), key=lambda kv: kv[1], reverse=True)
print("Amount of occurances for each WAF: ", waflistcount)

noneCount = ("No WAF", waflistcount[0][1])
otherCount = ("WAF", sum(j for i, j in waflistcount[1:]))

waflistcount = [noneCount, otherCount]

wafs, wafcounts = zip(*waflistcount)
indices = np.arange(len(waflistcount))
plt.pie(wafcounts, startangle=90, autopct='%1.00f%%')
plt.title("Percentage of crawled websites with / without WAF where we were blocked")
plt.legend(wafs)
plt.autoscale()
plt.show()
########################################################################

######################## WAF TYPES ########################
c.execute(
    "SELECT WAF, COUNT(*) FROM (SELECT DISTINCT webpage, WAF FROM 'vulnerability' WHERE WAF IS NOT 'None' AND WAF IS NOT 'False') GROUP BY WAF")
waflistcount = c.fetchall()
print("Amount of occurances for each WAF (excluding None/False): ", waflistcount)

waflistcount = sorted(waflistcount, key=lambda kv: kv[1], reverse=False)

otherCount = ("other", sum(j for i, j in waflistcount[:6]))
waflistcount = [otherCount] + waflistcount[6:]
wafs, wafcounts = zip(*waflistcount)
indices = np.arange(len(waflistcount))

plt.figure(figsize=(8, 10))
plt.bar(indices, wafcounts)
plt.xticks(indices, wafs, rotation='vertical')
plt.title("Amount of occurances for each WAF (excluding None/False)")
plt.subplots_adjust(top=0.9, bottom=0.45)
# plt.autoscale()
plt.show()
########################################################################

c.execute("SELECT Distinct WAF FROM 'vulnerability' WHERE status='Banned'")
distinctWafsBanned = list(map(lambda x: x[0], c.fetchall()))
print("WAF fields when banned: " + str(distinctWafsBanned))

print("")
### read log files ###
logfile1 = open("logfile1.text", "r")
logfile2 = open("logfile2.text", "r")
logfile3 = open("logfile3.text", "r")
logfile4 = open("logfile4.text", "r")

totalTime1 = 0
totalTime2 = 0
totalTime3 = 0
totalTime4 = 0
pages1 = 0
pages2 = 0
pages3 = 0
pages4 = 0

for line in logfile1:
    result = re.search(r"(\d+\.\d+).*: (\d+)", line)
    totalTime1 = float(result.group(1))
    pages1 = int(result.group(2))

for line in logfile2:
    result = re.search(r"(\d+\.\d+).*: (\d+)", line)
    totalTime2 = float(result.group(1))
    pages2 = int(result.group(2))

for line in logfile3:
    result = re.search(r"(\d+\.\d+).*: (\d+)", line)
    totalTime3 = float(result.group(1))
    pages3 = int(result.group(2))

for line in logfile4:
    result = re.search(r"(\d+\.\d+).*: (\d+)", line)
    totalTime4 = float(result.group(1))
    pages4 = int(result.group(2))

timeSum = totalTime1 + totalTime2 + totalTime3 + totalTime1

print("The total running time was:" + str(timeSum) + " seconds")
print("in minutes:", timeSum / 60)
print("in hours:", timeSum / 60 / 60)
print("")
pagesSum = pages1 + pages2 + pages3 + pages4
print("Total amount of distinct websites crawled:", 1000)
print("Total amount of pages crawled:", pagesSum)
print("the amount of distinct webpages in the DB with outputs is: ", distinctCount)
print("the total amount of entries in the DB with is: ", totalCount)

c.execute("SELECT COUNT(DISTINCT webpage) FROM 'vulnerability' WHERE WAF is not 'None' and WAF is not 'False' ")
distinctCountWithWaf = int(c.fetchone()[0])
print(
    "the percentage of webpages with WAF that we detected is:" + str(distinctCountWithWaf / distinctCount * 100) + "%")

c.execute("SELECT webpage, COUNT(*) FROM 'vulnerability' GROUP BY webpage")
distinctCountWithWaf = c.fetchall()

countDict = {}

for record in distinctCountWithWaf:
    res = (re.match(r"(https:\/\/*[^\/|\n|$]*)", record[0])).group(1)
    if res not in countDict:
        countDict[res] = record[1]
    else:
        countDict[res] += record[1]

countList = sorted(countDict.items(), key=lambda kv: kv[1], reverse=False)
countList1 = [y for x, y in countList if y <= 1]
countList2 = [y for x, y in countList if 1 < y <= 10]
countList3 = [y for x, y in countList if 10 < y <= 50]
countList4 = [y for x, y in countList if y > 50]
x = ["0-1", "2-10", "10-50", "50+"]
y = [len(countList1), len(countList2), len(countList3), len(countList4)]

plt.bar(x,y, label=y)
for i in range(len(y)):
    plt.text(i, y[i], y[i], ha='center')
plt.title("Number of payloads / website")
plt.ylabel("Number of websites")
plt.xlabel("Number of payloads")
plt.show()

c.execute("SELECT status, COUNT(webpage)  FROM (SELECT Distinct webpage, status FROM 'vulnerability' ) GROUP BY status")
countsOfStatusses = sorted(list(map(lambda x: (x[0], x[1]), c.fetchall())), key=lambda x: x[1], reverse=True)
plt.title("'Average' status / website")
statusses, counts = zip(*countsOfStatusses)
plt.bar(statusses, counts)
for i in range(len(counts)):
    plt.text(i, counts[i], counts[i], ha='center')
plt.xticks(rotation=90)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.35)
plt.show()

c.execute("SELECT status, COUNT(webpage)  FROM (SELECT webpage, status FROM 'vulnerability' ) GROUP BY status")
countsOfStatusses = sorted(list(map(lambda x: (x[0], x[1]), c.fetchall())), key=lambda x: x[1], reverse=True)
plt.title("Status / XSS attempt")
statusses, counts = zip(*countsOfStatusses)
plt.bar(statusses, counts)
for i in range(len(counts)):
    plt.text(i, counts[i], counts[i], ha='center')
plt.xticks(rotation=90)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.35)
plt.show()
