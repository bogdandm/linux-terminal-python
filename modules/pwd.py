import argparse
from typing import List

from main import AExec


class Exec(AExec):
	def __init__(self):
		super().__init__()
		self.arg_parser = argparse.ArgumentParser("pwd", description="print name of current/working directory")

	def __call__(self, args: List[str], env, stdin=""):
		super().__call__(args, env)
		return str(env.workdir) + "\n"
