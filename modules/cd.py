import argparse
from typing import List

from classes import TerminalException
from main import AExec, Main


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("cd", description="Change the shell working directory")
		self.arg_parser.add_argument("dir", metavar="DIR", default=argparse.SUPPRESS, type=str, nargs='?',
									 help="Change the current directory to DIR")

	def __call__(self, args: List[str], env: Main, stdin=""):
		parsed = super().__call__(args, env)
		if parsed is not None:
			path = (env.workdir / parsed.get("dir", env.homedir)).resolve()
			if path.exists() and path.is_dir():
				env.workdir = path
			else:
				raise TerminalException(f"{path}: No such file or directory")
