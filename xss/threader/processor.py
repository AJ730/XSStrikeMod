from concurrent.futures import ThreadPoolExecutor
from multiprocessing import freeze_support
import logging


from xss.logger.Logger import Logger


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
		"""
		Submit a new task to the executor
		@param executor: executor
		@type executor: executor
		@param func: func
		@type func: func
		@param args: args
		@type args: args
		@param kwargs: kwargs
		@type kwargs: kwargs
		@return: rask
		@rtype:
		"""
		future = executor.submit(func, *args, **kwargs)
		future.add_done_callback(self.future_callback_error_logger)

	def run_tasks(self, funcs):
		"""
		run all tasks
		@param funcs: funcs
		@type funcs: funcs
		@return: tasks
		@rtype: tasks
		"""
		self.logger.info('Starting Tasks')

		executor = ThreadPoolExecutor(max_workers=self.pool_size)

		results = []
		for i in range(len(funcs)):
			self.logger.info("Starting Task" + str(i))
			results.append(executor.submit(funcs[i][0], funcs[i][1]))

		for future in results:
			future.add_done_callback(self.future_callback_error_logger)


#
def task(identifier, *args):
	"""
	All tasks must have an identifier
	@param identifier: id
	@type identifier: id
	@return: id
	@rtype: anyType
	"""
	return identifier


# protect the entry point
if __name__ == '__main__':
	p = Scheduler(2)

	p.run_tasks([(task, 1), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2)])
