from concurrent.futures import ThreadPoolExecutor
from multiprocessing import freeze_support
import logging


class Scheduler:
	def __init__(self, pool_size):
		self.pool_size = pool_size
		freeze_support()
		self.logger = logging.getLogger(__name__)

	def future_callback_error_logger(self, future):
		try:
			future.result()
		except Exception:
			self.logger.critical("An exception was thrown!", exc_info=True)

	def submit_task(self, executor, func, *args, **kwargs):
		future = executor.submit(func, *args, **kwargs)
		future.add_done_callback(self.future_callback_error_logger)

	def run_tasks(self, funcs):
		self.logger.log(msg='Starting Tasks', level=logging.INFO)
		executor = ThreadPoolExecutor(max_workers=self.pool_size)
		results = [executor.submit(funcs[i][0], funcs[i][1]) for i in range(len(funcs))]
		for future in results:
			future.add_done_callback(self.future_callback_error_logger)


#
def task(identifier):
	print(f'Task {identifier} done')


# protect the entry point
if __name__ == '__main__':
	p = Scheduler(1)

	p.run_tasks([(task, 1), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2), (task, 2)])
