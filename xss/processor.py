from concurrent.futures import ThreadPoolExecutor
from logging.config import fileConfig
from multiprocessing import freeze_support
import logging
from time import sleep

from colorlog import ColoredFormatter

from xss.Logger import Logger


class Scheduler:
	def __init__(self, pool_size, logging_level=logging.INFO):
		self.pool_size = pool_size
		self.logger = Logger.get_logger(logging_level)
		freeze_support()

	def future_callback_error_logger(self, future):
		try:
			identifier = future.result()
			self.logger.info('Finished Task' + str(identifier))
		except Exception:
			self.logger.critical("An exception was thrown!", exc_info=True)

	def submit_task(self, executor, func, *args, **kwargs):
		future = executor.submit(func, *args, **kwargs)
		future.add_done_callback(self.future_callback_error_logger)

	def run_tasks(self, funcs):
		self.logger.info('Starting Tasks')

		executor = ThreadPoolExecutor(max_workers=self.pool_size)

		results = []
		for i in range(len(funcs)):
			self.logger.info("Starting Task" + str(i))
			results.append(executor.submit(funcs[i][0], funcs[i][1]))

		for future in results:
			future.add_done_callback(self.future_callback_error_logger)


#
def task(identifier):
	return identifier


# protect the entry point
if __name__ == '__main__':
	p = Scheduler(2)

	p.run_tasks([(task, 1), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2)])
