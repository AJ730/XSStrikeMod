import multiprocessing
import queue

import threading
import time

exitFlag = 0


class MyThread(threading.Thread):
	def __init__(self, threadID, queueLock, workQueue,q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.q = q
		self.queueLock = queueLock
		self.workQueue = workQueue

	def run(self):
		queueLock = self.queueLock
		print("Starting " + str(self.threadID))
		while not exitFlag:
			queueLock.acquire()
			if not self.workQueue.empty():
				data = self.q.get()
				queueLock.release()
				print("%s processing %s" % (self.threadID, data))
			else:
				queueLock.release()
				time.sleep(1)
				print("Exiting " + str(self.threadID))


class Threader:
	def __init__(self, threads, jobs):
		self.threadList = [i for i in range(threads)]
		self.queueLock = threading.Lock()
		self.workQueue = queue.Queue(jobs)
		self.threads = []
		self.threadID = 1
		self.jobs = jobs
		self.exit_flag = 0

	def start(self):
		# Create new threads
		workqueue = self.workQueue
		queueLock = self.queueLock

		for id in self.threadList:
			thread = MyThread(self.threadID, queueLock,workqueue, workqueue)
			thread.start()
			self.threads.append(thread)
			self.threadID += 1

		queueLock.acquire()
		for id in range(self.jobs):
			self.workQueue.put(id)
		self.queueLock.release()

		# Wait for queue to empty
		while not workqueue.empty():
			pass

		# Notify threads it's time to exit
		self.exit_flag = 1

		# Wait for all threads to complete
		for t in self.threads:
			t.join()
		print("Exiting Main Thread")


if __name__ == '__main__':
	t = Threader(10, 1)
	t.start()
