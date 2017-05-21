import argparse
import datetime
import os
import stat
from pathlib import Path
from typing import List

from hurry import filesize

from classes import TerminalException
from main import AExec


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("ls", description="list directory contents")
		self.arg_parser.add_argument("file", metavar="FILE", default=".", nargs="?",
									 help="List information about the FILE")
		self.arg_parser.add_argument("-l", "--list", action='store_const', default=False, const=True,
									 help="Use a long listing format")

		self.format_str = "{mode:10} {gid:5} {uid:5} {size:6} {time:} {name:}\n"

	def _format(self, file, mode):
		if mode == "l":
			status = os.stat(file)
			return self.format_str.format(
				mode=stat.filemode(status.st_mode),
				gid=status.st_gid,
				uid=status.st_uid,
				time=datetime.datetime.fromtimestamp(status.st_mtime),
				size=filesize.size(status.st_size),
				name=file.name
			)
		return file.name + "\n"

	def __call__(self, args: List[str], env, stdin=""):
		parsed = super().__call__(args, env)
		if parsed:
			if parsed["list"]:
				mode = "l"
			else:
				mode = "*"

			file = (env.workdir / Path(parsed.get("file"))).resolve()
			if not file.exists():
				raise TerminalException(f"{file}: No such file or directory")
			if file.is_dir():
				for f in file.iterdir():
					yield self._format(f, mode)
			else:
				self._format(file, mode)
