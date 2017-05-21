import abc
import shlex
from typing import List


class AExec(metaclass=abc.ABCMeta):
	instance = None

	@abc.abstractmethod
	def __init__(self):
		self.__class__.instance = self
		self.arg_parser = None

	@abc.abstractmethod
	def __call__(self, args: List[str], env, stdin=""):
		try:
			return vars(self.arg_parser.parse_args(args))
		except SystemExit:
			return None

class TerminalException(Exception):
	pass