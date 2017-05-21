import argparse
from typing import List

from classes import TerminalException
from main import AExec


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser(
			"cat", description="concatenate files and print on the standard output"
		)
		self.arg_parser.add_argument("file", metavar="FILES", type=str, nargs='+')

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
			for file in parsed["file"]:
				try:
					with open(env.workdir / file, "r") as f:
						yield f.read()
				except FileNotFoundError:
					raise TerminalException(f"{file}: No such file or directory")
