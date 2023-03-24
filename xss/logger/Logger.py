import logging

from colorlog import ColoredFormatter


class Logger:

	@staticmethod
	def get_logger(Log_level):
		LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

		logging.root.setLevel(Log_level)
		formatter = ColoredFormatter(LOGFORMAT)
		stream = logging.StreamHandler()
		stream.setLevel(Log_level)
		stream.setFormatter(formatter)

		log = logging.getLogger('pythonConfig')
		log.setLevel(Log_level)
		log.addHandler(stream)
		return log
