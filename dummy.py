import argparse
from typing import List

from main import AExec, TerminalException


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("", description="")

	def __call__(self, args: List[str], env, stdin=""):
		"""
		arg stdin - stdin
		yield / return - stdout
		raise ... - stderr
		:param args:
		:param env:
		:param stdin:
		:return:
		"""
		parsed = super().__call__(args, env)
		if parsed:
			pass
