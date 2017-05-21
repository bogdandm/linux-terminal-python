import argparse
from pathlib import Path
from typing import List

from main import AExec, TerminalException


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("mkdir ", description="make directories")
		self.arg_parser.add_argument("dir", metavar="DIRECTORY", nargs="+",
									 help="Create the DIRECTORY(ies), if they do not already exist")

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
			for d in map(Path, parsed["dir"]): # type: Path
				if d.exists():
					raise TerminalException(f"{d}: File exists")
				d.mkdir()
