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
print("amount of time 'No Change' was encountered: " + str(notCrawledCount))

c.execute("SELECT COUNT(*) FROM 'vulnerability' WHERE status = 'Server Error'")
serverErrorCount = c.fetchone()[0]
print("amount of time 'Not Crawled' was encountered: " + str(serverErrorCount))

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

c.execute("SELECT WAF, count(*) FROM 'vulnerability' WHERE WAF is not 'None' GROUP BY WAF  ")
waflistcount = c.fetchall()
print("Amount of occurances for each WAF: ",waflistcount)

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

