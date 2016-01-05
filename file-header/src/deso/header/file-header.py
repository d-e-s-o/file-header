#!/usr/bin/env python

#/***************************************************************************
# *   Copyright (C) 2016 Daniel Mueller (deso@posteo.net)                   *
# *                                                                         *
# *   This program is free software: you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation, either version 3 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
# ***************************************************************************/

"""A script to check whether a list of files contains the correct headers."""

from argparse import (
  ArgumentParser,
)
from os.path import (
  basename,
)
from sys import (
  argv as sysargv,
  stderr,
)


def hasCorrectHeader(file_):
  """Check whether a file contains an appropriate header."""
  with open(file_, "r") as f:
    try:
      line = next(f)
      return line.startswith("#!") or basename(file_) in line
    except (StopIteration, UnicodeDecodeError):
      return False


def main(argv):
  """Check whether all given files contain the correct header."""
  parser = ArgumentParser()
  parser.add_argument(
    "files", action="store", default=[], nargs="+",
    help="A list of files to check.",
  )
  ns = parser.parse_args(argv[1:])

  for file_ in ns.files:
    if not hasCorrectHeader(file_):
      print("%s does not contain a correct file header." % basename(file_), file=stderr)
      return 1

  return 0


if __name__ == "__main__":
  exit(main(sysargv))
