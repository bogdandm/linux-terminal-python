import argparse
import os
import shutil
from pathlib import Path
from typing import List

from main import AExec, TerminalException


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("rm", description="remove files or directories")
		self.arg_parser.add_argument("file", metavar="FILE", nargs="+",
									 help="List information about the FILE")
		self.arg_parser.add_argument("-d", "--dir", action='store_const', default=False, const=True,
									 help="Remove empty directories")
		self.arg_parser.add_argument("-r", "-R", "--recursive", action='store_const', default=False, const=True,
									 help="Remove directories and their contents recursively")

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
			for file in map(Path, parsed["file"]):  # type: Path
				if not file.exists():
					raise TerminalException(f"{file}: No such file or directory")
				if file.is_dir():
					if parsed["dir"]:
						if parsed["recursive"]:
							shutil.rmtree(str(file))
						else:
							try:
								file.rmdir()
							except OSError:
								raise TerminalException(f"{file}: Directory '{file.name}' is not empty")
					else:
						raise TerminalException(f"{file}: '{file.name}' is directory")
				else:
					os.remove(str(file))
