import importlib
import importlib.util
import os
import pathlib
import re
import sys
from collections import Iterable
from typing import Dict, Union, List

from colorama import Fore, Style

from classes import AExec, TerminalException

STDOUT = 0
STDERR = 1


def split(str):
	def mapper(s: str):
		if not s: return ""
		s = s.strip()
		if s.startswith('"'):
			s = s[1:]
		if s.endswith('"'):
			s = s[:-1]
		return s

	yield from filter(
		None,
		map(mapper, re.split(r"( |\".*?\"|\'.*?\')", str))
	)


class Call:
	def __init__(self, env: 'Main', command: str):
		self.env = env

		self._command = command
		c: List[str] = list(split(command))
		self.module = c.pop(0)

		self.args = []
		self.redirects = []

		def test(s: str):
			return not (s.startswith('"') and s.endswith('"') or s.startswith("'") and s.endswith("'")) and ">" in s

		while c:
			s = c.pop(0)
			if test(s):
				if s == ">":
					self.redirects.append(c.pop(0))
				else:
					self.redirects.append(s[1:])
			else:
				self.args.append(s)

	def __call__(self, module, stdin=""):
		try:
			res = module(self.args, self.env, stdin)
			if isinstance(res, Iterable):
				for r in res:
					yield (r, STDOUT)
			elif res:
				yield (res, STDOUT)
		except BaseException as e:
			yield (e, STDERR)


class Main:
	def __init__(self):
		self.homedir = (pathlib.Path(__file__) / "..").resolve()
		self.workdir = pathlib.Path(os.getcwd())
		self.modules: Dict[str, AExec] = dict()
		self.imports = dict()

	def import_module(self, name: str, path: Union[str, pathlib.Path] = None):
		path = path if path is not None else str(self.homedir / "modules" / (name + ".py"))
		spec = importlib.util.spec_from_file_location(name, path)
		if spec is None:
			raise ImportError(name, path)
		module = self.imports[name] = importlib.util.module_from_spec(spec)
		try:
			spec.loader.exec_module(module)
			self.modules[name] = module.Exec()
		except (AttributeError, FileNotFoundError) as e:
			raise ImportError(e)

	def out(self, data, std=STDOUT):
		if std == STDOUT:
			return data
		elif std == STDERR:
			if isinstance(data, TerminalException):
				return f"{Fore.RED}{data.args[0]}{Style.RESET_ALL}\n"
			elif isinstance(data, BaseException):
				return f"{Fore.RED}{data.__class__.__name__}: {str(data.args)[1:-1]}{Style.RESET_ALL}\n"
			else:
				return f"{Fore.RED}{data}{Style.RESET_ALL}\n"
		else:
			raise ValueError(std)

	def run(self):
		while True:
			call = input(f"{Fore.CYAN}{self.workdir}{Style.RESET_ALL} ~\n$ ")
			if call == "exit":
				break
			self(call)

	def __call__(self, command: str):
		call = Call(self, command)
		module_name = call.module
		if module_name not in self.modules:
			try:
				self.import_module(module_name)
			except ImportError as e:
				print(self.out(e, std=STDERR), end="")
				return

		if call.redirects:
			try:
				out = [open(r, "w", encoding="utf-8") for r in call.redirects]
			except IOError as e:
				print(self.out(e, std=STDERR), end="")
				return
		else:
			out = (sys.stdout,)

		for res in call(self.modules[module_name]):
			for o in out:
				o.write(self.out(*res))


if __name__ == '__main__':
	main = Main()
	main.run()
