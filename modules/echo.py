import argparse
from typing import List

from main import AExec


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("echo", description="display a line of text")
		self.arg_parser.add_argument("str", metavar="STR", type=str, nargs='*')
		self.arg_parser.add_argument("-n", help="do not output the trailing newline",
									 action='store_const', default=True, const=False)

	def __call__(self, args: List[str], env, stdin=""):
		parsed = super().__call__(args, env)
		if parsed:
			for s in parsed["str"]:
				yield s + ("\n" if parsed["n"] else "")
		if stdin:
			yield stdin
