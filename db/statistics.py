import re
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import warnings

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

c.execute("SELECT WAF, count( webpage) FROM 'vulnerability' WHERE WAF is not 'None' GROUP BY WAF  ")
waflistcount = c.fetchall()
print("Amount of occurances for each WAF: ", waflistcount)

# Todo:  labels fall off the screen

wafs, wafcounts = zip(*waflistcount)
indices = np.arange(len(waflistcount))
plt.bar(indices, wafcounts)
plt.xticks(indices, wafs, rotation='vertical')
plt.title("WAF's excluding None")
# plt.tight_layout()
plt.autoscale()
plt.show()

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
print("the percentage of webpages with WAF that we detected is:" + str(distinctCountWithWaf / distinctCount * 100) + "%")
